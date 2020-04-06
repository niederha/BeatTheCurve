google.charts.load('current', { 'packages': ['corechart'] });
google.charts.setOnLoadCallback(drawChart);
window.onresize = drawChart;
window.onload = updateNumericalData;

function updateNumericalData(){
    document.getElementById("sim_nbSuceptible").innerHTML = 12345656;
    document.getElementById("sim_nbSick").innerHTML = 1234789;
    document.getElementById("sim_nbDead").innerHTML = 324789017;
    document.getElementById("sim_nbImmune").innerHTML = 1723849;
    document.getElementById("sim_nbAcuteSyptoms").innerHTML = 174569;
    document.getElementById("sim_hospitalCapacity").innerHTML = 32453252345;
}

function drawChart() {


    colorList = ['#009688', '#ff5722', '#607d8b', '#4caf50', '#616161', '#000000'];
                 
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
    
    // Choosing which curves to display in which color
    var view = new google.visualization.DataView(data);
    var colorSerie = {};
    var nbActiveSerie = 0
    for (var i = 0; i < drawChart.displayMask.length; i++){
        if(!drawChart.displayMask[i]){
            view.hideColumns([i+1]);
        }else{
            colorSerie[nbActiveSerie++] = {color: colorList[i]};
        }
    }

    var options = {
        title: '',
        curveType: 'function',
        backgroundColor: { fill: "transparent" },
        legend: { position: 'bottom' },
        hAxis: { baseline: 0, title: "Number of days", viewWindow: {min: 0}},
        vAxis: { baseline: 0, title: "Number of people", viewWindow: {min: 0, max: 2000}},
        legend: { position: "none"},
        height: 500,
        series: colorSerie
    };
    console.log(options)
    var chart = new google.visualization.LineChart(document.getElementById('SimulationGraph'));
    chart.draw(view, options);
}



