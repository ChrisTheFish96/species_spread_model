# Load required libraries
install.packages("sp")
library(sp)


# Set number of absence points to generate
# Absence points were reduced to 5380
# Set absence data to 20 000
# Coordinates in ocean will be removed so dataset will be reduced
num_absence_points <- 20000

# Import presence data in csv file
# File is created by GBIF_collection_and_cleaning.r
presence_data <- read.csv("CLEANED_S_frugiperda_data.csv")

# Specify which columns contain latitude and longitude coordinates
latitude_column <- "decimalLatitude"
longitude_column <- "decimalLongitude"

# Extract latitude and longitude from the presence data
presence_latitude <- presence_data[, latitude_column]
presence_longitude <- presence_data[, longitude_column]

# Generate random absence points across the entire globe
absence_latitude <- runif(num_absence_points, -200, 200)
absence_longitude <- runif(num_absence_points, -170, 180)

# Create SpatialPoints objects for absence and presence coordinates
absence_coords <- SpatialPoints(cbind(absence_longitude, absence_latitude))
presence_coords <- SpatialPoints(cbind(presence_longitude, presence_latitude))

# Identify which absence coordinates are not in presence coordinates
# Filter absence coordinates based on the condition
# Create a SpatialPointsDataFrame for the absence data
not_in_presence <- !is.na(sp::over(absence_coords, presence_coords))
absence_coords <- absence_coords[!not_in_presence, ]
absence_data <- SpatialPointsDataFrame(coords = absence_coords, data = data.frame(Presence = rep(0, length(absence_coords))))

# Extract coordinates as a matrix
coord_matrix <- coordinates(absence_data)

# Create new columns for latitude and longitude
# Remove the original "coordinates" column
absence_data$Latitude <- coord_matrix[, 1]
absence_data$Longitude <- coord_matrix[, 2]
absence_data$coordinates <- NULL

# Write the data frame to a CSV file
csv_file_path <- "absence_data.csv"
write.csv(absence_data, file = csv_file_path, row.names = FALSE)