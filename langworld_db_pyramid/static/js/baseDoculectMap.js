import accessToken from "./mapboxAccessToken.js";
import {
  allFetchedDoculectGroupsContext,
  doculectGroupsInMapViewContext,
  idOfDoculectToOpenPopupOnMapContext,
} from "./contexts.js";
import getURLParams from "./getURLParams.js";

const elem = React.createElement;

export default function DoculectMap({ mapDivID }) {
  const leafletFeatureGroupsRef = React.useRef([]);
  const mapRef = React.useRef(null);

  const { mapViewLat, mapViewLong, zoom, idOfDoculectToShow } = getURLParams();
  const markerForDoculectIDRef = React.useRef(new Map());

  const { allDoculectGroups } = React.useContext(
    allFetchedDoculectGroupsContext
  );
  const { setDoculectGroupsInMapView } = React.useContext(
    doculectGroupsInMapViewContext
  );
  const { idOfDoculectToOpenPopupOnMap } = React.useContext(
    idOfDoculectToOpenPopupOnMapContext
  );

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
    if (allDoculectGroups === null) return;
    removeExistingMarkersAndFeatureGroups();
    createFeatureGroups();

    addGroupsOfMarkersToMap();
    setDoculectGroupsInMapView(getGroupsInMapView());
    zoomMapToFitAllMarkers(); // note that the map will not move if zoom doesn't need to change
    openPopupForDoculect(idOfDoculectToShow);

    mapRef.current.on("zoomend moveend", () => {
      // only change context, the list rendering is called from parent
      setDoculectGroupsInMapView(getGroupsInMapView());
    });
  }, [allDoculectGroups]);

  // open pop-up if ID of language to pop up changes
  React.useEffect(() => {
    if (idOfDoculectToOpenPopupOnMap === null) {
      mapRef.current.closePopup();
    } else {
      openPopupForDoculect(idOfDoculectToOpenPopupOnMap);
    }
  }, [idOfDoculectToOpenPopupOnMap]);

  const removeExistingMarkersAndFeatureGroups = () => {
    leafletFeatureGroupsRef.current.forEach((group) => group.clearLayers());
    leafletFeatureGroupsRef.current = [];
  };

  const createFeatureGroups = () => {
    for (let group of allDoculectGroups) {
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
      markerForDoculectIDRef.current[doculect["id"]] = marker;
    });

    return L.featureGroup(markersInThisGroup);
  };

  const addGroupsOfMarkersToMap = () => {
    leafletFeatureGroupsRef.current.forEach((featureGroup) =>
      featureGroup.addTo(mapRef.current)
    );
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

  const openPopupForDoculect = (doculectID) => {
    if (doculectID != null) {
      let marker = markerForDoculectIDRef.current[doculectID];
      marker.openPopup();
      marker.fire("mouseover"); // to make the marker rise to the top
      // TODO if user returns to the same list item, the marker will not rise again
      // I guess I have to trigger "mouseout" on PREVIOUS marker when ID changes
    }
  };

  const getGroupsInMapView = () => {
    let groupsInMapView = [];

    for (let group of allDoculectGroups) {
      // Make a copy of the group but without doculects.
      let copiedGroup = { ...group };
      copiedGroup["markers"] = [];

      // Add (from the original group) doculects that are in current map view.
      for (let doculect of group["markers"]) {
        let marker = markerForDoculectIDRef.current[doculect["id"]];
        if (mapRef.current.getBounds().contains(marker.getLatLng())) {
          copiedGroup["markers"].push(doculect);
        }
      }

      // If copied group turns out to have doculects, add to list of groups to be returned.
      if (copiedGroup["markers"].length > 0) groupsInMapView.push(copiedGroup);
    }

    return groupsInMapView;
  };

  return elem("div", { id: mapDivID });
}
