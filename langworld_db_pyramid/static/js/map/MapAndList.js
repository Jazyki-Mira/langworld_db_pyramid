import {
  allFetchedDoculectGroupsContext,
  doculectGroupsInMapViewContext,
  idOfDoculectToOpenPopupOnMapContext,
  fetchUrlContext,
} from "./contexts.js";
import DataLoadingPlaque from "./DataLoadingPlaque.js";
import DoculectMap from "./DoculectMap.js";
import doculectMapAndListStrings from "../i18n/doculectMapAndListStrings.js";
import getLocale from "../tools/getLocale.js";
import InteractiveDoculectList from "./InteractiveDoculectList.js";

const elem = React.createElement;

export default function MapAndList({
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
      formRef.current.addEventListener("change", () =>
        setFetchUrl(fetchUrlGenerator())
      );
      formRef.current.onsubmit = (e) => {
        e.preventDefault();
      };
    }
  }, []); // only look for the form once, hence empty dependency list

  React.useEffect(() => {
    /* Before the first fetch allDoculectGroups is null anyway, 
    but in tools like Query Wizard there can be multiple fetches 
    and it is good to explicitly set allDoculectGroups to null before fetching.
    That way, for example, another element can detect that new fetch operation started
    and a plaque with "data being loaded" message must be displayed.
     */
    setAllDoculectGroups(null);

    fetch(fetchUrl)
      .then((res) => res.json())
      .then((groups) => setAllDoculectGroups(groups))
      .catch(console.error);
  }, [fetchUrl]);

  /* If the page contains a DIV for alerts and there are no doculects to show, 
  display the alert for 2.5 seconds.
  */
  React.useEffect(() => {
    let alertDiv = document.getElementById("user-alert");
    if (alertDiv === null) return null;

    alertDiv.innerText =
      doculectMapAndListStrings["noMatchingDoculects"][getLocale()];

    if (
      allDoculectGroups != null &&
      allDoculectGroups.length === 1 &&
      allDoculectGroups[0]["doculects"].length === 0
      /* By design of the web app, the only situation where the may be no doculects to show
      (not just in the selected area of the map, but none at all)
      is when the database is queried with multiple parameters (Query Wizard).
      This might change if I create a more complex Query Wizard
      where the user can create their own (multiple) groups!
      */
    ) {
      alertDiv.classList.remove("w3-hide");
      setTimeout(() => alertDiv.classList.add("w3-hide"), 2500);
    }
  }, [allDoculectGroups]);

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
            },
            elem(
              "div",
              { className: "w3-twothird w3-container" },
              elem(DoculectMap)
            ),
            elem(
              "div",
              {
                className: "w3-third w3-container scrollable",
                id: "interactive-list",
              },
              elem(InteractiveDoculectList)
            ),
            elem(DataLoadingPlaque)
          )
        )
      )
    )
  );
}
