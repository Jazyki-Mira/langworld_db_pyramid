import accessToken from "./mapboxAccessToken.js"

const getParams = () => {
    let urlParams = new URLSearchParams(location.search);

    /* these 3 can be connected (center on a specific doculect),
    but I want to keep the functionality flexible and be able to center on something
    without necessarily showing the doculect */
    let mapViewLat = 55.0;
    let mapViewLong = 95.0;
    let idOfDoculectToShow = null;

    let zoom = 2.5;

    if (urlParams.has('lat')) mapViewLat = parseInt(urlParams.get('lat'));
    if (urlParams.has('long')) mapViewLong = parseInt(urlParams.get('long'));
    if (urlParams.has('show_doculect')) zoom = 4;
    // a check can be added here to change default map div id

    if (urlParams.has('show_doculect')) idOfDoculectToShow = urlParams.get('show_doculect');

    // these parameters may not be directly READ from URL params (after "?" in URL)
    // but INFERRED from URL
    let mapDivID = 'doculect-profile-map';
    let urlToFetch = '../json_api/doculects_for_map/';

    return { idOfDoculectToShow, mapDivID, mapViewLat, mapViewLong, urlToFetch, zoom };
}

const renderMap = ({ mapDivID, mapViewLat, mapViewLong, zoom }) => {

    let doculectMap = L.map(mapDivID).setView([mapViewLat, mapViewLong], zoom);
    const titleLayerUrl = 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=' + accessToken;

    L.tileLayer(titleLayerUrl,
        {
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            maxZoom: 18,
            id: 'mapbox/streets-v11',
            tileSize: 512,
            zoomOffset: -1,
            accessToken: accessToken
        }
    ).addTo(doculectMap);

    return doculectMap;
}

const fetchDataAndAddMarkers = (doculectMap, urlParams) => {
    fetch(urlParams.urlToFetch)
    .then(res => res.json())
    .then(doculects => addMarkers(doculects, doculectMap, urlParams))
    .catch(console.error);
}

const addMarkers = (doculects, doculectMap, { idOfDoculectToShow }) => {
    for (let doculect of doculects) {

       let iconSize = [parseInt(doculect["divIconSize"][0]), parseInt(doculect["divIconSize"][1])];
       let iconAnchor = [iconSize[0] / 2, iconSize[1] / 2];

       const icon = L.divIcon({
           html: doculect["divIconHTML"],
           className: "",
           iconSize: iconSize,
           iconAnchor: iconAnchor,
        });

        let marker = L.marker([doculect["latitude"], doculect["longitude"]], {icon: icon}).addTo(doculectMap);
        let url = `../doculect/${doculect["id"]}`;
        marker.bindPopup("<a href=" + url + ">" + doculect["name"] + "</a>");
        marker.on("mouseover", function (e) { this.openPopup(); });
        marker.on("click", function (e) { window.open(url, "_self"); });

        if (doculect["id"] === idOfDoculectToShow) marker.openPopup();
    }
}

const main = () => {
    const params = getParams();
    let doculectMap = renderMap(params);
    fetchDataAndAddMarkers(doculectMap, params);
}

main();
