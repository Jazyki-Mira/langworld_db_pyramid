import getLocale from "./tools/getLocale.js";
import MapWithList from "./mapWithList/MapWithList.js";

let splitURL = location.pathname.split("/");
const indexOfFamilyID = splitURL.indexOf("family") + 1;
const familyID = splitURL[indexOfFamilyID];

ReactDOM.render(
  React.createElement(MapWithList, {
    urlToFetch: `/${getLocale()}/json_api/doculects_for_map/family/${familyID}`,
  }),
  document.getElementById("map-and-list")
);
