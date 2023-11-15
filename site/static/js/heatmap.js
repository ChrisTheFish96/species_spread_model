    let myMap = L.map("leafletmap", {
        center: [12.107294, 10.228493],
        zoom: 2,
    });
    // let myMap2 = L.map("map2", {
    //     center: [12.107294, 10.228493],
    //     zoom: 1,
    // });
    
    // Adding the tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        minZoom: 1,
        noWrap: true,
    }).addTo(myMap);

    myMap.setMaxBounds(  [[-90,-180],   [90,180]]  )

    // add the same OpenStreetMap tile layer to the second map
    // L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    //     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    //     minZoom: 1,
    //     noWrap: true,
    // }).addTo(myMap2);
    // myMap2.setMaxBounds(  [[-90,-180],   [90,180]]  )
    

        features = spp126_geo_data.features;
    
        let heatArray = [];
    
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
    let year2060Array = [];
    let year2080Array = [];
    let year2100Array = [];

    // Function to update the heatmap based on the selected year
    function updateHeatmap(year) {
        // Clear existing heatmap layer
        if (heat) {
            myMap.removeLayer(heat);
        }

        // Clear existing heatmap data arrays
        currentYearArray = [];
        year2040Array = [];
        year2060Array = [];
        year2080Array = [];
        year2100Array = [];

        // Loop through each feature and accumulate data for the selected years
        features.forEach(feature => {
            const featureYear = parseInt(feature.properties.year);

            // Check if the feature should be included based on the selected year
            if ((year === 'current' && featureYear <= 2023) ||
                (year === '2040' && featureYear <= 2040) ||
                (year === '2060' && featureYear <= 2060) ||
                (year === '2080' && featureYear <= 2080) ||
                (year === '2100' && featureYear <= 2100)) {
            
            let location = feature.geometry;
            
            if (location) {
                const coordinates = [location.coordinates[1], location.coordinates[0]];

                // Accumulate data based on the selected year
                if (year === 'current') {
                currentYearArray.push(coordinates);
                } else if (year === '2040') {
                year2040Array.push(coordinates);
                } else if (year === '2060') {
                year2060Array.push(coordinates);
                } else if (year === '2080') {
                year2080Array.push(coordinates);
                } else if (year === '2100') {
                year2100Array.push(coordinates);
                }
            }
            }
        });

        // Combine arrays based on the selected year
        if (year === 'current') {
            heatArray = currentYearArray.slice();
        } else if (year === '2040') {
            heatArray = currentYearArray.concat(year2040Array);
        } else if (year === '2060') {
            heatArray = currentYearArray.concat(year2040Array, year2060Array);
        } else if (year === '2080') {
            heatArray = currentYearArray.concat(year2040Array, year2060Array, year2080Array);
        } else if (year === '2100') {
            heatArray = currentYearArray.concat(year2040Array, year2060Array, year2080Array, year2100Array);
        }

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
        }

        // Initial heatmap setup (assuming you want to display the "Current" data by default)
        updateHeatmap('current');
