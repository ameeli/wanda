// Script for creating pie chart, used by profile_overview.html
d3.json("/pie-chart.json", createPieChart);

function createPieChart(data) {    
  // create svg to take dimensions specified in profile_overview
  var svg = d3.select("#svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height"),
    radius = Math.min(width, height) / 2

  svg.selectAll("*").remove();
    
  var g = svg.append("g").attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

  var color = d3.scaleOrdinal(["#8e9aaf", "#b8dbd9"]);

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
    .style("fill", function(d) { return color(d.data.mw); })
      .transition()
      .ease(d3.easeLinear)
      .duration(1500)
      .attrTween("d", pieTween)

  function pieTween(b) {
    b.innterRadius = 0;
    var i = d3.interpolate({startAngle: 0, endAngle: 0}, b);
    return function(t) { return path(i(t)); };
  }

  // labeling each half with text
  arc.append("text")
    .attr("transform", function(d) { return "translate(" + label.centroid(d) + ")"; })
    .attr("y", "10")
    .attr("x", "5")
    .attr("fill", "white")
    .text(function(d) { return d.data.mw; });

  function handleMouseOver() {
    arc.append("text")
      .attr("id", "focus-pie-info")
      .text("Focusing: 62 reports")
      
    arc.append("text")
      .attr("transform", "translate(0, 20)" )
      .attr("id", "mw-pie-info")
      .text("Wandering: 50 reports");
  }

  function handleMouseOut() {
    svg.selectAll("#focus-pie-info").remove();
    svg.selectAll("#mw-pie-info").remove();
  }
}