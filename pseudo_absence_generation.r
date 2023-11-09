# Load required libraries
install.packages("sp")
library(sp)


# Set number of absence points to generate
# Absence points were reduced to 5380
# Set absence data to 20 000
# Coordinates in ocean will be removed so dataset will be reduced
num_absence_points <- 20000

# Import presence data in csv file
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

# Create absence data frame
absence_data <- data.frame(
  Presence = rep(0, num_absence_points),
  Latitude = absence_latitude,
  Longitude = absence_longitude
)

# Write the data frame to a CSV file
csv_file_path <- "absence_data.csv"
write.csv(absence_data, file = csv_file_path, row.names = FALSE)
