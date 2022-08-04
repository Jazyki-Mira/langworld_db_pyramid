import getLocale from "./getLocale.js";
import MapAndList from "./baseDoculectMapAndList.js";

ReactDOM.render(
  React.createElement(MapAndList, {
    mapDivID: "map-default",
    urlToFetch: `/${getLocale()}/json_api/doculects_for_map/all`,
  }),
  document.getElementById("map-and-list")
);
