import { doculectGroupsInMapViewContext } from "./contexts.js";
import getLocale from "./getLocale.js";

const elem = React.createElement;

export default function InteractiveDoculectList() {
  const { doculectGroupsInMapView } = React.useContext(
    doculectGroupsInMapViewContext
  );

  if (doculectGroupsInMapView === null) return null;

  return elem(
    "div",
    {},
    doculectGroupsInMapView.map((group) => DoculectGroup(group))
  );
}

function DoculectGroup(doculectGroup) {
  let doculects = doculectGroup["markers"];
  return elem(
    "div",
    { key: doculectGroup["id"] },
    elem("h2", {}, doculectGroup["name"]),
    elem(
      "ul",
      {},
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
      { href: `/${getLocale()}/doculect/${doculect["id"]}` },
      doculect["name"]
    )
  );
}
