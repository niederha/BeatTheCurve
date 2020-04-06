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
    sliderGOF.value = sendSimulationData.simulationData.goOutFrq;
}

function sliderSDCB(){
    sendSimulationData.simulationData.fracFollowSD = sliderSD.value;
    textSD.innerHTML = "Fraction of pepople following social distancing: " + sliderSD.value + "%";
}

function sliderGOFCB() {
    sendSimulationData.simulationData.goOutFrq = sliderGOF.value;
    textGOF.innerHTML = "Number of time per week people go to crowded places on average (e.g: supermarket):  " + sliderGOF.value;
}
sendSimulationData(); // Get the first simulation

// Bind callbacks

// country DDL
var countrySelector = document.getElementById("countrySelector");
countrySelector.onchange = function(){
    sendSimulationData.simulationData.country = countrySelector.value};

// SD slider
var sliderSD = document.getElementById("sliderSD");
var textSD = document.getElementById("textSD");
sliderSD.oninput = sliderSDCB;

// GOF slider
var sliderGOF = document.getElementById("sliderGOF");
var textGOF = document.getElementById("textGOF");
sliderGOF.oninput = sliderGOFCB;


var buttonSimulate = document.getElementById("buttonSimulate");
buttonSimulate.onclick = sendSimulationData;

 // Initialise  parameter view
 initialiseParamView();