export default function connectExpandAndCollapseButtonsToListsOfDoculects() {
  /* Update "expand all/collapse all" buttons by linking them
     to <ul>'s actually present in the DOM.
  */

  const subListsOfDoculects = document.querySelectorAll(
    "ul.doculects-in-group.w3-ul"
  );

  const expandAllButton = document.getElementById(
    "doculect-list-expand-all-button"
  );
  const collapseAllButton = document.getElementById(
    "doculect-list-collapse-all-button"
  );

  expandAllButton.onclick = () => {
    subListsOfDoculects.forEach((ul) => {
      ul.classList.remove("w3-hide");
    });
  };

  collapseAllButton.onclick = () => {
    subListsOfDoculects.forEach((ul) => {
      ul.classList.add("w3-hide");
    });
  };
}
