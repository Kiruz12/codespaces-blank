var map = L.map('map').setView([4.6, -74.1], 6);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

fetch('/api/divipola')
  .then(response => response.json())
  .then(data => {
    data[0].children.forEach(dep => {
      dep.children.forEach(mun => {
        if (mun.lat && mun.lon) {
          L.marker([mun.lat, mun.lon])
            .addTo(map)
            .bindPopup(`<b>${mun.name}</b><br>${dep.name}`);
        }
      });
    });
  });
