let allMarkers = [];

const fetchDataAndAddMarkersToMap = (doculectMap, urlParams) => {
  removeMarkers(doculectMap);

  fetch(urlParams.urlToFetch)
    .then((res) => res.json())
    .then((doculects) => addMarkers(doculects, doculectMap, urlParams))
    .catch(console.error);
};

const removeMarkers = (doculectMap) => {
  for (let marker of allMarkers) doculectMap.removeLayer(marker);
};

const addMarkers = (doculects, doculectMap, { idOfDoculectToShow }) => {
  for (let doculect of doculects) {
    let iconSize = [
      parseInt(doculect["divIconSize"][0]),
      parseInt(doculect["divIconSize"][1]),
    ];
    let iconAnchor = [iconSize[0] / 2, iconSize[1] / 2];

    const icon = L.divIcon({
      html: doculect["divIconHTML"],
      className: "",
      iconSize: iconSize,
      iconAnchor: iconAnchor,
    });

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
  }

  // after all markers were added, fit map to see them all
  let featureGroup = L.featureGroup(allMarkers);
  doculectMap.fitBounds(featureGroup.getBounds(), {
    maxZoom: 13,
    padding: [10, 25],
  });
};

export default fetchDataAndAddMarkersToMap;
