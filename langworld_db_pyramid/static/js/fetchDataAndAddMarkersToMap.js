let allMarkers = [];

const fetchDataAndAddMarkersToMap = (doculectMap, urlParams) => {
  removeMarkers(doculectMap);

  fetch(urlParams.urlToFetch)
    .then((res) => res.json())
    .then((groupsOfDoculects) =>
      addMarkers(groupsOfDoculects, doculectMap, urlParams)
    )
    .catch(console.error);
};

const removeMarkers = (doculectMap) => {
  for (let marker of allMarkers) doculectMap.removeLayer(marker);
};

const addMarkers = (groupsOfDoculects, doculectMap, { idOfDoculectToShow }) => {
  console.log(groupsOfDoculects);
  for (let group of groupsOfDoculects) {
    let iconSize = [
      parseInt(group["divIconSize"][0]),
      parseInt(group["divIconSize"][1]),
    ];
    let iconAnchor = [iconSize[0] / 2, iconSize[1] / 2];

    const icon = L.divIcon({
      html: group["divIconHTML"],
      className: "",
      iconSize: iconSize,
      iconAnchor: iconAnchor,
    });

    addMarkersForOneGroup(
      group["doculects"],
      doculectMap,
      icon,
      idOfDoculectToShow
    );
  }

  // after all markers were added, fit map to see them all
  let featureGroup = L.featureGroup(allMarkers);
  doculectMap.fitBounds(featureGroup.getBounds(), {
    maxZoom: 13,
    padding: [10, 25],
  });
};

const addMarkersForOneGroup = (
  doculects,
  doculectMap,
  icon,
  idOfDoculectToShow
) => {
  doculects.forEach((doculect) => {
    let marker = L.marker([doculect["latitude"], doculect["longitude"]], {
      icon: icon,
      riseOnHover: true,
    }).addTo(doculectMap);

    marker.bindPopup(doculect["popupText"]);
    marker.on("mouseover", function (e) {
      this.openPopup();
    });
    marker.on("click", function (e) {
      window.open(doculect["url"], "_self");
    });

    allMarkers.push(marker);

    if (doculect["id"] === idOfDoculectToShow) marker.openPopup();
  });
};

export default fetchDataAndAddMarkersToMap;
