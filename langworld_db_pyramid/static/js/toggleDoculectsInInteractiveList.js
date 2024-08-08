import getMarkerGroupsWhenRendered from "./tools/getMarkerGroupsWhenRendered.js";

/* This script is imported in a parent Jinja template,
so including it without eventListener will cause it to run
while the child template is still not fully rendered.
*/

function setUpExpandCollapseContainer() {
  {
    // even when DOM content is loaded, data still hasn't been fetched yet
    let markerGroups = getMarkerGroupsWhenRendered();

    if (markerGroups.length === 0) {
      setTimeout(setUpExpandCollapseContainer, 100);
    }

    const expandAllButton = document.getElementById(
      "doculect-list-expand-all-button"
    );
    const collapseAllButton = document.getElementById(
      "doculect-list-collapse-all-button"
    );

    expandAllButton.onclick = () => {
      markerGroups.forEach((ul) => {
        ul.classList.remove("w3-hide");
      });
    };

    collapseAllButton.onclick = () => {
      markerGroups.forEach((ul) => {
        ul.classList.add("w3-hide");
      });
    };

    const expandCollapseContainer = document.getElementById(
      "doculect-list-expand-collapse-container"
    );
    const listContainer = document.getElementById("interactive-list");
    if (listContainer != null) listContainer.prepend(expandCollapseContainer);
  }
}

window.addEventListener("DOMContentLoaded", setUpExpandCollapseContainer);
