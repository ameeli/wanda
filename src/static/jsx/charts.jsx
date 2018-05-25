"use strict";


class Chart extends React.Component { 

    constructor(props) {
        super(props);
        this.state = { 
          isHovered: false,
          chartData: ""} 
        this.setHovered = this.setHovered.bind(this)
        this.renderPieChart = this.renderPieChart.bind(this);
    }

    componentDidMount() {
        fetch('/pie-chart.json')
            .then((response) => response.json())
            .then((data) => this.setState( { chartData: data });

        // console.log('pieChartData: ', pieChartData);

        // this.setState({ data: pieChartData });
    }

    setHovered() {
        this.setState({ isHovered: true});

    }

    renderPieChart(data) {
      var svg = d3.select("#svg"),
          width = 280,
          height = 500,
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
          .innerRadius(0);

      // focusing and wandering labels placement
      var label = d3.arc()
          .outerRadius(radius - 120)
          .innerRadius(radius - 120);

      var arc = g.selectAll(".arc")
        .data(pie(data))
        .enter().append("g")
        .attr("class", "arc")

      arc.append("path")
        .attr("d", path)
        .attr("fill", function(d) { return color(d.data.mw); });

      // labeling each half with text
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

    render() {
        return (
            // have to render a DOM element here, so the issue is that my chart 
            // is not a DOM element and React won't like that. look into d3 react
            // libraries that may translate graph into DOM
        );
    }
}

ReactDOM.render(
    <Chart/>,
    document.getElementById("root")
);
