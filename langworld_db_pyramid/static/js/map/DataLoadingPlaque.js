import { allFetchedDoculectGroupsContext } from "./contexts.js";
import getLocale from "../tools/getLocale.js";
import doculectMapAndListStrings from "../i18n/doculectMapAndListStrings.js";

const elem = React.createElement;

export default function DataLoadingPlaque() {
  const { allDoculectGroups } = React.useContext(
    allFetchedDoculectGroupsContext
  );

  // remove the plaque as soon as something is loaded
  if (allDoculectGroups != null) return null;

  return elem(
    "div",
    { className: "w3-display-middle w3-pale-blue w3-round-large" },
    elem(
      "p",
      { className: "w3-large w3-center w3-text-dark-blue-grey" },
      doculectMapAndListStrings["dataNotLoaded"][getLocale()]
    )
  );
}
