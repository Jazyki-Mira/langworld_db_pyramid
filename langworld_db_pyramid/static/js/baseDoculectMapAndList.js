import {
  allFetchedDoculectGroupsContext,
  doculectGroupsInMapViewContext,
} from "./contexts.js";
import InteractiveDoculectList from "./baseDoculectList.js";
import DoculectMap from "./baseDoculectMap.js";

const elem = React.createElement;

export default function MapAndList({ mapDivID, urlToFetch }) {
  const [allDoculectGroups, setAllDoculectGroups] = React.useState(null);
  const [doculectGroupsInMapView, setDoculectGroupsInMapView] =
    React.useState(null);

  React.useEffect(() => {
    fetch(urlToFetch)
      .then((res) => res.json())
      .then((groups) => setAllDoculectGroups(groups))
      .catch(console.error);
  }, []);

  return elem(
    allFetchedDoculectGroupsContext.Provider,
    { value: { allDoculectGroups, setAllDoculectGroups } },
    elem(
      doculectGroupsInMapViewContext.Provider,
      { value: { doculectGroupsInMapView, setDoculectGroupsInMapView } },
      elem(
        "div",
        { className: "w3-row w3-padding-small" }, // TODO hardcoded for now
        elem(
          "div",
          { className: "w3-twothird w3-container" },
          // TODO div ID for map is needed because of CSS, but should I really keep it here?
          elem(DoculectMap, { mapDivID })
        ),
        elem(
          "div",
          { className: "w3-third w3-container" },
          elem(InteractiveDoculectList) // TODO div ID here or remove div ID for map
        )
      )
    )
  );
}
