var map = L.map("map").setView([35.62484634835641, 139.78602418344875], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

var marker = L.marker([35.62484634835641, 139.78602418344875]).addTo(map);

marker.bindPopup("<b>お台場</b>");