# Sensitivity Analysis
# This code compares power consumption trends of each dataframe 
# with different missing value tolerances (0%, 5%, 10%, 15%).
# Task 1: Fill missing values in each dataframe with average daily energy consumption
# for the month.
# Task 2: Calculate the monthly average for all substations in each dataframe.
# Task 3: Visualize the results to decide which dataframe to use for further analysis.

#必要なライブラリーのインポート
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import seaborn as sns



# Task 1: Fill missing values in each dataframe with average daily energy consumption
# for the month.

# Set the relative path to the "Output" subfolder
relative_path = "Output"

# Change the working directory to the subfolder
os.chdir(relative_path)

# Import each DataFrame
df_master_5per = pd.read_csv('df_master_5per.csv')
df_master_10per = pd.read_csv('df_master_10per.csv')
df_master_15per = pd.read_csv('df_master_15per.csv')

# Naming the columns for time data
df_master_5per = df_master_5per.rename(columns={'Unnamed: 0': 'times'})
df_master_10per = df_master_10per.rename(columns={'Unnamed: 0': 'times'})
df_master_15per = df_master_15per.rename(columns={'Unnamed: 0': 'times'})

# Set the 'times' column as the index
df_master_5per = df_master_5per.set_index('times')
df_master_10per = df_master_10per.set_index('times')
df_master_15per = df_master_15per.set_index('times')


# Convert the index to datetime type
df_master_5per.index = pd.to_datetime(df_master_5per.index)
df_master_10per.index = pd.to_datetime(df_master_10per.index)
df_master_15per.index = pd.to_datetime(df_master_15per.index)


# Create a DataFrame with 0% missing values
df_master_0per = df_master_5per.dropna(axis=1, how='any')


# Fill missing values in each dataframe with average daily energy consumption for the month.
df_master_5per = df_master_5per.groupby(df_master_5per.index.month).transform(lambda x: x.fillna(x.mean()))
df_master_10per = df_master_10per.groupby(df_master_10per.index.month).transform(lambda x: x.fillna(x.mean()))
df_master_15per = df_master_15per.groupby(df_master_15per.index.month).transform(lambda x: x.fillna(x.mean()))


# Task 2: Calculate the monthly average for all substations in each dataframe.

# Convert power consumption units from kWh to MWh
df_master_0per = df_master_0per / 1000
df_master_5per = df_master_5per / 1000
df_master_10per = df_master_10per / 1000
df_master_15per = df_master_15per / 1000


# Calculate daily power consumption for each DataFrame, 
# then calculate monthly average daily power consumption
df_master_0per = df_master_0per.resample("D").sum()
df_master_0per = df_master_0per.resample("M").mean()
df_master_5per = df_master_5per.resample("D").sum()
df_master_5per = df_master_5per.resample("M").mean()
df_master_10per = df_master_10per.resample("D").sum()
df_master_10per = df_master_10per.resample("M").mean()
df_master_15per = df_master_15per.resample("D").sum()
df_master_15per = df_master_15per.resample("M").mean()


# Save DataFrames to CSV files without index
df_master_5per.to_csv('df_master_5per.csv')
df_master_10per.to_csv('df_master_10per.csv')
df_master_15per.to_csv('df_master_15per.csv')



#Calculate the monthly average for all substations in each dataframe.
df_master_0per = df_master_0per.mean(axis=1)
df_master_5per = df_master_5per.mean(axis=1)
df_master_10per = df_master_10per.mean(axis=1)
df_master_15per = df_master_15per.mean(axis=1)



# Task 3: Visualise the results to decide which dataframe to use for further analysis.

# Visualize each DataFrame
sns.lineplot(data=df_master_0per,marker="o",label="0%")
sns.lineplot(data=df_master_5per,marker="o",label="5%")
sns.lineplot(data=df_master_10per,marker="o",label="10%")
sns.lineplot(data=df_master_15per,marker="o",label="15%")

# Set the plot title and labels
plt.title("Difference due to Missing values tolerance",fontweight='bold')
plt.ylabel("Daily energy consumption (MWh)",fontweight='bold')
plt.xlabel("Month",fontweight='bold')
plt.grid(True)
plt.ylim(1000, 3000)
plt.yticks(np.linspace(1000, 3000, 5))
plt.xticks(fontweight='bold',rotation=90)
plt.yticks(fontweight='bold')
plt.legend(loc='lower left')
plt.show()

# Result 3: In terms of trends, even with a 15% missing value tolerance, 
# there are no significant different trends. Therefore, I will analyse 
# using the DataFrame containing 15% missing values for future analysis.


