$(document).ready(function(){
    $(".nav-pills a").click(function(){
        $(this).tab('show');
    });
});

var url = document.location.toString(); // select current url shown in browser.
if (url.match('#')) {
        $('.nav-pills a[href=#' + url.split('#')[1] + ']').tab('show'); // activate current tab after reload page.
        displayD3Figure();
    }
    // Change hash for page-reload
    $('.nav-pills a').on('shown', function (e) { // this function call when we change tab.
        window.location.hash = e.target.hash; // to change hash location in url.
});

function displayD3Figure() {
    d3.text("data/test.json", function(error, text) {
    if(error) return console.warn(error);
    var matrixString = d3.csvParseRows(text);

    // converts string array to int array
    var matrix = [];
    for (i in matrixString) {
        matrix[i] = matrixString[i].map(Number);
    }

    // initializes the draw space
    var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height"),
    outerRadius = Math.min(width, height) * 0.5 - 40,
    innerRadius = outerRadius - 30;

    //var formatValue = d3.formatPrefix(",.0", 1e3);

    var chord = d3.chord()
        .padAngle(0.01)
        .sortSubgroups(d3.descending);

    var arc = d3.arc()
        .innerRadius(innerRadius)
        .outerRadius(outerRadius);

    var ribbon = d3.ribbon()
        .radius(innerRadius);

    var color = d3.scaleOrdinal()
        .domain(d3.range(35))
        .range(["#5eaf82", "#9e91fa", "#f76c79", "#99a869", "#d2957d", "#a2aca6", "#e3959e", "#adaefc", "#5bd14e", "#df9ceb", "#fe8fb1", "#87ca80", "#fc986d", "#2ad3d9", "#e8a8bb", "#a7c79c", "#a5c7cc", "#7befb7", "#b7e2e0", "#85f57b", "#f5d95b", "#dbdbff", "#fddcff", "#6e56bb", "#226fa8", "#5b659c", "#58a10f", "#e46c52", "#62abe2", "#c4aa77", "#b60e74", "#087983", "#a95703", "#2a6efb", "#427d92"]);

    var g = svg.append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")
        .datum(chord(matrix));

    // initializes groups
    var group = g.append("g")
        .attr("class", "groups")
        .selectAll("g")
        .data(function(chords) { return chords.groups; })
        .enter().append("g");
    
    // draws different nodes
    group.append("path")
        .style("fill", function(d) { return color(d.index); })
        .style("stroke", function(d) { return d3.rgb(color(d.index)).darker(); })
        .attr("d", arc);

    // draws ticks
    var groupTick = group.selectAll(".group-tick")
        .data(function(d) { return groupTicks(d, 1); })
        .enter().append("g")
        .attr("class", "group-tick")
        .attr("transform", function(d) { return "rotate(" + (d.angle * 180 / Math.PI - 90) + ") translate(" + outerRadius + ",0)"; });

    groupTick.append("line")
        .attr("x2", 6);

    groupTick
        .filter(function(d) { return d.value % 5 === 0; })
        .append("text")
        .attr("x", 8)
        .attr("dy", ".35em")
        .attr("transform", function(d) { return d.angle > Math.PI ? "rotate(180) translate(-16)" : null; })
        .style("text-anchor", function(d) { return d.angle > Math.PI ? "end" : null; })
        .text(function(d) { return d.value; });

    // draws ribbons
    g.append("g")
        .attr("class", "ribbons")
        .selectAll("path")
        .data(function(chords) { return chords; })
        .enter().append("path")
        .attr("d", ribbon)
        .style("fill", function(d) { return color(d.target.index); })
        .style("stroke", function(d) { return d3.rgb(color(d.target.index)).darker(); });
});


}


// Returns an array of tick angles and values for a given group and step.
function groupTicks(d, step) {
    console.log(d);
    var k = (d.endAngle - d.startAngle) / d.value;
    //console.log(d.value);
    //console.log(k);
    return d3.range(0, d.value, step).map(function(value) {
        //console.log({value: value, angle: value * k + d.startAngle});
        return {value: value, angle: value * k + d.startAngle};
  });
}
