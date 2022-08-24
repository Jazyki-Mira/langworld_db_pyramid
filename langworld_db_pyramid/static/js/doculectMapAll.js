import getLocale from "./tools/getLocale.js";
import hideListAndLegendToggleSwitch from "./hideListAndLegendToggleSwitch.js";
import MapAndList from "./map/MapAndList.js";

ReactDOM.render(
  React.createElement(MapAndList, {
    mapDivID: "map-default",
    urlToFetch: `/${getLocale()}/json_api/doculects_for_map/all`,
  }),
  document.getElementById("map-and-list")
);

hideListAndLegendToggleSwitch();
