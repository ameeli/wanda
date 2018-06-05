// Script for creating mw chart, used by profile_overview.html
d3.json("/mw_graph_data.json", createMwChart);

function createMwChart(data) {
  var svg1 = d3.select("#svg1"),
    margin = {top: 70, right: 20, bottom: 70, left: 60},
    width = +svg1.attr("width") - margin.left - margin.right,
    height = +svg1.attr("height") - margin.top - margin.bottom;

  svg1.selectAll("*").remove();

  var x = d3.scaleBand().rangeRound([0, width]).padding(0.1);
  var y = d3.scaleLinear().rangeRound([height, 0]);

  var g = svg1.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var tooltip = d3.select("body")
    .append("div")
    .attr("class", "toolTip");

  x.domain(data.map(function(d) { return d.happiness; }));
  y.domain([0, d3.max(data, function(d) { return d.frequency; })]);

  g.append("text")
    .attr("x", (width / 2))             
    .attr("y", 0 - (margin.top / 2))
    .attr("text-anchor", "middle")  
    .style("font-size", "16px") 
    .style("text-decoration", "none")  
    .text("Happiness While Mind Wandering"); 

  // Add the x Axis
  g.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x));

  // text label for the x axis
  g.append("text")             
    .attr("transform", "translate(" + (width/2) + " ," + (height + margin.top - 30) + ")")
    .style("text-anchor", "middle")
    .text("Happiness");

  // text label for the y axis
  g.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 5 - margin.left)
    .attr("x", 0 - (height / 2))
    .attr("dy", "1em")
    .style("text-anchor", "middle")
    .text("Frequency");   

  g.append("g")
    .attr("class", "axis axis--x")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x));

  g.append("g")
    .attr("class", "axis axis--y")
    .call(d3.axisLeft(y).ticks(10))
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", "0.71em")
      .attr("text-anchor", "end")
      .text("Frequency");

  g.selectAll(".bar")
    .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.happiness); })
      .attr("y", function(d) { return y(d.frequency); })
      .attr("width", x.bandwidth())
      .attr("height", function(d) { return height - y(d.frequency); })
      .on("mouseover", function(d){
            tooltip
              .style("left", d3.event.pageX - 35 + "px")
              .style("top", d3.event.pageY - 30 + "px")
              .style("display", "inline-block")
              .html((d.frequency) + " reports");
        })
        .on("mouseout", function(d){ tooltip.style("display", "none");});
}