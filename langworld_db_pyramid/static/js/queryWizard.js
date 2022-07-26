import fetchDataAndAddMarkersToMap from "./fetchDataAndAddMarkersToMap.js";
import getLocale from "./getLocale.js";
import renderMap from "./renderMap.js";

for (let elem of document.querySelectorAll("select")) {
  new SlimSelect({
    select: elem,
    placeholder: "Выберите любое количество значений",
    searchPlaceholder: "Поиск значения",
    searchText: "Нет подходящих значений",
    allowDeselectOption: true,
    closeOnSelect: false,
    selectByGroup: true,
  });
}

const handleChange = (e, doculectMap) => {
  console.log("Changed");
  let valuesFromAllSelects = [];

  for (let elem of document.querySelectorAll("select")) {
    let selectedValues = elem.slim.selected();
    if (selectedValues.length > 0)
      valuesFromAllSelects.push(`${elem.id}=${selectedValues.toString()}`);
  }

  let paramsForURLToFetch = encodeURI(valuesFromAllSelects.join("&"));
  let urlToFetch = `/${getLocale()}/json_api/query_wizard?${paramsForURLToFetch}`;
  console.log(urlToFetch);
  fetchDataAndAddMarkersToMap(doculectMap, { urlToFetch });
};

const handleSubmit = (e) => {
  e.preventDefault();
};

let doculectsFoundMap = renderMap({
  mapDivID: "map-default",
  urlToFetch: `/${getLocale()}/json_api/doculects_for_map/all`,
});

let form = document.querySelector("form");
form.onchange = (e) => handleChange(e, doculectsFoundMap);
form.onsubmit = handleSubmit;
