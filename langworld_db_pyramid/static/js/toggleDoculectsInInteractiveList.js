/* This script is imported in a parent Jinja template,
so including it without eventListener for "load" will cause it to run
while the child template is still not fully rendered.

I use .addEventListener instead of .onload to allow potential multiple
actions after window is loaded.
*/

window.addEventListener("load", () => {
  const toggleSwitch = document.getElementById("doculects-in-list-toggle");

  toggleSwitch.onclick = () => {
    for (let ul of document.querySelectorAll("ul.doculects-in-group")) {
      ul.classList.toggle("w3-hide");
    }

    for (let heading of document.querySelectorAll("p.legend-heading")) {
      heading.classList.toggle("w3-large");
      heading.classList.toggle("w3-medium");
    }
  };

  const toggleSwitchContainer = document.getElementById(
    "doculects-in-list-toggle-container"
  );
  const listContainer = document.getElementById("interactive-list");
  listContainer.prepend(toggleSwitchContainer);

  /* If the switch is ON at pageload (and this is only possible at Refresh in Firefox 
  and after clicking Back in Chrome), reset the switch back to OFF.
  No other actions are needed because the data is being fetched and there are no containers
  with data to hide/show.
  */
  if (toggleSwitch.checked === true) toggleSwitch.click();
});
