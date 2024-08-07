import hideExpandCollapseContainer from "./tools/hideExpandCollapseContainer.js";
import renderMapWithList from "./tools/renderMapWithList.js";

renderMapWithList("all");

// FIXME this only works after Ctrl+F5
// using event listener, otherwise it will run while the template is still not fully rendered
window.addEventListener("load", () => {

  // default behavior of list is to have all items collapsed. Here it's better to have them expanded
  const markerGroups = document.querySelectorAll(
    "ul.doculects-in-group.w3-ul.w3-hide"
  );

  markerGroups.forEach((ul) => {
    console.log(ul.classList);
    ul.classList.remove("w3-hide");
  });

  // There is only one group of doculects, so "expand/collapse" buttons are not needed.
  hideExpandCollapseContainer();
});
