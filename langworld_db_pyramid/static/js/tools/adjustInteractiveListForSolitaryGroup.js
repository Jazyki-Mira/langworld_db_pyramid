/* If interactive list has only one group of doculects:
   1. the only group of doculects can be expanded right away,
      contrary to default behavior of having doculect groups collapsed
   2. "expand/collapse" buttons are not needed.
*/

export default function adjustInteractiveListForSolitaryGroup() {

  // 1. expand the only group of doculects
  const group = document.querySelector("ul.doculects-in-group.w3-ul.w3-hide");
  // make sure group is ready (it may take a while to fetch data)
  if (group === null) {
    setTimeout(adjustInteractiveListForSolitaryGroup, 100);
  } else {
    /* the following could be outside of braces,
       but it would trigger error in console while group is null
    */
    group.classList.remove("w3-hide");

    // 2. hide expand/collapse buttons
    document
      .getElementById("doculect-list-expand-collapse-container")
      .classList.add("w3-hide");
  }
}
