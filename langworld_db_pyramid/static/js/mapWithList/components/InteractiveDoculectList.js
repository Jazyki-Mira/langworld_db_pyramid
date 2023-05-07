import {
  doculectGroupsInMapViewContext,
  idOfDoculectToOpenPopupOnMapContext,
} from "../contexts.js";
import getLocale from "../../tools/getLocale.js";
import doculectMapAndListStrings from "../../i18n/doculectMapAndListStrings.js";

const elem = React.createElement;

export default function InteractiveDoculectList() {
  const { doculectGroupsInMapView } = React.useContext(
    doculectGroupsInMapViewContext
  );
  const { setIdOfDoculectToOpenPopupOnMap } = React.useContext(
    idOfDoculectToOpenPopupOnMapContext
  );

  if (doculectGroupsInMapView === null) return null;

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
    // return empty div for compound values (hence excluding them from interactive list)
    // TODO in the future this can be toggled by the user
    if (doculectGroup["id"].includes("&")) return elem("div", { key: doculectGroup["id"] });

    let headingText = `${doculectGroup["name"]} (${doculectGroup["doculects"].length})`;
    if (doculectGroup["href"] != "")
      headingText = elem("a", { href: doculectGroup["href"] }, headingText);

    let doculects = doculectGroup["doculects"];
    return elem(
      "div",
      { key: doculectGroup["id"] },
      elem(
        "p",
        { className: "legend-heading indented-for-icon" },
        elem("img", {
          className: "icon-in-map-legend",
          src: doculectGroup["imgSrc"],
          title: doculectMapAndListStrings["toggleSwitchHint"][getLocale()],
          onClick: () => {
            let ul = document.querySelector(`ul#${doculectGroup["id"]}`);
            ul.classList.toggle("w3-hide");
          },
        }),
        headingText
      ),
      elem(
        "ul",
        { className: "doculects-in-group w3-ul", id: doculectGroup["id"] },
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
