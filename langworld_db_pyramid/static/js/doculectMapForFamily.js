import renderMap from "./renderMap.js";

let splitURL = location.pathname.split('/');
const indexOfFamilyID = splitURL.indexOf("family") + 1;
const familyID = splitURL[indexOfFamilyID];

renderMap({ mapDivID: 'map-default', urlToFetch: `../json_api/doculects_for_map/family/${familyID}` });
