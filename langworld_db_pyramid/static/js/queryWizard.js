import MapAndList from "./baseDoculectMapAndList.js";
import getLocale from "./getLocale.js";

const elem = React.createElement;

const wrapInputFieldsWithSlimSelect = () => {
  for (let elem of document.querySelectorAll("select")) {
    new SlimSelect({
      select: elem,
      placeholder: "Выберите любое количество значений",
      searchPlaceholder: "Поиск значения",
      searchText: "Нет подходящих значений",
      allowDeselectOption: true,
      closeOnSelect: false,
      selectByGroup: true,
      showContent: "down",
    });
  }
};

function QueryWizard() {
  const form = document.getElementById("query-wizard-form");

  const generateFetchUrl = () => {
    let valuesFromAllSelects = [];

    for (let elem of form.querySelectorAll("select")) {
      let selectedValues = elem.slim.selected();
      if (selectedValues.length > 0)
        valuesFromAllSelects.push(`${elem.id}=${selectedValues.toString()}`);
    }

    let paramsForURLToFetch = encodeURI(valuesFromAllSelects.join("&"));
    return `/${getLocale()}/json_api/query_wizard?${paramsForURLToFetch}`;
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
    urlToFetch: `/${getLocale()}/json_api/doculects_for_map/all`,
    formId: "query-wizard-form",
    fetchUrlGenerator: generateFetchUrl,
  });
}

ReactDOM.render(elem(QueryWizard), document.getElementById("map-and-list"));
