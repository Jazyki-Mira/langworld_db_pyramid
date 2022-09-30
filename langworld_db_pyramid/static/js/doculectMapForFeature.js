import renderMapWithList from "./tools/renderMapWithList.js";

let splitURL = location.pathname.split("/");
const indexOfFeatureID = splitURL.indexOf("feature") + 1;

renderMapWithList(`feature/${splitURL[indexOfFeatureID]}`);
