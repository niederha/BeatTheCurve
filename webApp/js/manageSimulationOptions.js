function sendSimulationData(){
    //Default values
    if (typeof sendSimulationData.simulationData == 'undefined'){
        sendSimulationData.simulationData = {
            country: 'CH',
            fracFollowSD: 0,
            lvlSD: 'none',
            hygiene: 'dirty',
            isolationOfInfected: false,
            goOutFrq: 7
        }
    }
    sendSimulationData.simulationData.country;
    console.log(sendSimulationData.simulationData);
}

function initialiseParamView(){
    countrySelector.value = sendSimulationData.simulationData.country;
    sliderSD.value = sendSimulationData.simulationData.fracFollowSD;
}

function sliderSDCB(){
    sendSimulationData.simulationData.fracFollowSD = sliderSD.value;
    textSD.innerHTML = "Fraction of pepople following social distancing: " + sliderSD.value + "%";
}

sendSimulationData(); // Get the first simulation

// Bind callbacks
var countrySelector = document.getElementById("countrySelector");
countrySelector.onchange = function(){
    sendSimulationData.simulationData.country = countrySelector.value};

var sliderSD = document.getElementById("sliderSD");
var textSD = document.getElementById("textSD")
sliderSD.oninput = sliderSDCB

var buttonSimulate = document.getElementById("buttonSimulate");
buttonSimulate.onclick = sendSimulationData;

 // Initialise  parameter view
 initialiseParamView();