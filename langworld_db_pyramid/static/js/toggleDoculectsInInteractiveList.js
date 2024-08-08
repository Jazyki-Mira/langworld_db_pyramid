/* This script is imported in a parent Jinja template,
so including it without eventListener will cause it to run
while the child template is still not fully rendered.
*/

function setUpExpandCollapseContainer() {
  {
    const markerGroups = document.querySelectorAll(
      "ul.doculects-in-group.w3-ul.w3-hide"
    );

    // even when DOM content is loaded and this function is called, data may still not have been fetched yet
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
