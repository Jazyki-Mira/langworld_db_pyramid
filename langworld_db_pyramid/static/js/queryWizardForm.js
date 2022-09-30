import getLocale from "./tools/getLocale.js";
import queryWizardStrings from "./i18n/queryWizardStrings.js";
import { urlTopic } from "./constants/pubSubTopics.js";
/* PubSub and SlimSelect below come from global namespaces 
and have to be included in Jinja templates*/

const form = document.getElementById("query-wizard-form");
const locale = getLocale();

window.addEventListener("load", () => {
  /* this is necessary not only to prepare the form visually 
  but to add .slim attribute to <select> elements */
  wrapInputFieldsWithSlimSelect();

  // move the form into the container with the interactive list of doculects
  const formContainer = document.getElementById("query-wizard-form-container");
  const mapWithListContainer = document.getElementById(
    "map-and-list-inside-container"
  );
  mapWithListContainer.append(formContainer);

  /* hide the interactive list of results because user has not selected anything yet 
  and the form has to be in focus */
  const interactiveListContainer = document.getElementById("interactive-list");
  interactiveListContainer.classList.toggle("w3-hide");

  form.onchange = () => {
    markLabelsOfCategories(); // to let the user see in which categories they have selected values
    PubSub.publish(urlTopic, generateFetchUrl()); // pass the result of calling the function, not the function itself
  };
  form.onsubmit = (e) => e.preventDefault();

  const clearButton = document.getElementById("clear-selection");
  clearButton.onclick = () => {
    for (let elem of document.querySelectorAll("select")) elem.slim.set([]);
  };
});

function generateFetchUrl() {
  let valuesFromAllSelects = [];

  for (let elem of form.querySelectorAll("select")) {
    let selectedValues = elem.slim.selected();
    if (selectedValues.length > 0)
      valuesFromAllSelects.push(`${elem.id}=${selectedValues.toString()}`);
  }

  let paramsForURLToFetch = encodeURI(valuesFromAllSelects.join("&"));
  return `/${locale}/json_api/query_wizard?${paramsForURLToFetch}`;
}

function markLabelsOfCategories() {
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
}

function wrapInputFieldsWithSlimSelect() {
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
}
