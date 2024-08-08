function getMarkerGroupsFromDOM() {
  return document.querySelectorAll("ul.doculects-in-group.w3-ul.w3-hide");
}

export default function getMarkerGroupsWhenRendered() {
  // repeatedly tries to get marker groups from document until they are rendered
  let groups = getMarkerGroupsFromDOM();
  if (groups.length === 0) {
    setTimeout(getMarkerGroupsWhenRendered, 100);
  }
  // console.log("Marker groups loaded");
  return groups;
}
