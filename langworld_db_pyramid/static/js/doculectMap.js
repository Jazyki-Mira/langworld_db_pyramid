import accessToken from "./leafletAccessToken.js"

const renderMarkers = (centerLatitude = 55.0, centerLongitude = 95.0) => {
    let doculectMap = L.map('doculect-profile-map').setView([centerLatitude, centerLongitude], 2.5);
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

    fetch("../json_api/doculects_for_map/")
    .then(res => res.json())
    .then(doculects => addMarkers(doculects, doculectMap))
    .catch(console.error);
}

const addMarkers = (doculects, doculectMap) => {
    for (let doculect of doculects) {
        let marker = L.marker([doculect["latitude"], doculect["longitude"]], {icon: L.divIcon({className: "div-icon square-with-outline green"})}).addTo(doculectMap);
        let url = `../doculect/${doculect["id"]}`;
        marker.bindPopup("<a href=" + url + ">" + doculect["name"] + "</a>");
        marker.on("mouseover", function (e) { this.openPopup(); });
        marker.on('click', function (e) { window.open(url, "_self"); });
    }
}

renderMarkers();
