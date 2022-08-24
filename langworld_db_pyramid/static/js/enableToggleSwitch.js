export default function enableToggleSwitch(
  idOfSwitch,
  idOfInitiallyVisibleDiv,
  idOfInitiallyHiddenDiv
) {
  const toggleSwitch = document.getElementById(idOfSwitch);
  const initiallyHiddenDiv = document.getElementById(idOfInitiallyHiddenDiv);
  const initiallyVisibleDiv = document.getElementById(idOfInitiallyVisibleDiv);
  const nameOfHiddenClass = "w3-hide";

  const toggleVisibility = (elements) => {
    elements.map((div) => {
      div.classList.toggle(nameOfHiddenClass);
    });
  };

  toggleSwitch.onclick = () =>
    toggleVisibility([initiallyHiddenDiv, initiallyVisibleDiv]);

  /* In Chrome, when user goes back to the page where the switch had been on,
  the switch remains on but the <div> that had been hidden and was made visible
  by the switch is hidden again.

  In Firefox, same thing happens if the switch is turned ON and then the page is reloaded.

  To prevent this, I have to check the position of switch at page load and switch
  the visibility of div's if the switch is ON.
  */

  window.addEventListener("load", () => {
    if (toggleSwitch.checked === true)
      toggleVisibility([initiallyHiddenDiv, initiallyVisibleDiv]);
  });
}
