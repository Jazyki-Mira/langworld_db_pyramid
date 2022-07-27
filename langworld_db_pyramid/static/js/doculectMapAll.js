import getLocale from "./getLocale.js";
import renderMap from "./renderMap.js";

renderMap({
  mapDivID: "map-default",
  urlToFetch: `/${getLocale()}/json_api/doculects_for_map/all`,
});
