var q1=["a","b","c"];
var q2=['d','e','f'];
var q3=['g','h','i'];

var liste=[q1,q2,q3];

shuffle(liste);

var i,j;
for (i = 0; i < q1.length; i++) {
    for (j = 0; j < liste.length; j++) {
        document.write(liste[i][j] + "<br>");
    } 
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
