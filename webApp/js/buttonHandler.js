class displayCurveButtonHandler {

    constructor(buttonId, curveName, color, isOnDisplay = true) {
        this.button = document.getElementById(buttonId);
        this.isOnDisplay = isOnDisplay;
        this.textOncolor = "w3-text-white";
        this.textOffColor = "w3-text-" + color;
        this.buttonOnColor = "w3-" + color;

        this.curveName = curveName;
        // Setup borders if needed
        var borderClassTag = "w3-border-" + color;
        if (!this.button.classList.contains(borderClassTag)) {
            this.button.classList.add(borderClassTag);
        }

        // Setup callback
        this.button.addEventListener('click', this.reverseButton);
    }

    reverseDispay() {
        this.reverseButton()
        this.reverseCurveVisibility()
        this.isOnDisplay = !this.isOnDisplay;
    }

    turnOnButton() {
        this.button.classList.add(this.buttonOnColor);
        this.button.classList.remove(this.textOffColor);
        this.button.classList.add(this.textOnColor);
    }

    turnOffButton() {
        this.button.classList.remove(this.buttonOnColor);
        this.button.classList.remove(this.textOnColor);
        this.button.classList.add(this.textOnColor);
    }
    
    reverseCurveVisibility() {
        console.log("Reverse display");
    }

    reverseButton() {
        if (this.isOnDisplay) {
            //this.turnOffButton();
            console.log(typeof this.turnOffButton);
        } else {
            //this.turnOnButton();
            console.log(typeof this.turnOffButton);
        }
        this.isOnDisplay = !this.isOnDisplay;
    }

    
}