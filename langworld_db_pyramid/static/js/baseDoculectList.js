import { doculectGroupsInMapViewContext } from "./contexts.js";
import getLocale from "./getLocale.js";

const elem = React.createElement;

export default function InteractiveDoculectList() {
  const { doculectGroupsInMapView } = React.useContext(
    doculectGroupsInMapViewContext
  );

  if (doculectGroupsInMapView === null) return null;

  console.log("Inside DoculectList:", doculectGroupsInMapView);
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
    {},
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
    {},
    elem(
      "a",
      { href: `/${getLocale()}/doculect/${doculect["id"]}` },
      doculect["name"]
    )
  );
}
