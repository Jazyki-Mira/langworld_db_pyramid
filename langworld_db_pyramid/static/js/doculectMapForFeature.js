import getLocale from "./tools/getLocale.js";
import MapWithList from "./mapWithList/MapWithList.js";

let splitURL = location.pathname.split("/");
const indexOfFeatureID = splitURL.indexOf("feature") + 1;
const featureID = splitURL[indexOfFeatureID];

ReactDOM.render(
  React.createElement(MapWithList, {
    urlToFetch: `/${getLocale()}/json_api/doculects_for_map/feature/${featureID}`,
  }),
  document.getElementById("map-and-list")
);
