/* If there is always only one group of doculects,
the "doculect list / legend only" switch is not needed and can be hidden.
I wait for the page to load because the switch may be contained in a parent template.
*/
export default function hideListAndLegendToggleSwitch() {
  window.addEventListener("load", () =>
    document
      .getElementById("doculects-in-list-toggle-container")
      .classList.add("w3-hide")
  );
}
