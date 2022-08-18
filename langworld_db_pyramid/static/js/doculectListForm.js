import doculectListFormLabels from "./i18n/doculectListFormLabels.js";
import getLocale from "./tools/getLocale.js";

const elem = React.createElement;

function DoculectListItem({ doculect }) {
  let textToDisplay = ` ${doculect.iso639p3Codes.join(
    ", "
  )} ${doculect.glottocodes.join(", ")}`;

  if (doculect.aliases != "") {
    textToDisplay += ` (${doculect.aliases})`;
  }

  return elem(
    "li",
    { className: "doculect" },
    elem(
      "a",
      { href: `/${getLocale()}/doculect/${doculect.id}` },
      doculect.name
    ),
    textToDisplay
  );
}

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

  return elem(
    "form",
    {
      onSubmit: (e) => {
        handleSubmit(e);
      },
    },
    elem(
      "label",
      {
        id: "doculect-form-label",
        className: "w3-large w3-text-dark-blue-grey",
      },
      doculectListFormLabels["formLabel"][locale]
    ),
    elem("br"),
    elem("input", {
      id: "doculect-form-input",
      name: "searchText",
      type: "text",
      placeholder: doculectListFormLabels["inputPlaceholderText"][locale],
      onChange: (e) => setQuery(e.target.value),
    }),
    elem("input", {
      id: "doculect-form-button",
      type: "submit",
      value: doculectListFormLabels["buttonLabel"][locale],
    })
  );
}

ReactDOM.render(
  elem(DoculectListForm),
  document.getElementById("doculect-finder-form")
);
