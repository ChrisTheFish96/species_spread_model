# Install all needed packages and set up libraries
install.packages("languageserver")
install.packages("devtools")
library(devtools)
install_github("ropensci/CoordinateCleaner")
install.packages("maps")
install.packages("ggplot")
library(CoordinateCleaner)
library(dplyr)
library(ggplot2)
library(sf)

# Read in csv file and add a column for species to be used later
d <- read.csv("bio1.csv", sep=",", header=FALSE)
print(nrow(d))

print(paste0("Number of records: ", nrow(d)))


# Check the column names of data to ensure download was successful
print("Column names:")
colnames(d)

filtered_data <- subset(d, !is.na(Longitude) & (Latitude != ''))
print(paste0("Number of records after filtering:", nrow(filtered_data)))

# Record level checking
# Flag problems using cc_sea and remove them from the dataset
rl <- cc_sea(d,lon="V1", lat="V2", ref=NULL, scale=110, value="clean", speedup=TRUE, verbose=TRUE, buffer=NULL )

print(paste0("Number of records after cleaning: ", nrow(rl)))


# Plot data to get an overview of presence data and to ensure data was cleaned correctly
wm <- borders("world", colour = "gray50", fill = "gray50")
ggplot() +
  coord_fixed() +
  wm +
  geom_point(data = rl,
             aes(x = Longitude, y = Latitude),
             colour = "darkred",
             size = 0.5) +
  theme_bw()


# Create a csv file with the cleaned presence data
file_path <- "future_combined_data/2100/2100_ssp126_cleaned_data.csv"
write.csv(rl, file = file_path, row.names = FALSE)
