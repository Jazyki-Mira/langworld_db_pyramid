import getLocale from "./tools/getLocale.js";
import hideListAndLegendToggleSwitch from "./tools/hideListAndLegendToggleSwitch.js";
import MapWithList from "./mapWithList/MapWithList.js";
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

  const markLabelsOfCategories = () => {
    for (let categoryContainer of document.querySelectorAll(
      "div.wrap-collapsible"
    )) {
      for (let elem of categoryContainer.querySelectorAll("select")) {
        let currentCategoryId = elem.getAttribute("for-category");
        let categoryLabel = document.getElementById(
          `category-label-${currentCategoryId}`
        );
        if (categoryLabel === null) continue;

        if (elem.slim.selected().length > 0) {
          categoryLabel.classList.add(
            "label-of-category-with-some-values-selected"
          );
          break;
        }
        categoryLabel.classList.remove(
          "label-of-category-with-some-values-selected"
        );
      }
    }
  };

  wrapInputFieldsWithSlimSelect();
  form.addEventListener("change", markLabelsOfCategories);

  // after the render: move the form into same container as interactive list, hide the list
  React.useEffect(() => {
    let formContainer = document.getElementById("query-wizard-form-container");
    let mapWithListContainer = document.getElementById(
      "map-and-list-inside-container"
    );
    mapWithListContainer.append(formContainer);

    let interactiveListContainer = document.getElementById("interactive-list");
    interactiveListContainer.classList.toggle("w3-hide");
  }, []);

  return elem(MapWithList, {
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

// query wizard only has one group of doculects, so no need switch between list and legend
hideListAndLegendToggleSwitch();
