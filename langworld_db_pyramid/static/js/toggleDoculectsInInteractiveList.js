/* This script is imported in a parent Jinja template,
so including it without eventListener for "load" will cause it to run
while the child template is still not fully rendered.

I use .addEventListener instead of .onload to allow potential multiple
actions after window is loaded.
*/

window.addEventListener("load", () => {
  const expandAllButton = document.getElementById(
    "doculect-list-expand-all-button"
  );
  const collapseAllButton = document.getElementById(
    "doculect-list-collapse-all-button"
  );
  const markerGroups = document.querySelectorAll(
    "ul.doculects-in-group.w3-ul.w3-hide"
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
});
