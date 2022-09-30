import {
  allFetchedDoculectGroupsContext,
  doculectGroupsInMapViewContext,
  idOfDoculectToOpenPopupOnMapContext,
} from "./contexts.js";
import DataLoadingPlaque from "./components/DataLoadingPlaque.js";
import DoculectMap from "./components/DoculectMap.js";
import doculectMapAndListStrings from "../i18n/doculectMapAndListStrings.js";
import getLocale from "../tools/getLocale.js";
import InteractiveDoculectList from "./components/InteractiveDoculectList.js";
import { urlTopic } from "../constants/pubSubTopics.js";

const elem = React.createElement;

export default function MapWithList({ urlToFetch }) {
  const [allDoculectGroups, setAllDoculectGroups] = React.useState(null);
  const [doculectGroupsInMapView, setDoculectGroupsInMapView] =
    React.useState(null);
  const [idOfDoculectToOpenPopupOnMap, setIdOfDoculectToOpenPopupOnMap] =
    React.useState(null);
  const [fetchUrl, setFetchUrl] = React.useState(urlToFetch);

  // If there is a PubSub, subscribe to changes in URL to be fetched
  try {
    /* A callback passed to PubSub.subscribe (along with topic name) takes two arguments, 
      first of which is topic. I don't need it.
    */
    PubSub.subscribe(urlTopic, (_, url) => setFetchUrl(url));
  } catch (ReferenceError) {
    /* PubSub is only needed if I need to fetch new data dynamically.
       But if the page does not need to fetch new data, there is no need to import PubSub,
       and it is OK to just let the ReferenceError pass silently.
    */
  }

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

  /* If the page contains a DIV for alerts and there are no doculects to show, show the alert.
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
      // show the alert, then after .75 seconds fade out (fading out takes 1 second, see CSS)
      alertDiv.classList.remove("w3-hide");
      setTimeout(() => alertDiv.classList.add("fade-out"), 750);
      setTimeout(() => {
        // after a total of 2 seconds, revert classes to original state
        alertDiv.classList.remove("fade-out");
        alertDiv.classList.add("w3-hide");
      }, 2000);
    }
  }, [allDoculectGroups]);

  return elem(
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
  );
}
