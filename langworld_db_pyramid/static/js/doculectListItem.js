import getLocale from "./tools/getLocale.js";

export default function DoculectListItem({ doculect }) {
  let textToDisplay = ` ${doculect.iso639p3Codes.join(
    ", "
  )} ${doculect.glottocodes.join(", ")}`;

  if (doculect.aliases != "") {
    textToDisplay += ` (${doculect.aliases})`;
  }

  return React.createElement(
    "li",
    { className: "doculect" },
    React.createElement(
      "a",
      { href: `/${getLocale()}/doculect/${doculect.id}` },
      doculect.name
    ),
    textToDisplay
  );
}
