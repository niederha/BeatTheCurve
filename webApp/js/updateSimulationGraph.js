google.charts.load('current', { 'packages': ['corechart'] });
google.charts.setOnLoadCallback(drawChart);
window.onresize = drawChart;
window.onload = updateNumericalData;

function updateNumericalData(){
    document.getElementById("sim_nbSuceptible").innerHTML = 12345656;
    document.getElementById("sim_nbSick").innerHTML = 1234789;
    document.getElementById("sim_nbDead").innerHTML = 324789017;
    document.getElementById("sim_nbImmune").innerHTML = 1723849;

}

function drawChart() {

    // Define static variables
    if (typeof drawChart.displayMask == 'undefined'){
        drawChart.displayMask = [true, true, true, true, true, true];
    }

    var data = google.visualization.arrayToDataTable([
        ['Day since beginning', 'Suceptible',   'Infected', 'Deaths',   'Recovered', 'Hositalized', 'Hospital capacity'],
        ['0',                   0,                 0,        0,          0,           0,             1000],
        ['1',                   1000,            400,        0,          12,          44,            1000],
        ['2',                   900,             499,        20,         50,          100,           1000],
        ['3',                   300,             1100,       100,        300,         700,           1000],
        ['4',                   100,             2000,       500,        400,         1000,          1000]
    ]);
    
    view = new google.visualization.DataView(data);
    for (var i = 0; i < drawChart.displayMask.length; i++){
        if(!drawChart.displayMask[i]){
            view.hideColumns([i+1]);
        }
    }

    var options = {
        title: '',
        curveType: 'function',
        backgroundColor: { fill: "transparent" },
        legend: { position: 'bottom' },
        hAxis: { baseline: 0, title: "Number of days", viewWindow: {min: 0}},
        vAxis: { baseline: 0, title: "Number of people", viewWindow: {min: 0}},
        legend: { position: "none"},
        height: 400
    };

    var chart = new google.visualization.LineChart(document.getElementById('SimulationGraph'));
    chart.draw(view, options);
}


