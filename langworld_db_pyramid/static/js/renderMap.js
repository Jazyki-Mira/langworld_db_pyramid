import accessToken from "./mapboxAccessToken.js";
import fetchDataAndAddMarkersToMap from "./fetchDataAndAddMarkersToMap.js";

const getURLParams = () => {
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

  let zoom = urlParams.has("show_doculect") ? 4 : 2.5;

  return { idOfDoculectToShow, mapViewLat, mapViewLong, zoom };
};

const renderBase = ({ mapDivID, mapViewLat, mapViewLong, zoom }) => {
  let doculectMap = L.map(mapDivID).setView([mapViewLat, mapViewLong], zoom);
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
  }).addTo(doculectMap);

  return doculectMap;
};

export default function renderMap({ mapDivID, urlToFetch }) {
  const paramsFromURL = getURLParams();
  const params = { mapDivID, urlToFetch, ...paramsFromURL };
  let doculectMap = renderBase(params);
  fetchDataAndAddMarkersToMap(doculectMap, params);
  return doculectMap;
}
