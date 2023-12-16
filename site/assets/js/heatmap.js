let myMap = L.map("leafletmap", {
    center: [-29, 41],
    zoom: 5,
    scrollWheelZoom: false,
});

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    minZoom: 1,
    noWrap: true,
}).addTo(myMap);

myMap.setMaxBounds(  [[-10,-2],   [-40,40]]  )

let heatArray = [];
// Determine the current HTML page or identifier
const currentPage = window.location.pathname;

// Define different feature variables for each HTML page
let features;

// Check the current page and assign features accordingly
if (currentPage.includes('ssp126.html')) {
    features = ssp126_geoData.features; // Replace with your spp245 feature data
    console.log("126")
} else if (currentPage.includes('ssp370.html')) {
    features = ssp370_geoData.features; // Replace with your spp370 feature data
    console.log("370")
} else if (currentPage.includes('ssp585.html')) {
    features = ssp585_geoData.features; // Replace with your spp585 feature data
    console.log("585")
} else {
    // Default fallback in case the page doesn't match any of the specified pages
    // You might want to handle this according to your application's logic
    features = []; // Set an empty array or default value
}
for (let i = 0; i < features.length; i++) {
let location = features[i].geometry;
if (location) {
    //console.log(location);
    heatArray.push([location.coordinates[1], location.coordinates[0]]);
}

}

let heat = L.heatLayer(heatArray, {
gradient: {
    0: '#ED16B1',
    0.1: '#9916EE',
    0.2: '#1D2FF1',
    0.4: '#00BC5C',
    0.6: '#FDD42E',
    0.8: '#DE1213',
    1: "#9F0132"
},
minOpacity: 0.2,
}).addTo(myMap);

// Separate arrays for each year
let currentYearArray = [];
let year2040Array = [];
let year2070Array = [];
let year2100Array = [];
// Function to update the text content based on the selected year
function updateTextContent(year) {
    // Hide all text elements first
    const textElements = document.querySelectorAll('[id$="-text"]');
    textElements.forEach(element => {
        element.style.display = 'none';
    });

    // Show the selected year text
    const selectedYearText = document.getElementById(`${year}-text`);
    if (selectedYearText) {
        selectedYearText.style.display = 'block';
    }
}

// Function to update the heatmap based on the selected year
function updateHeatmap(map_object,year) {
    // Clear existing heatmap layer
    if (heat) {
        myMap.removeLayer(heat);
    }

    // Clear existing heatmap data arrays
    currentYearArray = [];
    year2040Array = [];
    year2070Array = [];
    year2100Array = [];

    // Loop through each feature and accumulate data for the selected years
    features.forEach(feature => {
        const featureYear = parseInt(feature.properties.year);

        // Check if the feature should be included based on the selected year
        if ((year === '2023' && featureYear <= 2023) ||
            (year === '2040' && featureYear <= 2040) ||
            (year === '2070' && featureYear <= 2070) ||
            (year === '2100' && featureYear <= 2100)) {
        
        let location = feature.geometry;
        
        if (location) {
            const coordinates = [location.coordinates[1], location.coordinates[0]];

            // Accumulate data based on the selected year
            if (year === '2023') {
            currentYearArray.push(coordinates);
            } else if (year === '2040') {
            year2040Array.push(coordinates);
            } else if (year === '2070') {
            year2070Array.push(coordinates);
            } else if (year === '2100') {
            year2100Array.push(coordinates);
            }
        }
        }
    });

    // Combine arrays based on the selected year
    if (year === '2023') {
        heatArray = currentYearArray.slice();
    } else if (year === '2040') {
        heatArray = currentYearArray.concat(year2040Array);
    } else if (year === '2070') {
        heatArray = currentYearArray.concat(year2040Array, year2070Array);
    } else if (year === '2100') {
        heatArray = currentYearArray.concat(year2040Array, year2070Array, year2100Array);
    }
    updateTextContent(year);
    // Create a new heatmap layer with the new data and add it to the map
    heat = L.heatLayer(heatArray, {
        gradient: {
        0: '#ED16B1',
        0.1: '#9916EE',
        0.2: '#1D2FF1',
        0.4: '#00BC5C',
        0.6: '#FDD42E',
        0.8: '#DE1213',
        1: "#9F0132"
        },
        minOpacity: 0.2,
    }).addTo(myMap);
    
    // Get all buttons with the class 'btn' and remove the 'active-button' class
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => button.classList.remove('active-button'));
      
    // Add the 'active-button' class to the clicked button
    const clickedButton = document.getElementById(`btn${year}`);
    clickedButton.classList.add('active-button');
    }
    // Initial heatmap setup (assuming you want to display the "Current" data by default)
    updateHeatmap(myMap,'2023');
