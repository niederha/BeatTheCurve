var a1=["proposition juste", "proposition fausse 1", "proposition fausse 2"];
var q1=["id01","Question","réponse complète", a1];

var vf1=["id001","Question","réponse complète", 1];


var q2=['d','e','f'];
var q3=['g','h','i'];

var liste=[q1,q2,q3];



//shuffle(liste);

var i;
for (i = 0; i < liste.length; i++) {
    var tab1=[`<button onclick="document.getElementById('`+liste[i][0]+`').
    style.display='block'" class="w3-button w3-dark-grey w3-large">`, liste[i][3][0]];

    var tab2=[`<button onclick="document.getElementById('f0').
    style.display='block'" class="w3-button w3-dark-grey w3-large">`, liste[i][3][1]];
    
    var tab3=[`<button onclick="document.getElementById('f0').
    style.display='block'" class="w3-button w3-dark-grey w3-large">`, liste[i][3][2]];

    var tableau=[tab1,tab2,tab3];
    
    shuffle(tableau);
    
    document.write(`

    `);






    document.write(`
        <div class="w3-third w3-orange" style="margin-left:11.333%; margin-top:5%; height:42%">
            <center><h4><b>`+liste[i][1]+`</b></h4></center><br>
            <div style="margin-bottom:1%; margin-left:1%">
                `+tableau[0][0]+`A.</button> 
                `+tableau[0][1]+`<br>
            </div>
            <div style="margin-bottom:1%; margin-left:1%">
                `+tableau[1][0]+`B.</button> 
                `+tableau[1][1]+`<br>
            </div>
            <div style="margin-bottom:1%; margin-left:1%">
                `+tableau[2][0]+`C.</button> 
                `+tableau[2][1]+`<br>
            </div>
        </div>`)
} 


function shuffle(array) {
    var currentIndex = array.length, temporaryValue, randomIndex;
  
    // While there remain elements to shuffle...
    while (0 !== currentIndex) {
  
      // Pick a remaining element...
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex -= 1;
  
      // And swap it with the current element.
      temporaryValue = array[currentIndex];
      array[currentIndex] = array[randomIndex];
      array[randomIndex] = temporaryValue;
    }
  
    return array;
  }
  
  // Used like so
  var arr = [2, 11, 37, 42];
  shuffle(arr);
  console.log(arr);
