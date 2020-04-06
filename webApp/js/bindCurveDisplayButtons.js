// I wanted a class but this is js... so this is the next best thing
function createDisplayCurveButtonHandler(buttonId, curveNum, color, isOnDisplay = true) {
    var displayCurveButtonHandler = function(){};
    displayCurveButtonHandler.button = document.getElementById(buttonId);
    displayCurveButtonHandler.isOnDisplay = isOnDisplay;
    displayCurveButtonHandler.textOnColor = "w3-text-white";
    displayCurveButtonHandler.textOffColor = "w3-text-" + color;
    displayCurveButtonHandler.buttonOnColor = "w3-" + color;
    displayCurveButtonHandler.curveNum = curveNum;

    // Setup borders if needed
    var borderClassTag = "w3-border-" + color;
    if (displayCurveButtonHandler.button.classList.contains(borderClassTag)) {
        displayCurveButtonHandler.button.classList.add(borderClassTag);
    }
    return displayCurveButtonHandler
}
function turnOnButton(bh){
    bh.button.classList.add(bh.buttonOnColor);
    bh.button.classList.remove(bh.textOffColor);
    bh.button.classList.add(bh.textOnColor);
    drawChart.displayMask[bh.curveNum] = true;
}
function turnOffButton(bh) {
    bh.button.classList.remove(bh.buttonOnColor);
    bh.button.classList.remove(bh.textOnColor);
    bh.button.classList.add(bh.textOffColor);
    drawChart.displayMask[bh.curveNum] = false;
}
function reverseButton(bh) {
    if (bh.isOnDisplay) {
        turnOffButton(bh);
    } else {
        turnOnButton(bh);
    }
    bh.isOnDisplay = !bh.isOnDisplay;
    drawChart();
}

google.charts.setOnLoadCallback(setButtonCallbacks);

// Button callback bindings



function setButtonCallbacks() {
    var buttonSuceptible = createDisplayCurveButtonHandler("buttonSuceptible", 0, "teal");
    var buttonSick = createDisplayCurveButtonHandler("buttonSick", 1, "deep-orange");
    var buttonDead = createDisplayCurveButtonHandler("buttonDead", 2, "blue-gray");
    var buttonRecovered = createDisplayCurveButtonHandler("buttonRecovered", 3, "green");
    var buttonAcuteSymptoms = createDisplayCurveButtonHandler("buttonAcuteSymptoms", 4, "dark-gray");
    var buttonHospitalCapacity = createDisplayCurveButtonHandler("buttonHospitalCapacity", 5, "black");

    buttonSuceptible.button.onclick = function(){reverseButton(buttonSuceptible)};
    buttonSick.button.onclick = function () { reverseButton(buttonSick) };
    buttonDead.button.onclick = function () { reverseButton(buttonDead) };
    buttonRecovered.button.onclick = function () { reverseButton(buttonRecovered) };
    buttonAcuteSymptoms.button.onclick = function () { reverseButton(buttonAcuteSymptoms) };
    buttonHospitalCapacity.button.onclick = function () { reverseButton(buttonHospitalCapacity) };
}



