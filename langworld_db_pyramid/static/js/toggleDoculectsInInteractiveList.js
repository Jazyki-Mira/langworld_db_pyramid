/* This script is imported in a parent Jinja template,
so including it without eventListener for "load" will cause it to run
while the child template is still not fully rendered.

I use .addEventListener instead of .onload to allow potential multiple
actions after window is loaded.
*/

window.addEventListener("load", () => {
  const toggleSwitch = document.getElementById("doculects-in-list-toggle");

  toggleSwitch.onclick = () => {
    // cannot just toggle because the user may have expanded/collapsed individual groups
    if (toggleSwitch.checked) {
      for (let ul of document.querySelectorAll("ul.doculects-in-group")) {
        ul.classList.add("w3-hide");
      }
    } else {
      for (let ul of document.querySelectorAll("ul.doculects-in-group")) {
        ul.classList.remove("w3-hide");
      }
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
  const toggleBackOnLoad = () => {
    if (toggleSwitch.checked === true) toggleSwitch.click();
  };

  setTimeout(toggleBackOnLoad, 10);
  /* Without the timeout Chrome will think that the switch is OFF
  and then turn it ON after a fraction of a second.
  Turns out that even with a ZERO timeout Chrome will recognize the switch is ON at pageload,
  but I put 10 milliseconds just in case.
  */
});
