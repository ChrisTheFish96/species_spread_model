# Install all needed packages and set up libraries
install.packages("languageserver")
install.packages("devtools")
library(devtools)
install_github("ropensci/CoordinateCleaner")
install.packages("rgbif")
install.packages("rnaturalearth")
install.packages("rnaturalearthdata")
install.packages("countrycode")
install.packages("maps")
install.packages("ggplot")
library(countrycode)
library(CoordinateCleaner)
library(dplyr)
library(ggplot2)
library(rgbif)
library(sf)

# Collect data from GBIF using the taxon key for Spodoptera frugiperda
d <- occ_download_get('0034367-231002084531237') %>%
  occ_download_import()
print(paste0("Number of records downloaded: ", nrow(d)))


# Check the column names of data to ensure download was successful
print("Column names in download:")
colnames(d)

# Select columns of interest and filter out missing values in coordinates
S_frugiperda_GBIF <- d %>%
  dplyr::select("species", "decimalLongitude",
                "decimalLatitude", "countryCode", "individualCount",
                "gbifID", "family", "taxonRank", "coordinateUncertaintyInMeters",
                "year", "basisOfRecord", "institutionCode")
                
filtered_data <- subset(S_frugiperda_GBIF, !is.na(decimalLongitude) & (decimalLatitude != ''))
print(paste0("Number of records afrer filtering:", nrow(filtered_data)))

# Record level checking
# Flag problems using coordinate cleaner and remove them from the dataset
rl <- clean_coordinates(x = filtered_data, 
                        lon = "decimalLongitude", 
                        lat = "decimalLatitude",
                        species = "species",
                        tests = c("centroids",
                                  "equal", "zeros", "gbif", "institutions", "seas", "duplicates"),
                        value = "clean"
                      )
print(paste0("Number of records after cleaning: ", nrow(rl)))

# Dataset level checking
# Checking for coordinate conversion issues and rasterised data
dsl <- clean_dataset(
    rl,
    lon = "decimalLongitude",
    lat = "decimalLatitude",
    ds = "species",
    tests = c("ddmm", "periodicity"),
    verbose = TRUE)

# Plot data to get an overview of presence data and to ensure data was cleaned correctly
wm <- borders("world", colour = "gray50", fill = "gray50")
ggplot() +
  coord_fixed() +
  wm +
  geom_point(data = rl,
             aes(x = decimalLongitude, y = decimalLatitude),
             colour = "darkred",
             size = 0.5) +
  theme_bw()


# Create a csv file with the cleaned presence data
file_path <- "CLEANED_S_frugiperda_data.csv"
write.csv(rl, file = file_path, row.names = FALSE)
