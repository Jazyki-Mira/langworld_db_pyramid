import getLocale from "./getLocale.js";
import MapWithList from "../mapWithList/MapWithList.js";

export default function renderMapWithList(variablePartOfUrl) {
  ReactDOM.render(
    React.createElement(MapWithList, {
      urlToFetch: `/${getLocale()}/json_api/doculects_for_map/${variablePartOfUrl}`,
    }),
    document.getElementById("map-and-list")
  );
}
