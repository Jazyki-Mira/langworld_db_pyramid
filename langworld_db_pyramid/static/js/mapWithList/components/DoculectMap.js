import {
  allFetchedDoculectGroupsContext,
  doculectGroupsInMapViewContext,
  idOfDoculectToOpenPopupOnMapContext,
} from "../contexts.js";
import adjustInteractiveListForSolitaryGroup from "../../tools/adjustInteractiveListForSolitaryGroup.js";
import connectExpandAndCollapseButtonsWithGroups from "../../tools/connectExpandAndCollapseButtonsToListsOfDoculects.js";
import {compoundValueSeparator} from "../../constants/literals.js";

const elem = React.createElement;

export default function DoculectMap({ mapDivID = "map-default" }) {
  const leafletFeatureGroupsRef = React.useRef([]); // "featureGroup" in terms of Leaflet, not database
  const mapRef = React.useRef(null);
  const selectedMarker = React.useRef(null);

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

  const [mapboxToken, setMapboxToken] = React.useState(null);
  const [mapLoaded, setMapLoaded] = React.useState(false);

  const opacityForUnfocusedDoculects = 0.3;

  if (mapboxToken === null) {
    fetch("/json_api/mapbox_token")
      .then((res) => res.json())
      .then(setMapboxToken)
      .catch(console.error);
  }

  React.useEffect(() => {
    if (mapboxToken === null) return null;

    mapRef.current = L.map(mapDivID).setView([mapViewLat, mapViewLong], zoom);

    const titleLayerUrl =
      "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=" +
      mapboxToken;

    L.tileLayer(titleLayerUrl, {
      attribution:
        'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
      maxZoom: 18,
      id: "mapbox/streets-v11",
      tileSize: 512,
      zoomOffset: -1,
      accessToken: mapboxToken,
      minZoom: 2,
    }).addTo(mapRef.current);

    setMapLoaded(true);
  }, [mapboxToken]); // map will be loaded once mapBox token is fetched

  React.useEffect(() => {
    if (
      allDoculectGroups === null ||
      mapRef.current === null ||
      mapLoaded === false
    )
      return null;
    removeExistingMarkersAndFeatureGroups();
    createFeatureGroups();

    addGroupsOfMarkersToMap();
    addLegend();
    if (
      allDoculectGroups.length > 1 ||
      allDoculectGroups[0]["doculects"].length > 0
    )
      zoomMapToFitAllMarkers(); // note that the map will not move if zoom doesn't need to change

    setDoculectGroupsInMapView(getGroupsInMapView());

    /* Motivation for setTimeout()
       If user opens the map from a doculect profile, it is likely that their mouse will
       end up pointing at a random doculect on the map, thus triggering its popup to open.
       This is because of the position of the link to the map in doculect profiles.
       This means that the user will not see the popup for the doculect they were meant to see.
       Adding the timeout leads to the following chain of events:
       1. A popup opens for a doculect that user's mouse is pointing at,
       2. after 0.5 seconds a popup opens for the correct doculect (closing the previous one).
          Timeout of less than 0.5 seconds might not be enough for the map to show the popup for
          the random doculect the user's mouse is pointing at.
     */
    setTimeout(() => {
      changeIconForDoculectToShow(idOfDoculectToShow);
      openPopupForDoculect(idOfDoculectToShow);
    }, 500);

    mapRef.current.on("zoomend moveend", () => {
      // only change context, the list rendering is called from parent
      setDoculectGroupsInMapView(getGroupsInMapView());

      /* Reconnect "expand all" / "collapse all" buttons with all marker groups
         currently in view.
         This has to be done every time the set of marker groups changes.
         Instead of checking whether the groups have changed (which will complicate the code),
         we just do it every time after zooming/moving has occurred.
      */
      connectExpandAndCollapseButtonsWithGroups();

      /* If this map is meant to show only one group of doculects (e.g. all doculects, query wizard)
         and the preceding zooming in had made it disappear,
         properties of the interactive list must be restored after zooming out again.
      */
      if (allDoculectGroups.length === 1)
        adjustInteractiveListForSolitaryGroup();
    });
  }, [allDoculectGroups, mapLoaded]);

  // open pop-up if ID of language to pop-up changes
  React.useEffect(() => {
    if (mapRef.current === null || mapLoaded === false) return null;

    if (idOfDoculectToOpenPopupOnMap === null) {
      mapRef.current.closePopup();
      // restore focus on doculect to show (that was indicated in URL)
      if (idOfDoculectToShow != null) {
        selectedMarker.current.setOpacity(opacityForUnfocusedDoculects);
        markerForDoculectIDRef.current[idOfDoculectToShow].openPopup();
        changeIconForDoculectToShow(idOfDoculectToShow);
      }
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
        createFeatureGroup(group["doculects"], icon)
      );
    }
  };

  const createFeatureGroup = (doculectsInThisGroup, icon) => {
    let markersInThisGroup = [];

    doculectsInThisGroup.forEach((doculect) => {
      let marker = L.marker([doculect["latitude"], doculect["longitude"]], {
        icon: icon,
        riseOnHover: true,
        // if one doculect is to be highlighted, make all markers transparent by default:
        opacity: idOfDoculectToShow == null ? 1 : opacityForUnfocusedDoculects,
      });

      marker.bindPopup(doculect["popupText"]);
      marker.on("mouseover", function (e) {
        if (selectedMarker.current != null)
          selectedMarker.current.fire("mouseout");
        this.setOpacity(1);
        this.openPopup();
        // keep opacity on the doculect that was in focus when page loaded
        if (idOfDoculectToShow != null)
          markerForDoculectIDRef.current[idOfDoculectToShow].setOpacity(1);
      });
      marker.on("mouseout", function (e) {
        /* If marker corresponds to the doculect that needs to stay in focus,
           don't do anything: it has to remain opaque and with pop-up open
        */
        if (
          marker == markerForDoculectIDRef.current[idOfDoculectToShow] &&
          idOfDoculectToShow != null
        )
          return null;

        this.closePopup();
        this.setOpacity(
          idOfDoculectToShow == null ? 1 : opacityForUnfocusedDoculects
        );
        if (idOfDoculectToShow != null)
          markerForDoculectIDRef.current[idOfDoculectToShow].openPopup();
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
    /* Compound values will be added to map after elementary ones,
       which means that pie markers will simply cover the circles.
       This is exactly what we need.
    */
    leafletFeatureGroupsRef.current.forEach((group) =>
      group.addTo(mapRef.current)
    );
  };

  const addLegend = () => {
    // legend not needed if this map is only intended to show a single group of doculects
    if (allDoculectGroups.length === 1) return null;

    let legend = L.control({ position: "bottomright" });

    legend.onAdd = () => {
      let div = L.DomUtil.create("div", "legend");

      // exclude compound values from legend
      allDoculectGroups
        .filter((g) => !g["id"].includes(compoundValueSeparator))
        .forEach((group) => {
          div.innerHTML += `<img src="${group["imgSrc"]}" height="20px"/><span>${group["name"]}</span><br>`;
        });
      return div;
    };

    legend.addTo(mapRef.current);
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

  const changeIconForDoculectToShow = (doculectID) => {
    if (doculectID === null) return null;

    const marker = markerForDoculectIDRef.current[doculectID];
    marker.setOpacity(1);
    marker.setZIndexOffset(1000);
  };

  const openPopupForDoculect = (doculectID) => {
    if (doculectID === null) return null;

    if (selectedMarker.current != null) selectedMarker.current.fire("mouseout");

    selectedMarker.current = markerForDoculectIDRef.current[doculectID];
    selectedMarker.current.fire("mouseover");
  };

  const getGroupsInMapView = () => {
    let groupsInMapView = [];

    for (let group of allDoculectGroups) {
      // Make a copy of the group but without doculects.
      let copiedGroup = { ...group };
      copiedGroup["doculects"] = [];

      // Add (from the original group) doculects that are in current map view.
      for (let doculect of group["doculects"]) {
        let marker = markerForDoculectIDRef.current[doculect["id"]];
        if (mapRef.current.getBounds().contains(marker.getLatLng())) {
          copiedGroup["doculects"].push(doculect);
        }
      }

      // If copied group turns out to have doculects, add to list of groups to be returned.
      if (copiedGroup["doculects"].length > 0)
        groupsInMapView.push(copiedGroup);
    }

    return groupsInMapView;
  };

  return elem("div", { id: mapDivID });
}

function getURLParams() {
  let urlParams = new URLSearchParams(location.search);

  /* these 3 can be connected (center on a specific doculect),
      but I want to keep the functionality flexible and be able to center on something
      without necessarily showing the doculect */
  let idOfDoculectToShow = urlParams.has("show_doculect")
    ? urlParams.get("show_doculect")
    : null;
  let mapViewLat = urlParams.has("lat") ? parseInt(urlParams.get("lat")) : 55.0;
  let mapViewLong = urlParams.has("long")
    ? parseInt(urlParams.get("long"))
    : 95.0;

  let zoom = 2.5;

  return { idOfDoculectToShow, mapViewLat, mapViewLong, zoom };
}
