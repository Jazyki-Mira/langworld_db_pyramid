import hideExpandCollapseContainer from "./tools/hideExpandCollapseContainer.js";
import renderMapWithList from "./tools/renderMapWithList.js";

renderMapWithList("all");

/* using event listener to wait for DOM the template to be rendered
PLUS a timeout to wait for data to be loaded and <ul>'s to be created.
Returning a promise from `renderMapWithList` and using `.then()` on it doesn't work: 
throws `<name of promise> is undefined`.
TODO: maybe some changes could be made to `renderMapWithList()`
*/
window.addEventListener("DOMContentLoaded", () => {
  setTimeout(() => {
    // default behavior of list is to have all items collapsed. Here it's better to have them expanded
    const markerGroups = document.querySelectorAll(
      "ul.doculects-in-group.w3-ul.w3-hide"
    );

    markerGroups.forEach((ul) => {
      ul.classList.remove("w3-hide");
    });

    // There is only one group of doculects, so "expand/collapse" buttons are not needed.
    hideExpandCollapseContainer();
  }, 750);
});
