import connectExpandAndCollapseButtonsToListsOfDoculects from "./tools/connectExpandAndCollapseButtonsToListsOfDoculects.js";

function setUpExpandCollapseContainerInInteractiveList() {
  {
    const markerGroups = document.querySelectorAll(
      "ul.doculects-in-group.w3-ul.w3-hide"
    );

    // even when DOM content is loaded and this function is called, data may still not have been fetched yet
    if (markerGroups.length === 0) {
      setTimeout(setUpExpandCollapseContainerInInteractiveList, 100);
    }

    connectExpandAndCollapseButtonsToListsOfDoculects();

    const expandCollapseContainer = document.getElementById(
      "doculect-list-expand-collapse-container"
    );
    const listContainer = document.getElementById("interactive-list");
    if (listContainer != null) listContainer.prepend(expandCollapseContainer);
  }
}

/* This script is imported in a parent Jinja template,
so including it without eventListener will cause it to run
while the child template is still not fully rendered.
*/
window.addEventListener(
  "DOMContentLoaded",
  setUpExpandCollapseContainerInInteractiveList
);
