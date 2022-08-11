import {
  doculectGroupsInMapViewContext,
  idOfDoculectToOpenPopupOnMapContext,
} from "./contexts.js";
import getLocale from "./getLocale.js";

const elem = React.createElement;

export default function InteractiveDoculectList() {
  const { doculectGroupsInMapView } = React.useContext(
    doculectGroupsInMapViewContext
  );
  const { setIdOfDoculectToOpenPopupOnMap } = React.useContext(
    idOfDoculectToOpenPopupOnMapContext
  );

  if (doculectGroupsInMapView === null) return null;

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
        "h2",
        {},
        elem("img", { src: doculectGroup["imgSrc"] }),
        headingText
      ),
      elem(
        "ul",
        { className: "doculects-in-group" },
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
