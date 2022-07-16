import accessToken from "./mapboxAccessToken.js"

const getURLParams = () => {
    let urlParams = new URLSearchParams(location.search);

    /* these 3 can be connected (center on a specific doculect),
    but I want to keep the functionality flexible and be able to center on something
    without necessarily showing the doculect */
    let idOfDoculectToShow = urlParams.has('show_doculect') ? urlParams.get('show_doculect') : null;
    let mapViewLat = urlParams.has('lat') ? parseInt(urlParams.get('lat')) : 55.0;
    let mapViewLong = urlParams.has('long') ? parseInt(urlParams.get('long')) : 95.0;

    let zoom = urlParams.has('show_doculect') ? 4 : 2.5;

    return { idOfDoculectToShow, mapViewLat, mapViewLong, zoom };
}

const renderBase = ({ mapDivID, mapViewLat, mapViewLong, zoom }) => {

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

        let marker = L.marker([doculect["latitude"], doculect["longitude"]], {icon: icon, riseOnHover: true}).addTo(doculectMap);
        let url = `../doculect/${doculect["id"]}`;
        let popupText = "popupText" in doculect ? doculect["popupText"] : "<a href=" + url + ">" + doculect["name"] + "</a>";
        marker.bindPopup(popupText);
        marker.on("mouseover", function (e) { this.openPopup(); });
        marker.on("click", function (e) { window.open(url, "_self"); });

        if (doculect["id"] === idOfDoculectToShow) marker.openPopup();
    }
}

export default function renderMap ({ mapDivID, urlToFetch }) {
    const paramsFromURL = getURLParams();
    const params = { mapDivID, urlToFetch, ...paramsFromURL };
    let doculectMap = renderBase(params);
    fetchDataAndAddMarkers(doculectMap, params);
};
