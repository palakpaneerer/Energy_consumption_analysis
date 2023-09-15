# Classification
# This code uses regional population characteristics data for each substation to determine the attribute class for each substation.
# Task 1: Set the threshold in the function.
# Task 2: Apply the functions to classify substations.
# Task 3: Check how many substations belong to each class


# Import the required libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


# Set the relative path to the "Gis_Data" subfolder
relative_path = "Gis_Data"

# Change the working directory to the subfolder
os.chdir(relative_path)

# Import each DataFrame
df = pd.read_excel('Index each substation.xlsx')

# Task 1: Set the threshold in the function.
df["Average Income(£)"].iloc[0] = df["Average Income(£)"].iloc[0].replace("\u202f","")
for i in np.arange(len(df["Average Income(£)"])):
    df["Average Income(£)"].iloc[i] = df["Average Income(£)"].iloc[i].replace("\u202f","")
df["Average Income(£)"] = df["Average Income(£)"].astype(int)

def group_income(x):
    if x <= 29999:
        return "Low"
    elif x <= 34999:
        return "Medium"
    else:
        return "High"
    
def group_Deprivation(x):
    if x <= 2:
        return "Low"
    elif x <= 8:
        return "Medium"
    else:
        return "High"

def group_rural_urban(x):
    if x == 1:
        return "Rural"
    else:
        return "Urban"

def group_Retired_Population(x):
    if x <= 10:
        return "Low"
    elif x <= 30:
        return "Medium"
    else:
        return "High"
    
def group_Average_Age(x):
    if x <= 40:
        return "Low"
    elif x <= 45:
        return "Medium"
    else:
        return "High"

def group_Gas(x):
    if x <= 50:
        return "Low"
    else:
        return "High"
    
def group_EPC(x):
    if x <= 35:
        return "Low"
    elif x <= 60:
        return "Medium"
    else:
        return "High"  
    
# Task 2: Apply the functions to classify substations.
df["Income Group"] = df["Average Income(£)"].apply(group_income)
df["Deprivation Group"] = df["Deprivation"].apply(group_Deprivation)
df["rural/urban Group"] =df["rural(1)/urban(2)"].apply(group_rural_urban)
df["Retired Population Group"] = df["Retired Population (%)"].apply(group_Retired_Population)
df["Age Group"] = df["Average Age"].apply(group_Average_Age)
df["Gas Group"] = df["Non Gas Properties(%)"].apply(group_Gas)
df["EPC Group"] = df["EPC Rating above C(%)"].apply(group_EPC)

df = df[['SubstationName', 'Income Group', 'Deprivation Group', 'rural/urban Group',
       'Retired Population Group', 'Age Group', 'Gas Group', 'EPC Group']]


# Task 3: Check how many substations belong to each class
columns_to_plot = df.columns[1:]

# Draw graphs for each group
for column in columns_to_plot:
    column_counts = df[column].value_counts()
    
    plt.figure(figsize=(8, 6))
    column_counts.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title(f'{column} Counts')
    plt.xlabel(column)
    plt.ylabel('Count')
    plt.xticks(rotation=0)  # X軸のラベルを水平に表示
    plt.tight_layout()
    plt.grid()
    plt.show()
# Result 3: Can not be disclosed



# Return to the parent folder
os.chdir("..")  
# Set the relative path to the "Output" subfolder
relative_path = "Output"

# Change the working directory to the subfolder
os.chdir(relative_path)

# Save data frame
df.to_csv("Classification.csv", index=False)