/*jshint esversion: 6 */
// Update figures
//

function divAddData(idElem, data1, data2){
  container_element = document.getElementById(idElem);
  container_element.innerHTML = "";
  let div1 = document.createElement('div');
  div1.classList.add("w3-container","w3-third","w3-margin", "w3-cell-middle");
  let paragraph = document.createElement('h3');
  paragraph.textContent = data1;
  div1.appendChild(paragraph);
  let div2 = document.createElement('div');
  if (data2){
    div2.classList.add("w3-container","w3-third","w3-margin", "w3-middle");
    let paragraph2 = document.createElement('h7');
    paragraph2.textContent = 'new: ' + data2;
    div2.appendChild(paragraph2);
  }
  //paragraph.classList.add('class1');
  container_element.appendChild(div1);
  if (data2) {container_element.appendChild(div2)};
}

fetch("https://coronavirus-monitor.p.rapidapi.com/coronavirus/worldstat.php", {
	"method": "GET",
	"headers": {
		"x-rapidapi-host": "coronavirus-monitor.p.rapidapi.com",
		"x-rapidapi-key": "815636d2f5msh5b6f6b41061625ep10f46fjsn4221a8a8f565"
	}
})
.then(response => response.json().then(data => {
  divAddData("nbSuceptible", "5,424,242");
  divAddData("nbSick", data.total_cases, data.new_cases);
  divAddData("nbDead", data.total_deaths, data.new_deaths);
  divAddData("nbImmune", data.total_recovered);
}))
.catch(err => {
    console.log(err);
});
