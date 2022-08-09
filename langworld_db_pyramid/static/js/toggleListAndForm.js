const formDiv = document.getElementById("query-wizard-form");
const listDiv = document.getElementById("interactive-list");
const toggleSwitch = document.getElementById("form-list-toggle");

toggleSwitch.onclick = () => {
  formDiv.classList.toggle("w3-hide");
  listDiv.classList.toggle("w3-hide");
};
