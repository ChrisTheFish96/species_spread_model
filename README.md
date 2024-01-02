# Species spread modelling
For easy access to the site [click here](https://christhefish96.github.io/species_spread_model/). 
## Overall idea:
This was a passion project of mine that aimed to combine science and conventional machine learning tools to create a visual representation of how a pest species distribution can spread due to the effects of climate change.


The target species for this project was *Spodoptera frugiperda* - the fall armyworm.


The fall armyworm is a Lepidopteran pest that feeds on many food crop species. This species have been responsible for losses totalling more than $9 billion per year in Africa alone.


The project was divided into four large parts: data collection, modelling, analysis and visualization. Leaflet maps were created for predictions in 2040, 2070 and 2100 for SSP126, SSP370 and SSP585 climate scenarios.

## Data used:
Occurence data was collected from the Global Biodiversity Information Facility (GBIF).

Current and future climate data was collected in the form of raster files from Climatologies at High resolution for the Earth’s Land Surface Areas (CHELSA).

## General workflow:
1. Collect occurance data from GBIF.
2. Clean occurance data using R's Coordinate Cleaner package. See table below for details on tests.
3. Use R to generate pseudoabsences.
4. Use Coordinate Cleaner to clean absence datapoints
5. Collect environmental variable data (Bio1-Bio19 as well as gdd10 and ngd10 - [See site for more details](https://christhefish96.github.io/species_spread_model/site/data.html#:~:text=ad%20lectus%20posuere.-,Variables,-Auctor%20nisi%20et)).
6. Combine presence and absence data points and randomly shuffle datapoints for model training.
7. Create an Artificual Neural Network (ANN) using paramgrid (Best Hyperparameters: {'activation': 'relu', 'alpha': 0.0001, 'hidden_layer_sizes': (100, 50, 25), 'solver': 'adam'}). [See site for performance details details](https://christhefish96.github.io/species_spread_model/site/modelling.html#:~:text=of%20trees%3A%20200-,ANN%20Performance,-Overall%20accuracy%3A%200.9611). 
8. Create a Random forest Regression (RFR) using pramgrid (Best Hyperparameters: {'max_depth': None, 'max_features': 'sqrt', 'min_samples_leaf': 1, 'min_samples_split': 5, 'n_estimators': 200}). [See site for performance details](https://christhefish96.github.io/species_spread_model/site/modelling.html#:~:text=1051-,RFR%20Performance,-Overall%20accuracy%3A%200.9647).
9. Because the models preformed similarly on the test data, I chose the RFR to predict future spread as it provides feature importances which will allow me to scale down the biovariables. For this project I chose all variables with a [feature importance above 0.05](https://christhefish96.github.io/species_spread_model/site/assets/img/Feature%20importances.png).
10. After creating my predictions using my RFR model, I used QGIS with a mask of South Africa to extract the predicted presence data for each year I was interested in (2040, 2070, and 2100) for every climate scenario.
11. This data was then converted into geoJSON data to be used in a variety of Leaflet maps.


#### Tests in Coordinate Cleaner:

| Test          |Description                                                                            |
|---------------|---------------------------------------------------------------------------------------|
| centroids     |tests a radius around country centroids                                                |
| equal         |tests for equal absolute longitude and latitude                                        |
| zeros         |tests for plain zeros, equal latitude and longitude and a radius around the point 0/0  |
| gbif          |tests a one-degree radius around the GBIF headquarters in Copenhagen, Denmark          |
| institutions  |tests a radius around known biodiversity institutions                                  |
| seas          |tests if coordinates fall into the ocean                                               |
| duplicates    |tests for duplicate records                                                            |

## Tech stack used:
* R (version 4.3.2)
* Python (version 3.12.1)
* SciKit Learn (version 1.3.2)
* QGIS (version 3.34.1)
* Leaflet (version 1.9.4)
* D3 (version 7.8.5)
* Bootstrap
* JavaSript
* CSS
* HTML5

## What I learned:
* How to obtain and filter data from GBIF.
* How to use the Coordinate Cleaner R library to flac and remove potential problems in the coordinates from the obtained data.
* How to create pseudoabsences for data in R.
* Finding the best hyperparameters for model creation.
* Saving a trained model and then calling it when prediction need to be made on different data.
* Became more familiar with hyperparameter tuning
* Learned to work in QGIS with masks and raster files.
* Became more comfortable using GDAL to extract XYZ data from raster files for later use as csv files
