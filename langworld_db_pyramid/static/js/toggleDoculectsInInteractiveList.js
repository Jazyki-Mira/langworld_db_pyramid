const toggleSwitch = document.getElementById("doculects-in-list-toggle");

toggleSwitch.onclick = () => {
  for (let ul of document.querySelectorAll("ul.doculects-in-group")) {
    ul.classList.toggle("w3-hide");
  }

  for (let heading of document.querySelectorAll("p.legend-heading")) {
    heading.classList.toggle("w3-large");
    heading.classList.toggle("w3-medium");
  }
};

const toggleSwitchContainer = document.getElementById(
  "doculects-in-list-toggle-container"
);
const listContainer = document.getElementById("interactive-list");
listContainer.prepend(toggleSwitchContainer);
