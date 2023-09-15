# Data Preprocessing Script 1
# This script serves two main purposes:
# Task 1: Count the total number of substations.
# Task 2: Identify the number of substations that have location data.
# It operates on CSV files containing Power Data for each substation and a CSV file containing location information.

# Import necessary libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# Task 1: Count the total number of substations.

# Specify the directory where the substation data is located.
# There is a subfolder named "Big_Data" containing substation data.
# Using a relative path from the current working directory.
relative_path = "Big_Data"

# Change the working directory to the subfolder.
os.chdir(relative_path)

# List all files in the directory.
list_files = os.listdir("./")

# Initialize an empty list to store CSV file names.
list_csv = []

# Iterate through the files and add CSV files to the list.
for file_name in list_files:
    if file_name.endswith(".csv"):
        list_csv.append(file_name)

# Display the number of substations.
print("Task 1: Counting Substations")
print("Number of substations:", len(list_csv))
# Result 1: There are 613 substation data files in total.


# Task 2: Identify the number of substations that have location data.

# Change the working directory to the parent directory.
os.chdir("..")

# Use a relative path from the current working directory.
relative_path = "Substations_Location"

# Change the working directory to the subfolder.
os.chdir(relative_path)

# Read the CSV file containing location information.
substations_location = pd.read_csv('LEP_Coords.csv')

# Extract the 'SubstationName' column from the location information.
substations_location = substations_location["SubstationName"]

# Get substation names from the folder with Big Data.
substations_from_Big_Data = []

# Remove .csv from each element and add to the new list.
for item in list_csv:
    filename = item.split(".csv")[0]
    substations_from_Big_Data.append(filename)

# Convert substations_from_Big_Data and substations_location to sets.
set_from_Big_Data = set(substations_from_Big_Data)
set_from_Substations_Location = set(substations_location)

# Extract elements common to both sets.
substations_with_location = set_from_Big_Data.intersection(set_from_Substations_Location)

# Display the count of substations with location data.
print("Task 2: Identifying Substations with Location Data")
print("Number of substations with location data:", len(substations_with_location))
# Result 2: There are 578 substations with location data.

# Save the list of substations with location data to a file.

# Change the working directory to the parent directory.
os.chdir("..")

# Use a relative path from the current working directory.
relative_path = "Output"

# Change the working directory to the subfolder.
os.chdir(relative_path)

# Convert substations_with_location list to a DataFrame.
df = pd.DataFrame(substations_with_location)

# Save the DataFrame to a CSV file without index.
df.to_csv('substations_with_location.csv', index=False, header=False)

print(f'substations_with_location has been saved to {relative_path} folder')
