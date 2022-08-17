const alphabeticDiv = document.getElementById("alphabetic");
const byVolumeDiv = document.getElementById("by-volume");
const toggleSwitch = document.getElementById("alphabetic-or-by-volume-toggle");

toggleSwitch.onclick = () => {
  alphabeticDiv.classList.toggle("w3-hide");
  byVolumeDiv.classList.toggle("w3-hide");
};
