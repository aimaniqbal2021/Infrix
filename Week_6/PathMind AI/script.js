const API_URL = "http://127.0.0.1:5000/explore";
const OVERPASS_URL = "https://overpass-api.de/api/interpreter";
const NOMINATIM_URL = "https://nominatim.openstreetmap.org/search";

const map = L.map('map', { zoomControl: false }).setView([25, 40], 3);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap'
}).addTo(map);
L.control.zoom({ position: 'bottomleft' }).addTo(map);

const resultsArea = document.getElementById("results-area");
const searchInput = document.getElementById("search-input");
const suggestionsBox = document.getElementById("suggestions");
const searchClear = document.getElementById("search-clear");

let marker = null;
let trailMarkers = [];
let searchTimeout = null;

// ---- UTILS ----
const diffClass = (d) => d === 'Extreme' ? 'extreme' : d === 'Hard' ? 'hard' : 'moderate';

function clearTrailMarkers() {
    trailMarkers.forEach(m => map.removeLayer(m));
    trailMarkers = [];
}

function getDistanceKm(lat1, lon1, lat2, lon2) {
    const R = 6371;
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat/2)**2 +
              Math.cos(lat1*Math.PI/180) * Math.cos(lat2*Math.PI/180) * Math.sin(dLon/2)**2;
    return (R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))).toFixed(1);
}

const trailIcon = L.divIcon({
    className: '',
    html: `<div style="width:22px;height:22px;background:#FF6B35;border:2px solid #fff;border-radius:50% 50% 50% 0;transform:rotate(-45deg);box-shadow:0 2px 8px rgba(255,107,53,0.6);"></div>`,
    iconSize: [22, 22],
    iconAnchor: [11, 22]
});

// ---- SEARCH / GEOCODE ----
searchInput.addEventListener("input", () => {
    const q = searchInput.value.trim();
    searchClear.style.display = q ? "block" : "none";
    clearTimeout(searchTimeout);
    if (q.length < 2) { suggestionsBox.innerHTML = ""; suggestionsBox.style.display = "none"; return; }
    searchTimeout = setTimeout(() => fetchSuggestions(q), 350);
});

searchClear.addEventListener("click", () => {
    searchInput.value = "";
    searchClear.style.display = "none";
    suggestionsBox.innerHTML = "";
    suggestionsBox.style.display = "none";
    searchInput.focus();
});

searchInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        const q = searchInput.value.trim();
        if (q) { clearTimeout(searchTimeout); fetchSuggestions(q, true); }
    }
});

async function fetchSuggestions(q, autoSelect = false) {
    try {
        const res = await fetch(`${NOMINATIM_URL}?q=${encodeURIComponent(q)}&format=json&limit=5`, {
            headers: { "Accept-Language": "en" }
        });
        const data = await res.json();
        if (autoSelect && data.length > 0) {
            selectPlace(data[0]);
            return;
        }
        showSuggestions(data);
    } catch(e) {
        suggestionsBox.style.display = "none";
    }
}

function showSuggestions(places) {
    if (!places.length) { suggestionsBox.style.display = "none"; return; }
    suggestionsBox.innerHTML = places.map((p, i) => {
        const name = p.display_name.split(",").slice(0, 3).join(", ");
        const type = p.type || p.class || "";
        return `<div class="suggestion-item" data-i="${i}" data-lat="${p.lat}" data-lon="${p.lon}" data-name="${p.display_name}">
            <div class="sug-name">${name}</div>
            <div class="sug-type">${type}</div>
        </div>`;
    }).join("");
    suggestionsBox.style.display = "block";

    suggestionsBox.querySelectorAll(".suggestion-item").forEach(el => {
        el.addEventListener("click", () => {
            selectPlace({
                lat: el.dataset.lat,
                lon: el.dataset.lon,
                display_name: el.dataset.name
            });
        });
    });
}

function selectPlace(place) {
    const lat = parseFloat(place.lat).toFixed(4);
    const lon = parseFloat(place.lon).toFixed(4);
    const name = place.display_name.split(",").slice(0, 2).join(", ");

    searchInput.value = name;
    suggestionsBox.style.display = "none";

    map.setView([lat, lon], 10);
    triggerSearch(lat, lon);
}

// ---- MAP CLICK ----
map.on("click", function(e) {
    const lat = e.latlng.lat.toFixed(4);
    const lon = e.latlng.lng.toFixed(4);
    suggestionsBox.style.display = "none";
    triggerSearch(lat, lon);
});

document.addEventListener("click", (e) => {
    if (!e.target.closest("#search-wrap")) {
        suggestionsBox.style.display = "none";
    }
});

// ---- MAIN SEARCH ----
async function triggerSearch(lat, lon) {
    clearTrailMarkers();
    if (marker) map.removeLayer(marker);
    marker = L.marker([lat, lon]).addTo(map);
    marker.bindPopup(`<b style="font-size:12px">📍 ${lat}, ${lon}</b>`).openPopup();

    document.getElementById("hint-card").style.display = "none";

    resultsArea.innerHTML = `
        <div class="loading-state">
            <div class="spinner"></div>
            <div class="loading-label">Scanning terrain data...</div>
        </div>
    `;

    try {
        const [apiRes, spots] = await Promise.all([
            fetch(API_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ lat, lon })
            }),
            fetchNearbySpots(lat, lon)
        ]);

        const data = await apiRes.json();

        // Drop pins
        const validSpots = spots.filter(s => {
            const slat = s.lat || s.center?.lat;
            const slon = s.lon || s.center?.lon;
            return slat && slon;
        }).slice(0, 8);

        validSpots.forEach(spot => {
            const slat = spot.lat || spot.center?.lat;
            const slon = spot.lon || spot.center?.lon;
            const name = spot.tags?.name || spot.tags?.["name:en"] || "Trail spot";
            const type = spot.tags?.tourism || spot.tags?.natural || spot.tags?.leisure || spot.tags?.route || "spot";
            const dist = getDistanceKm(lat, lon, slat, slon);
            const m = L.marker([slat, slon], { icon: trailIcon }).addTo(map);
            m.bindPopup(`
                <div style="font-family:system-ui;min-width:140px">
                    <b style="font-size:13px;color:#FF6B35">${name}</b><br>
                    <span style="font-size:11px;color:#666;text-transform:capitalize">${type}</span><br>
                    <span style="font-size:11px;color:#888">${dist} km away</span>
                </div>
            `);
            trailMarkers.push(m);
        });

        if (validSpots.length > 0) {
            const group = L.featureGroup([marker, ...trailMarkers]);
            map.fitBounds(group.getBounds().pad(0.2));
        }

        // Build spots HTML
        const spotsHTML = validSpots.length > 0
            ? `<div class="act-section-label">Nearby spots (${validSpots.length} found)</div>
               ${validSpots.map(spot => {
                    const slat = spot.lat || spot.center?.lat;
                    const slon = spot.lon || spot.center?.lon;
                    const name = spot.tags?.name || spot.tags?.["name:en"] || "Unnamed spot";
                    const type = spot.tags?.tourism || spot.tags?.natural || spot.tags?.leisure || spot.tags?.route || "spot";
                    const dist = getDistanceKm(lat, lon, slat, slon);
                    const mapsUrl = `https://www.google.com/maps?q=${slat},${slon}`;
                    return `<div class="trail-card" onclick="window.open('${mapsUrl}','_blank')">
                        <div class="trail-dot"></div>
                        <div class="trail-info">
                            <div class="trail-name">${name}</div>
                            <div class="trail-meta">${type} · ${dist} km away</div>
                        </div>
                        <div class="trail-open">↗</div>
                    </div>`;
               }).join('')}`
            : `<div class="act-section-label">Nearby spots</div>
               <div class="no-spots">No named spots found within 30 km — try clicking a more specific area</div>`;

        const activitiesHTML = (data.activities || []).map((act, i) => `
            <div class="activity-card" style="animation-delay:${i * 0.07}s">
                <span class="act-num">0${i+1}</span>
                <span class="act-name">${act}</span>
                <span class="act-arrow">›</span>
            </div>
        `).join('');

        resultsArea.innerHTML = `
            <div class="coord-badge">
                <div>
                    <div class="label">Coordinates</div>
                    <div class="value">${lat}° / ${lon}°</div>
                </div>
                <div class="dot"></div>
            </div>
            <div class="stat-row">
                <div class="stat-card terrain">
                    <div class="slabel">Terrain</div>
                    <div class="svalue">${data.terrain || '—'}</div>
                </div>
                <div class="stat-card season">
                    <div class="slabel">Best Season</div>
                    <div class="svalue">${data.season || '—'}</div>
                </div>
            </div>
            <div class="diff-card">
                <div class="diff-label">Difficulty rating</div>
                <div class="diff-badge ${diffClass(data.difficulty)}">${data.difficulty || 'Unknown'}</div>
            </div>
            <div class="act-section-label">Top activities</div>
            ${activitiesHTML}
            ${spotsHTML}
        `;

    } catch(err) {
        resultsArea.innerHTML = `
            <div class="coord-badge" style="border-color:rgba(255,77,79,0.3)">
                <div>
                    <div class="label" style="color:#ff4d4f">Connection error</div>
                    <div class="value" style="font-size:13px;color:#8a8f9e">Make sure Flask is running on port 5000</div>
                </div>
            </div>
        `;
    }
}

async function fetchNearbySpots(lat, lon) {
    const radius = 30000;
    const query = `
        [out:json][timeout:25];
        (
          node["tourism"="viewpoint"](around:${radius},${lat},${lon});
          node["natural"="peak"](around:${radius},${lat},${lon});
          way["route"="hiking"](around:${radius},${lat},${lon});
          node["leisure"="nature_reserve"](around:${radius},${lat},${lon});
        );
        out center 10;
    `;
    const res = await fetch(OVERPASS_URL, { method: "POST", body: query });
    const data = await res.json();
    return data.elements || [];
}
