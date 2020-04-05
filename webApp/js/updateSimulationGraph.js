google.charts.load('current', { 'packages': ['corechart'] });
google.charts.setOnLoadCallback(drawChart);
window.onresize = drawChart;

function drawChart() {
    var data = google.visualization.arrayToDataTable([
        ['Day since beginning', 'Suceptible',   'Infected', 'Deaths',   'Recovered', 'Hositalized', 'Hospital capacity'],
        ['1',                   1000,            400,        0,          12,          44,            1000],
        ['2',                   900,             499,        20,         50,          100,           1000],
        ['3',                   300,             1100,       100,        300,         700,           1000],
        ['4',                   100,             2000,       500,        400,         1000,          1000]
    ]);

    var options = {
        title: 'How would COVID-19 spread',
        curveType: 'function',
        backgroundColor: { fill: "transparent" },
        legend: { position: 'bottom' }
    };

    var chart = new google.visualization.LineChart(document.getElementById('SimulationGraph'));

    chart.draw(data, options);
}