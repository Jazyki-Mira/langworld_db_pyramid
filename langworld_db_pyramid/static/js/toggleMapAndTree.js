const mapAndListDiv = document.getElementById("map-and-list");
const toggleSwitch = document.getElementById("map-tree-toggle");
const treeDiv = document.getElementById("tree");

toggleSwitch.onclick = () => {
  mapAndListDiv.classList.toggle("w3-hide");
  treeDiv.classList.toggle("w3-hide");
};
