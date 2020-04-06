/*jshint esversion: 6 */

google.charts.load('current', {
  'packages': ['geochart']
});

let dataPippo = [];
let dataPippoInt = [];
let dataPippo1 = [];
var pippoIndex = 0;

const pippoList = [
  ["total_cases_per_1m_population", "cases"],
  ["deaths", "new_deaths"],
  ["serious_critical", "active_cases"],
  ["total_recovered", "active_cases"]
];

function changePippoIndex(val){
  pippoIndex = val;
  getPippoData();
}

function getPippoData() {
  fetch("https://coronavirus-monitor.p.rapidapi.com/coronavirus/cases_by_country.php", {
      "method": "GET",
      "headers": {
        "x-rapidapi-host": "coronavirus-monitor.p.rapidapi.com",
        "x-rapidapi-key": "815636d2f5msh5b6f6b41061625ep10f46fjsn4221a8a8f565"
      }
    })
    .then(response => response.json().then(data => {
      function fixElemName(el) {
        if (el.country_name == "USA")
          el.country_name = "United States";
        else if (el.country_name == "UK")
          el.country_name = "United Kingdom";
      }
      dataPippo = data.countries_stat;
      dataPippo.forEach((el, i) => {
        fixElemName(el);
        dataPippo[i] = [el["country_name"], el[pippoList[pippoIndex][0]], el[pippoList[pippoIndex][1]]];
      });
      ///{"country_name":"UK","cases":"47,806","deaths":"4,934","region":"","total_recovered":"135","new_deaths":"621","new_cases":"5,903","serious_critical":"1,559","active_cases":"42,737","total_cases_per_1m_population":"704"},
    }))
    .then(() => {
      drawRegionsMap(["Country", ...pippoList[pippoIndex]]);
    })
    .catch(err => {
      console.log(err);
    });
}

function drawRegionsMap(labels) {
  function filterData(data, i){
    if (i != 0)
      data = parseInt(data.replace(",", ""));
    return data;
  }
  dataPippo.forEach((el, i1) => dataPippoInt[i1] = el.map((el1,i2) => filterData(el1, i2)));
  dataPippo1 = dataPippoInt.map(el => el[1]);
  maxVal = Math.max(...dataPippo1);
  if (pippoIndex == 0) maxVal = 3500;
  else if (pippoIndex == 3) maxVal/=2;

  dataPippoInt.unshift(labels);
  var data = google.visualization.arrayToDataTable(
    dataPippoInt
  );

  var options = {
    backgroundColor: {
      fill: "transparent"
    },
    colorAxis: {
      minValue: 0,
      maxValue: maxVal,
      colors: ['rgb(150, 180, 252)', 'rgb(23, 78, 166)']
    },
  };
  var chart = new google.visualization.GeoChart(document.getElementById('regions_div'));
  chart.draw(data, options);
}

google.charts.setOnLoadCallback(getPippoData);
window.onresize = drawRegionsMap;
