import DoculectListItem from "./doculectListItem.js";
import doculectListFormLabels from "./i18n/doculectListFormLabels.js";
import getLocale from "./getLocale.js";

const elem = React.createElement;

const fetchAndRenderResults = (url) =>
  fetch(url)
    .then((res) => res.json())
    .then(renderListOfMatchingDoculects)
    .catch(console.error);

const renderListOfMatchingDoculects = (retrieved_data) => {
  if (typeof retrieved_data[Symbol.iterator] != "function") return; // promise is pending, no data to iterate over

  ReactDOM.render(
    elem(
      "ul",
      {},
      retrieved_data.map((item, i) =>
        elem(DoculectListItem, { doculect: item, key: i }, null)
      )
    ),
    document.getElementById("doculect-finder-list")
  );
};

function DoculectListForm(props) {
  const [query, setQuery] = React.useState("");

  const locale = getLocale();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query === "") {
      renderListOfMatchingDoculects([]);
    } else {
      let url = `/${locale}/json_api/doculect_by_name/` + query;
      fetchAndRenderResults(url);
    }
  };

  return elem(
    "form",
    {
      onSubmit: (e) => {
        handleSubmit(e);
      },
    },
    elem("label", {}, doculectListFormLabels["formLabel"][locale]),
    elem("br"),
    elem("input", {
      name: "searchText",
      type: "text",
      onChange: (e) => setQuery(e.target.value),
    }),
    elem("input", {
      type: "submit",
      value: doculectListFormLabels["buttonLabel"][locale],
    })
  );
}

ReactDOM.render(
  elem(DoculectListForm),
  document.getElementById("doculect-finder-form")
);
