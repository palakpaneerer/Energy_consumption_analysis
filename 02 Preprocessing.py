# Data Preprocessing Script 2
# This code checks for missing values in 578 substations with location information 
# identified during 01 preprocessing.

# Task 1: Set missing value tolerances to 5%, 10%, and 15% and create lists of substations 
# that meet each tolerance.
# Task 2: Visualise trends in missing values graphically.

# Import necessary libraries
import numpy as np
import pandas as pd
import os
from tqdm import tqdm  # For progress tracking
import missingno as msno  # For missing value visualization

# Task 1: Set missing value tolerances to 5%, 10%, and 15% and create lists of substations 
# that meet each tolerance.

# Set missing value tolerances
missing_value_tolerance5per = 0.05
missing_value_tolerance10per = 0.1
missing_value_tolerance15per = 0.15

# Set the relative path from the current working directory
relative_path = "Output"

# Change the working directory to the subfolder
os.chdir(relative_path)

# Read the CSV file containing information about substations with location data into a DataFrame
df_substation_with_location = pd.read_csv('substations_with_location.csv', index_col=None, header=None)

# Set the column name to "SubstationName"
df_substation_with_location.columns = ["SubstationName"]

# Append ".csv" to each cell value in the SubstationName column
df_substation_with_location['SubstationName'] = df_substation_with_location['SubstationName'].apply(lambda x: x + '.csv')

# Change back to the parent folder
os.chdir("..")

# Set the relative path to the "Big_Data" subfolder
relative_path = "Big_Data"

# Change the working directory to the subfolder
os.chdir(relative_path)

# Initialize various lists and DataFrames
list_use_5per = []
list_use_10per = []
list_use_15per = []
df_master_5per = pd.DataFrame()
df_master_10per = pd.DataFrame()
df_master_15per = pd.DataFrame()

# Loop through each CSV file and perform data preprocessing
for i in tqdm(np.arange(len(df_substation_with_location['SubstationName']))):
    df = pd.read_csv(df_substation_with_location['SubstationName'][i], index_col='times')
    df.index = pd.to_datetime(df.index)
    df_assetID = pd.pivot_table(df, values='Active_Power', index='times', columns='AssetID')

    # Resample substation data on an hourly basis
    df_hourly = df_assetID.resample("H").first()

    # Define the period as from January 2021 to December 2022
    P = pd.date_range(start='2021-01', end='2022-12-31 23:00:00', freq='H')
    df_period = df_hourly.reindex(P)

    # Sum the power consumption (kWh) of each AssetID
    # to represent total power consumption of a substation.
    df_period_total = df_period.sum(axis=1)
    df_period_total = df_period_total.replace(0, np.nan)

    # Count the number of NaN values for each substation
    n_missing = df_period_total.isna().sum()

    # Count the total number of data values
    n_values = df_period_total.count()

    # Calculate the ratio of values to total values (1 - missing value ratio)
    value_ratio = n_values / (n_missing + n_values)

    # If the missing value ratio is within tolerance, add the substation name to the list
    if value_ratio >= (1 - missing_value_tolerance5per):
        list_use_5per.append(str(df_substation_with_location['SubstationName'][i]))
        col = os.path.splitext(df_substation_with_location['SubstationName'][i])[0]
        df_master_5per[col] = df_period_total

    if value_ratio >= (1 - missing_value_tolerance10per):
        list_use_10per.append(str(df_substation_with_location['SubstationName'][i]))
        col = os.path.splitext(df_substation_with_location['SubstationName'][i])[0]
        df_master_10per[col] = df_period_total

    if value_ratio >= (1 - missing_value_tolerance15per):
        list_use_15per.append(str(df_substation_with_location['SubstationName'][i]))
        col = os.path.splitext(df_substation_with_location['SubstationName'][i])[0]
        df_master_15per[col] = df_period_total

# Display the number of substations within each tolerance
print("Number of substations with less than 5% missing value:", len(df_master_5per.columns))
print("Number of substations with less than 10% missing value:", len(df_master_10per.columns))
print("Number of substations with less than 15% missing value:", len(df_master_15per.columns))

# Result 1:
#5%: 224 substations
#10%: 380 substations
#15%: 480 substations


# Task 2: Visualize the trends in missing values
msno.matrix(df_master_5per)
msno.matrix(df_master_10per)
msno.matrix(df_master_15per)

# Result 2: Missing values tend to be concentrated around the beginning of the 2021 data.

# Save the DataFrames with missing value tolerances to CSV files
# Return to the parent folder
os.chdir("..")  

# Set the relative path to the "Output" subfolder
relative_path = "Output"

# Change the working directory to the subfolder
os.chdir(relative_path)

# Save DataFrames to CSV files without index
df_master_5per.to_csv('df_master_5per.csv')
df_master_10per.to_csv('df_master_10per.csv')
df_master_15per.to_csv('df_master_15per.csv')
