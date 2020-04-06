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
    console.log(sendSimulationData.simulationData);
}

function initialiseParamView(){
    countrySelector.value = sendSimulationData.simulationData.country;
}


sendSimulationData(); // Get the first simulation

// Bind callbacks
var countrySelector = document.getElementById("countrySelector");
countrySelector.onchange = function(){
    sendSimulationData.simulationData.country = countrySelector.value};


var buttonSimulate = document.getElementById("buttonSimulate");
buttonSimulate.onclick = sendSimulationData;

 // Initialise  parameter view
 initialiseParamView();