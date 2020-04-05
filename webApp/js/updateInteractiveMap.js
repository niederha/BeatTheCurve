
google.charts.load('current', {'packages': ['geochart']});
google.charts.setOnLoadCallback(drawRegionsMap);
window.onresize = drawRegionsMap;
window.onload = sliderMap;

//slider
function sliderMap() {
 var slider = document.getElementById("myRange");
 var output = document.getElementById("demo");
 output.innerHTML = slider.value; // Display the default slider value
 
 // Update the current slider value (each time you drag the slider handle)
    slider.oninput = function() {
        output.innerHTML = this.value;    
    }
}
function drawRegionsMap() {

    var data = google.visualization.arrayToDataTable([
        ['Country', 'Number cases'],
        ['Germany', 200],
        ['United States', 300],
        ['Brazil', 400],
        ['Canada', 500],
        ['France', 600],
        ['RU', 700]
    ]);

    var options = {
        backgroundColor: {fill:"transparent"},
        colorAxis: {minValue: 0, maxValue: 1000, colors: ['green', 'red', 'black']},
    };
    var chart = new google.visualization.GeoChart(document.getElementById('regions_div'));
    chart.draw(data, options);  
}