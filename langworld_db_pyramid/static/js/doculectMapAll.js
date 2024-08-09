import renderMapWithList from "./tools/renderMapWithList.js";
import adjustInteractiveListForSolitaryGroup from "./tools/adjustInteractiveListForSolitaryGroup.js";

renderMapWithList("all");

window.addEventListener(
  "DOMContentLoaded",
  adjustInteractiveListForSolitaryGroup
);
