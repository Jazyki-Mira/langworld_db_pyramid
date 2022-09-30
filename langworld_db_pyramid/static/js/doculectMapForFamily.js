import renderMapWithList from "./tools/renderMapWithList.js";

let splitURL = location.pathname.split("/");
const indexOfFamilyID = splitURL.indexOf("family") + 1;

renderMapWithList(`family/${splitURL[indexOfFamilyID]}`);
