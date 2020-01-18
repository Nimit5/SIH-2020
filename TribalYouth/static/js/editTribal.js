let skillBtn=document.getElementById("skills");
let skillPopup=document.getElementById("skillPopup");

let span = document.getElementsByClassName("close")[0];   // for closing

// When the user clicks on the button skills, open the modal
skillBtn.onclick = function() {
  skillPopup.style.display = "block";
}

  
// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  skillPopup.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == skillPopup) {
    skillPopup.style.display = "none";
  }
}
