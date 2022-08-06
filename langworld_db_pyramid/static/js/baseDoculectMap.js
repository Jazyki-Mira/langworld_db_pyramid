import accessToken from "./mapboxAccessToken.js";
import { doculectGroupsContext } from "./contexts.js";
import getURLParams from "./getURLParams.js";

const elem = React.createElement;

export default function DoculectMap({ mapDivID }) {
  const leafletFeatureGroupsRef = React.useRef([]);
  const mapRef = React.useRef(null);

  const { mapViewLat, mapViewLong, zoom, idOfDoculectToShow } = getURLParams();
  const markerForDoculectID = new Map();

  const { doculectGroups } = React.useContext(doculectGroupsContext);

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

  React.useEffect(() => {
    if (doculectGroups === null) return;
    removeExistingMarkersAndFeatureGroups();
    createFeatureGroups();

    addGroupsOfMarkersToMap();
    zoomMapToFitAllMarkers(); // note that the map will not move if zoom doesn't need to change
    openPopupForDoculect(idOfDoculectToShow);
  }, [doculectGroups]);

  const removeExistingMarkersAndFeatureGroups = () => {
    leafletFeatureGroupsRef.current.forEach((group) => group.clearLayers());
    leafletFeatureGroupsRef.current = [];
  };

  const createFeatureGroups = () => {
    for (let group of doculectGroups) {
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

      leafletFeatureGroupsRef.current.push(
        createFeatureGroup(group["markers"], icon)
      );
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
    leafletFeatureGroupsRef.current.forEach((featureGroup) =>
      featureGroup.addTo(mapRef.current)
    );
  };

  const openPopupForDoculect = (doculectID) => {
    if (doculectID != null) markerForDoculectID[doculectID].openPopup();
  };

  const zoomMapToFitAllMarkers = () => {
    let allMarkers = [];
    leafletFeatureGroupsRef.current.forEach((group) => {
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
