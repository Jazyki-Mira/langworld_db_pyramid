import MapAndList from "./map/MapAndList.js";
import getLocale from "./tools/getLocale.js";
import queryWizardStrings from "./i18n/queryWizardStrings.js";

const elem = React.createElement;

const wrapInputFieldsWithSlimSelect = () => {
  const locale = getLocale();

  for (let elem of document.querySelectorAll("select")) {
    new SlimSelect({
      select: elem,
      placeholder: queryWizardStrings["placeholder"][locale],
      searchPlaceholder: queryWizardStrings["searchPlaceholder"][locale],
      searchText: queryWizardStrings["searchText"][locale],
      allowDeselectOption: true,
      closeOnSelect: false,
      selectByGroup: true,
      showContent: "down",
    });
  }
};

function QueryWizard() {
  const form = document.getElementById("query-wizard-form");
  const locale = getLocale();

  const generateFetchUrl = () => {
    let valuesFromAllSelects = [];

    for (let elem of form.querySelectorAll("select")) {
      let selectedValues = elem.slim.selected();
      if (selectedValues.length > 0)
        valuesFromAllSelects.push(`${elem.id}=${selectedValues.toString()}`);
    }

    let paramsForURLToFetch = encodeURI(valuesFromAllSelects.join("&"));
    return `/${locale}/json_api/query_wizard?${paramsForURLToFetch}`;
  };

  wrapInputFieldsWithSlimSelect();

  // after the render: move the form into same container as interactive list, hide the list
  React.useEffect(() => {
    let formContainer = document.getElementById("query-wizard-form-container");
    let mapAndListContainer = document.getElementById(
      "map-and-list-inside-container"
    );
    mapAndListContainer.append(formContainer);

    let interactiveListContainer = document.getElementById("interactive-list");
    interactiveListContainer.classList.toggle("w3-hide");
  }, []);

  return elem(MapAndList, {
    mapDivID: "map-default",
    urlToFetch: `/${locale}/json_api/doculects_for_map/all`,
    formId: "query-wizard-form",
    fetchUrlGenerator: generateFetchUrl,
  });
}

ReactDOM.render(elem(QueryWizard), document.getElementById("map-and-list"));

const clearButton = document.getElementById("clear-selection");
clearButton.onclick = () => {
  // will only work if the select elements were already wrapped in SlimSelect
  for (let elem of document.querySelectorAll("select")) elem.slim.set([]);
};
