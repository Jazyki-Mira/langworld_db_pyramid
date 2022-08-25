import {
  doculectGroupsInMapViewContext,
  idOfDoculectToOpenPopupOnMapContext,
} from "./contexts.js";
import getLocale from "../tools/getLocale.js";
import doculectMapAndListStrings from "../i18n/doculectMapAndListStrings.js";

const elem = React.createElement;

export default function InteractiveDoculectList() {
  const { doculectGroupsInMapView } = React.useContext(
    doculectGroupsInMapViewContext
  );
  const { setIdOfDoculectToOpenPopupOnMap } = React.useContext(
    idOfDoculectToOpenPopupOnMapContext
  );

  /* TODO I am not sure this is the right module for displaying this message
  although the implementation is easy enough here thanks to useContext()
  */
  if (doculectGroupsInMapView === null)
    return elem(
      "div",
      { className: "w3-display-middle w3-pale-green w3-round-large" },
      elem(
        "p",
        { className: "w3-large w3-center w3-text-dark-blue-grey" },
        doculectMapAndListStrings["dataNotLoaded"][getLocale()]
      )
    );

  if (doculectGroupsInMapView != null && doculectGroupsInMapView.length === 0)
    return elem(
      "p",
      { className: "w3-large" },
      doculectMapAndListStrings["noDoculectsToShow"][getLocale()]
    );

  return elem(
    "div",
    {},
    doculectGroupsInMapView.map((group) => DoculectGroup(group))
  );

  // these functions have to be inside top-level function to be able to use the context
  function DoculectGroup(doculectGroup) {
    let headingText = `${doculectGroup["name"]} (${doculectGroup["doculects"].length})`;
    if (doculectGroup["href"] != "")
      headingText = elem("a", { href: doculectGroup["href"] }, headingText);

    let doculects = doculectGroup["doculects"];
    return elem(
      "div",
      { key: doculectGroup["id"] },
      elem(
        "p",
        { className: "w3-large legend-heading indented-for-icon" },
        elem("img", { src: doculectGroup["imgSrc"] }),
        headingText
      ),
      elem(
        "ul",
        { className: "doculects-in-group w3-ul" },
        doculects.map((doculect) => DoculectListItem(doculect))
      )
    );
  }

  function DoculectListItem(doculect) {
    return elem(
      "li",
      { key: doculect["id"] },
      elem(
        "a",
        {
          href: `/${getLocale()}/doculect/${doculect["id"]}`,
          onMouseEnter: () => setIdOfDoculectToOpenPopupOnMap(doculect["id"]),
          onMouseOut: () => setIdOfDoculectToOpenPopupOnMap(null),
        },
        doculect["name"]
      )
    );
  }
}
