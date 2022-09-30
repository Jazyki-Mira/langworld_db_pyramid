export default function getIdFromUrl(paramName) {
  let splitURL = location.pathname.split("/");
  const indexOfFeatureID = splitURL.indexOf(paramName) + 1;

  return splitURL[indexOfFeatureID];
}
