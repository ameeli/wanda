// Script for creating pie chart, used by profile_overview.html
function createPieChart(data) {    
  var svg = d3.select("svg"),
      width = +svg.attr("width"),
      height = +svg.attr("height"),
      radius = Math.min(width, height) / 2,
      g = svg.append("g").attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

  var color = d3.scaleOrdinal(["#98abc5", "#8a89a6"]);

  var pie = d3.pie()
      .sort(null)
      .value(function(d) { return d.occurrence; });

  var path = d3.arc()
      .outerRadius(radius - 10)
      .innerRadius(0);

  var label = d3.arc()
      .outerRadius(radius - 120)
      .innerRadius(radius - 120);

  var arc = g.selectAll(".arc")
    .data(pie(data))
    .enter().append("g")
    .attr("class", "arc");

  // svg.append("text")
  //   .attr("x", (width / 2))             
  //   .attr("y", (width / 2))
  //   .attr("text-anchor", "middle")  
  //   .style("font-size", "16px") 
  //   .style("text-decoration", "underline")  
  //   .text("Value vs Date Graph");


  arc.append("path")
    .attr("d", path)
    .attr("fill", function(d) { return color(d.data.mw); });


  arc.append("text")
    .attr("transform", function(d) { 
      return "translate(" + label.centroid(d) + ")"; 
    })
    .attr("dy", "0.40em") // y axis
    .attr("y", "10")
    .attr("x", "5")
    .attr("fill", "white")
    .text(function(d) { return d.data.mw; });
}

function getPieData() {
  $.get('/pie-chart.json', createPieChart);
}

getPieData();