import getLocale from "./tools/getLocale.js";
import hideListAndLegendToggleSwitch from "./tools/hideListAndLegendToggleSwitch.js";
import MapWithList from "./mapWithList/MapWithList.js";

ReactDOM.render(
  React.createElement(MapWithList, {
    urlToFetch: `/${getLocale()}/json_api/doculects_for_map/all`,
  }),
  document.getElementById("map-and-list")
);

// general map only has one group of doculects, so no need switch between list and legend
hideListAndLegendToggleSwitch();
