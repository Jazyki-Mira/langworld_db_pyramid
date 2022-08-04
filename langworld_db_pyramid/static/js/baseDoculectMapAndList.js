import accessToken from "./mapboxAccessToken.js";

export default function MapAndList({ mapDivID, urlToFetch }) {
  const elem = React.createElement;

  const markerForDoculectID = new Map();
  const mapRef = React.useRef(null);

  const getURLParams = () => {
    let urlParams = new URLSearchParams(location.search);

    /* these 3 can be connected (center on a specific doculect),
      but I want to keep the functionality flexible and be able to center on something
      without necessarily showing the doculect */
    let idOfDoculectToShow = urlParams.has("show_doculect")
      ? urlParams.get("show_doculect")
      : null;
    let mapViewLat = urlParams.has("lat")
      ? parseInt(urlParams.get("lat"))
      : 55.0;
    let mapViewLong = urlParams.has("long")
      ? parseInt(urlParams.get("long"))
      : 95.0;

    let zoom = 2.5;

    return { idOfDoculectToShow, mapViewLat, mapViewLong, zoom };
  };

  const { mapViewLat, mapViewLong, zoom, idOfDoculectToShow } = getURLParams();

  // map base (rendered once, hence empty dependency array)
  React.useEffect(() => {
    mapRef.current = L.map(mapDivID).setView([mapViewLat, mapViewLong], zoom);

    const titleLayerUrl =
      "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=" +
      accessToken;

    L.tileLayer(titleLayerUrl, {
      attribution:
        'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
      maxZoom: 18,
      id: "mapbox/streets-v11",
      tileSize: 512,
      zoomOffset: -1,
      accessToken: accessToken,
      minZoom: 2.5, // 2 will show all languages but will be too small
    }).addTo(mapRef.current);
  }, []);

  const featureGroupsRef = React.useRef([]);

  React.useEffect(() => {
    fetch(urlToFetch)
      .then((res) => res.json())
      .then((groupsOfDoculects) => {
        removeExistingMarkersAndFeatureGroups();
        createFeatureGroups(groupsOfDoculects);
      })
      .then(() => {
        addGroupsOfMarkersToMap();
        zoomMapToFitAllMarkers(); // note that the map will not move if zoom doesn't need to change
        openPopupForDoculect(idOfDoculectToShow);
      })
      .catch(console.error);
  }, [urlToFetch]);

  const removeExistingMarkersAndFeatureGroups = () => {
    featureGroupsRef.current.forEach((group) => group.clearLayers());
    featureGroupsRef.current = [];
  };

  const createFeatureGroups = (groupsOfDoculects) => {
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

      featureGroupsRef.current.push(createFeatureGroup(group["markers"], icon));
    }
  };

  const createFeatureGroup = (doculectsInThisGroup, icon) => {
    let markersInThisGroup = [];

    doculectsInThisGroup.forEach((doculect) => {
      let marker = L.marker([doculect["latitude"], doculect["longitude"]], {
        icon: icon,
        riseOnHover: true,
      });

      marker.bindPopup(doculect["popupText"]);
      marker.on("mouseover", function (e) {
        this.openPopup();
      });
      marker.on("click", function (e) {
        window.open(doculect["url"], "_self");
      });

      markersInThisGroup.push(marker);
      markerForDoculectID[doculect["id"]] = marker;
    });

    return L.featureGroup(markersInThisGroup);
  };

  const addGroupsOfMarkersToMap = () => {
    featureGroupsRef.current.forEach((featureGroup) =>
      featureGroup.addTo(mapRef.current)
    );
  };

  const openPopupForDoculect = (doculectID) => {
    if (doculectID != null) markerForDoculectID[doculectID].openPopup();
  };

  const zoomMapToFitAllMarkers = () => {
    let allMarkers = [];
    featureGroupsRef.current.forEach((group) => {
      group.eachLayer((marker) => allMarkers.push(marker));
    });

    let groupOfAllMarkers = L.featureGroup(allMarkers);

    mapRef.current.fitBounds(groupOfAllMarkers.getBounds(), {
      maxZoom: 13,
      padding: [10, 25],
    });
  };

  return elem("div", { id: mapDivID });
}
