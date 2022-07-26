const fetchDataAndAddMarkersToMap = (doculectMap, urlParams) => {
  fetch(urlParams.urlToFetch)
    .then((res) => res.json())
    .then((doculects) => addMarkers(doculects, doculectMap, urlParams))
    .catch(console.error);
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

    if (doculect["id"] === idOfDoculectToShow) marker.openPopup();
  }
};

export default fetchDataAndAddMarkersToMap;
