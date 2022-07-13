import accessToken from "./mapboxAccessToken.js"

const getUrlParams = () => {
    let urlParams = new URLSearchParams(location.search);

    let lat = 55.0;
    let long = 95.0;
    let zoom = 2.5;

    if (urlParams.has('lat')) lat = parseInt(urlParams.get('lat'));
    if (urlParams.has('long')) long = parseInt(urlParams.get('long'));
    if (urlParams.has('show_doculect')) zoom = 4;

    return { lat, long, zoom };
}

const renderMap = ({ lat, long, zoom }) => {

    let doculectMap = L.map('doculect-profile-map').setView([lat, long], zoom);
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

const fetchDataAndAddMarkers = (url, doculectMap) => {
    fetch(url)
    .then(res => res.json())
    .then(doculects => addMarkers(doculects, doculectMap))
    .catch(console.error);
}

const addMarkers = (doculects, doculectMap) => {
    let urlParams = new URLSearchParams(location.search);

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

        if (urlParams.has("show_doculect") && urlParams.get("show_doculect") === doculect["id"]) marker.openPopup();
    }
}

const main = () => {
    const urlParams = getUrlParams(); // TODO: div class, show_doculect
    let doculectMap = renderMap(urlParams);
    const url = "../json_api/doculects_for_map/";
    fetchDataAndAddMarkers(url, doculectMap);
}

main();
