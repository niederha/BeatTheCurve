/*jshint esversion: 6 */

google.charts.load('current', {
  'packages': ['geochart']
});

let dataPippo = [];

function getPippoData() {
  fetch("https://coronavirus-monitor.p.rapidapi.com/coronavirus/cases_by_country.php", {
      "method": "GET",
      "headers": {
        "x-rapidapi-host": "coronavirus-monitor.p.rapidapi.com",
        "x-rapidapi-key": "815636d2f5msh5b6f6b41061625ep10f46fjsn4221a8a8f565"
      }
    })
    .then(response => response.json().then(data => {
			function fixElemName(el){
				if (el.country_name == "USA")
					el.country_name = "United States";
				else if  (el.country_name == "UK")
					el.country_name = "United Kingdom";
			}
      dataPippo = data.countries_stat;
      dataPippo.forEach((el, i) => {
				fixElemName(el);
        dataPippo[i] = [el.country_name, el.cases];
      });
      dataPippo.unshift(['Country', 'Number cases']);
    }))
    .then(() => {
      drawRegionsMap();
    })
    .catch(err => {
      console.log(err);
    });
}

function sleep(time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

function drawRegionsMap() {

  var data = google.visualization.arrayToDataTable(
    dataPippo
  );

  var options = {
    backgroundColor: {
      fill: "transparent"
    },
    colorAxis: {
      minValue: 0,
      maxValue: 1000,
      colors: ['green', 'red', 'black']
    },
  };
  var chart = new google.visualization.GeoChart(document.getElementById('regions_div'));
  chart.draw(data, options);
}

google.charts.setOnLoadCallback(getPippoData);
window.onresize = drawRegionsMap;
