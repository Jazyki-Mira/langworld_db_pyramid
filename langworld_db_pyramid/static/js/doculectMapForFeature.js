import renderMap from "./renderMap.js";

let splitURL = location.pathname.split('/');
const indexOfFeatureID = splitURL.indexOf("feature") + 1;
const featureID = splitURL[indexOfFeatureID];

renderMap({ mapDivID: 'map-default', urlToFetch: `../json_api/doculects_for_map/feature/${featureID}` });
