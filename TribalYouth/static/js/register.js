// yeh pop up window khulne ke liye hai (model)

let modal = document.getElementById("myModal"); // kya khulega

// Get the button that opens the modal
let btn = document.getElementById("myBtn"); // kise khulega

// Get the <span> element that closes the modal
let span = document.getElementsByClassName("close")[0];   // for closing

// When the user clicks on the button user tribe, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

  
// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

// get button for nav. register
let navbtn = document.getElementById("navbtn");

// When the user clicks on the navigation bar button to Register, open the modal
navbtn.onclick = function() {
  modal.style.display = "block";
  document.getElementById("signup").style.display="block";
  document.getElementById("login").style.display="none";
}


/* Function for tabs for login or signup */
function openCity(evt, type) {
  let i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(type).style.display = "block";
  evt.currentTarget.className += " active";
}

/* Function for differnt register windows */
//let tribalBtn=document.getElementById("Tribal");
// Function for handling tab under tab for signup of tribal and proffesor

function openInnerTab(evt, type) {
  let i, innertab, tabimg;
  innertab = document.getElementsByClassName("innertab");
  for (i = 0; i < innertab.length; i++) {
    innertab[i].style.display = "none";
  }
  tabimg = document.getElementsByClassName("tabimg");
  for (i = 0; i < tabimg.length; i++) {
    tabimg[i].className = tabimg[i].className.replace(" active", "");
  }
  document.getElementById(type).style.display = "block";
  evt.currentTarget.className += " active";
}