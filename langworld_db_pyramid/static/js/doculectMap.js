import accessToken from "./leafletAccessToken.js"

const renderMarkers = () => {
    let urlParams = new URLSearchParams(location.search);

    let lat = 55.0;
    let long = 95.0;
    let zoom = 2.5;

    if (urlParams.has('lat')) lat = urlParams.get('lat');
    if (urlParams.has('long')) long = urlParams.get('long');
    if (urlParams.has('show_doculect')) zoom = 4;

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

    fetch("../json_api/doculects_for_map/")
    .then(res => res.json())
    .then(doculects => addMarkers(doculects, doculectMap))
    .catch(console.error);
}

const addMarkers = (doculects, doculectMap) => {
    let urlParams = new URLSearchParams(location.search);

    const defaultIcon = L.divIcon({
       html: `
       <svg  xmlns="http://www.w3.org/2000/svg"
       xmlns:xlink="http://www.w3.org/1999/xlink" height="40" width="40">
       <circle cx="20" cy="20" r="14" style="fill:#008080;stroke:black;stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;"/>
       </svg>
       `,
       className: "",
       iconSize: [40, 40],
       iconAnchor: [20, 20],
    });

    for (let doculect of doculects) {
        let marker = L.marker([doculect["latitude"], doculect["longitude"]], {icon: defaultIcon}).addTo(doculectMap);
        let url = `../doculect/${doculect["id"]}`;
        marker.bindPopup("<a href=" + url + ">" + doculect["name"] + "</a>");
        marker.on("mouseover", function (e) { this.openPopup(); });
        marker.on("click", function (e) { window.open(url, "_self"); });

        if (urlParams.has("show_doculect") && urlParams.get("show_doculect") === doculect["id"]) marker.openPopup();
    }
}

renderMarkers();
