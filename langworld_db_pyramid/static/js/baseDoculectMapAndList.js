import { doculectGroupsContext } from "./contexts.js";
import DoculectMap from "./baseDoculectMap.js";

const elem = React.createElement;

export default function MapAndList({ mapDivID, urlToFetch }) {
  const [doculectGroups, setDoculectGroups] = React.useState(null);

  React.useEffect(() => {
    fetch(urlToFetch)
      .then((res) => res.json())
      .then((groups) => setDoculectGroups(groups))
      .catch(console.error);
  }, []);

  return elem(
    doculectGroupsContext.Provider,
    { value: { doculectGroups, setDoculectGroups } },
    elem(DoculectMap, { mapDivID })
    // list not implemented yet
  );
}
