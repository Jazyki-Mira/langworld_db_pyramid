import doculectListFormStrings from "./i18n/doculectListFormStrings.js";
import getLocale from "./tools/getLocale.js";

const elem = React.createElement;
const listContainer = document.getElementById("doculect-finder-list");

function DoculectListItem({ doculect }) {
  let additionalTextToDisplay = "";

  if (doculect.aliases != "") {
    additionalTextToDisplay += ` (${doculect.aliases})`;
  }

  if (doculect.iso639p3Codes.length > 0)
    additionalTextToDisplay += ` | ${doculect.iso639p3Codes.join(", ")}`;

  if (doculect.glottocodes.length > 0)
    additionalTextToDisplay += ` | ${doculect.glottocodes.join(", ")}`;

  return elem(
    "li",
    { className: "doculect" },
    elem(
      "a",
      { href: `/${getLocale()}/doculect/${doculect.id}` },
      doculect.name
    ),
    elem(
      "span",
      { className: "w3-text-dark-blue-grey" },
      additionalTextToDisplay
    )
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

  const fetchAndRenderResults = (url) => {
    ReactDOM.render(
      elem(
        "p",
        { className: "w3-margin-left w3-text-dark-blue-grey" },
        doculectListFormStrings["searchInProgressText"][locale]
      ),
      listContainer
    );

    fetch(url)
      .then((res) => res.json())
      .then(renderListOfMatchingDoculects)
      .catch(console.error);
  };

  const renderListOfMatchingDoculects = (retrieved_data) => {
    const locale = getLocale();

    if (typeof retrieved_data[Symbol.iterator] != "function") return; // promise is pending, no data to iterate over

    if (retrieved_data.length === 0) {
      ReactDOM.render(
        elem(
          "p",
          { className: "w3-margin-left w3-text-dark-blue-grey" },
          doculectListFormStrings["nothingFoundText"][locale]
        ),
        listContainer
      );
    } else {
      ReactDOM.render(
        elem(
          "ul",
          {},
          retrieved_data.map((item, i) =>
            elem(DoculectListItem, { doculect: item, key: i }, null)
          )
        ),
        listContainer
      );
    }
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
      doculectListFormStrings["formLabel"][locale]
    ),
    elem("br"),
    elem("input", {
      id: "doculect-form-input",
      name: "searchText",
      type: "text",
      placeholder: doculectListFormStrings["inputPlaceholderText"][locale],
      onChange: (e) => setQuery(e.target.value),
    }),
    elem("input", {
      id: "doculect-form-button",
      type: "submit",
      value: doculectListFormStrings["buttonLabel"][locale],
    })
  );
}

ReactDOM.render(
  elem(DoculectListForm),
  document.getElementById("doculect-finder-form")
);
