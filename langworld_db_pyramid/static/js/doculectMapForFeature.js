import getLocale from "./getLocale.js";
import MapAndList from "./baseDoculectMapAndList.js";

let splitURL = location.pathname.split("/");
const indexOfFeatureID = splitURL.indexOf("feature") + 1;
const featureID = splitURL[indexOfFeatureID];

ReactDOM.render(
  React.createElement(MapAndList, {
    mapDivID: "map-default",
    urlToFetch: `/${getLocale()}/json_api/doculects_for_map/feature/${featureID}`,
  }),
  document.getElementById("map-and-list")
);
