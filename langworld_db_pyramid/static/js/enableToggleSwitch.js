export default function enableToggleSwitch(idOfSwitch, IdsOfDivsToToggle) {
  const toggleSwitch = document.getElementById(idOfSwitch);

  toggleSwitch.onclick = () =>
    IdsOfDivsToToggle.map((divId) => {
      document.getElementById(divId).classList.toggle("w3-hide");
    });
}
