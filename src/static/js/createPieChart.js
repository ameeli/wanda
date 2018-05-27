// Script for creating pie chart, used by profile_overview.html
d3.json("/pie-chart.json", createPieChart);

function createPieChart(data) {    
  // create svg to take dimensions specified in profile_overview
  var svg = d3.select("svg"),
      width = +svg.attr("width"),
      height = +svg.attr("height"),
      radius = Math.min(width, height) / 2,
      g = svg.append("g").attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

  var color = d3.scaleOrdinal(["#98abc5", "#8a89a6"]);

  // points to where pie should get % data
  var pie = d3.pie()
      .sort(null)
      .value(function(d) { return d.occurrence; });

  // radius of entire circle
  var path = d3.arc()
      .outerRadius(radius - 10)
      .innerRadius(radius - 130);

  // focusing and wandering labels placement
  var label = d3.arc()
    .outerRadius(radius - 75)
    .innerRadius(radius - 75);

  var infoLabel = d3.arc()
    .outerRadius(radius - 100)
    .innerRadius(-80)

  var arc = g.selectAll(".arc")
    .data(pie(data))
    .enter().append("g")
    .attr("class", "arc")
    .on("mouseover", handleMouseOver)
    .on("mouseout", handleMouseOut);

  arc.append("path")
    .attr("d", path)
    .attr("fill", function(d) { return color(d.data.mw); });

  // labeling each half with text
  arc.append("text")
    .attr("transform", function(d) { 
      return "translate(" + label.centroid(d) + ")"; 
    })
    .attr("y", "10")
    .attr("x", "5")
    .attr("fill", "white")
    .text(function(d) { return d.data.mw; });

  function handleMouseOver() {
    arc.append("text")
      .style("font", "15px sans-serif")
      .attr("fill", "#8a89a6")
      .attr("id", "info")
      .text("Focusing: 62 reports")
      
    arc.append("text")
      .attr("transform", "translate(0, 20)" )
      .attr("fill", "#98abc5")
      .style("font", "15px sans-serif")
      .attr("id", "info")
      .text("Wandering: 50 reports");
  }

  function handleMouseOut() {
    svg.selectAll("#info").remove();
  }
}
