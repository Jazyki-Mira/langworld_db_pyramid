const toggleSwitch = document.getElementById("doculects-in-list-toggle");

toggleSwitch.onclick = () => {
  for (let ul of document.querySelectorAll("ul.doculects-in-group")) {
    ul.classList.toggle("w3-hide");
  }
};

const toggleSwitchContainer = document.getElementById(
  "doculects-in-list-toggle-container"
);
const listContainer = document.getElementById("interactive-list");
listContainer.prepend(toggleSwitchContainer);
