import {
  allFetchedDoculectGroupsContext,
  doculectGroupsInMapViewContext,
  idOfDoculectToOpenPopupOnMapContext,
  fetchUrlContext,
} from "./contexts.js";
import InteractiveDoculectList from "./InteractiveDoculectList.js";
import DoculectMap from "./DoculectMap.js";

const elem = React.createElement;

// TODO rename urlToFetch
export default function MapAndList({
  mapDivID,
  urlToFetch,
  formId = null,
  fetchUrlGenerator = null,
}) {
  const [allDoculectGroups, setAllDoculectGroups] = React.useState(null);
  const [doculectGroupsInMapView, setDoculectGroupsInMapView] =
    React.useState(null);
  const [idOfDoculectToOpenPopupOnMap, setIdOfDoculectToOpenPopupOnMap] =
    React.useState(null);
  const [fetchUrl, setFetchUrl] = React.useState(urlToFetch);

  // fetchUrl can only change if there is some sort of form on the page
  // For now I assume that the form is in HTML already, not being created by React
  const formRef = React.useRef(null);

  React.useEffect(() => {
    if (formId != null) {
      formRef.current = document.getElementById(formId);
      formRef.current.onchange = () => setFetchUrl(fetchUrlGenerator());
      formRef.current.onsubmit = (e) => {
        e.preventDefault();
      };
    }
  }, []); // only look for the form once, hence empty dependency list

  React.useEffect(() => {
    console.log("Starting to fetch URL", fetchUrl);
    fetch(fetchUrl)
      .then((res) => res.json())
      .then((groups) => setAllDoculectGroups(groups))
      .then(console.log("Fetched"))
      .catch(console.error);
  }, [fetchUrl]); // TODO handle case when there are no doculects

  return elem(
    fetchUrlContext.Provider,
    { value: { fetchUrl, setFetchUrl } },
    elem(
      allFetchedDoculectGroupsContext.Provider,
      { value: { allDoculectGroups, setAllDoculectGroups } },
      elem(
        doculectGroupsInMapViewContext.Provider,
        { value: { doculectGroupsInMapView, setDoculectGroupsInMapView } },
        elem(
          idOfDoculectToOpenPopupOnMapContext.Provider,
          {
            value: {
              idOfDoculectToOpenPopupOnMap,
              setIdOfDoculectToOpenPopupOnMap,
            },
          },
          elem(
            "div",
            {
              className: "w3-row w3-padding-small",
              id: "map-and-list-inside-container",
            }, // TODO hardcoded for now
            elem(
              "div",
              { className: "w3-twothird w3-container" },
              // TODO div ID for map is needed because of CSS, but should I really keep it here?
              elem(DoculectMap, { mapDivID })
            ),
            elem(
              "div",
              {
                className: "w3-third w3-container scrollable",
                id: "interactive-list",
              },
              elem(InteractiveDoculectList) // TODO div ID here or remove div ID for map
            )
          )
        )
      )
    )
  );
}
