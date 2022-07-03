export default function DoculectListItem({ doculect }) {
    let textToDisplay = `${doculect.name} ${doculect.iso639p3Codes.join(", ")} ${doculect.glottocodes.join(", ")}`;

    if ( doculect.aliases != "") {
        textToDisplay += ` (${doculect.aliases})`;
    }

    return React.createElement(
        "li",
        { className: "doculect" },
        textToDisplay
    );
}
