export default function getURLParams() {
  let urlParams = new URLSearchParams(location.search);

  /* these 3 can be connected (center on a specific doculect),
      but I want to keep the functionality flexible and be able to center on something
      without necessarily showing the doculect */
  let idOfDoculectToShow = urlParams.has("show_doculect")
    ? urlParams.get("show_doculect")
    : null;
  let mapViewLat = urlParams.has("lat") ? parseInt(urlParams.get("lat")) : 55.0;
  let mapViewLong = urlParams.has("long")
    ? parseInt(urlParams.get("long"))
    : 95.0;

  let zoom = 2.5;

  return { idOfDoculectToShow, mapViewLat, mapViewLong, zoom };
}
