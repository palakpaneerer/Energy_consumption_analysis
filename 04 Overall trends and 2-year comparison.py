#Overall trends and 2-year comparison
#This code checks CPIH trends from 2021 to 2022.
#Task 1: Check CPIH trends in a graphic manner.
#Task 2: Check the trends in electricity usage using paired t-tests 
#        to see if there are any differences in consumption trends over the two years.


#Import the required libraries
import matplotlib.pyplot as plt
import pandas as pd
import os
import seaborn as sns
from scipy import stats
import matplotlib.ticker as mtick


#Task 1: Check CPIH trends in a graphic manner.
# Set the relative path to the "Inflation" subfolder
relative_path = "Inflation"

# Change the working directory to the subfolder
os.chdir(relative_path)

# Import each DataFrame
CPIH = pd.read_excel('CPIH.xlsx', index_col="Month")


# Visuarise CPIH trend
sns.lineplot(CPIH)
plt.title("Electricity and CPIH inflation rates", fontweight='bold')
plt.ylabel("Annual inflation rates (%)", fontweight='bold')
plt.xlabel("Year", fontweight='bold')
plt.xticks(rotation=90, fontweight='bold')
plt.yticks(fontweight='bold')
plt.legend(loc='upper left')
fmt = '%.0f%%'  
yticks = mtick.FormatStrFormatter(fmt)
plt.gca().yaxis.set_major_formatter(yticks)
plt.grid(True)  
plt.show()
#Result 1: CPIH continueed to rise rapidly from January 2021 to December 2022.


#Task 2: Check the trends in electricity usage using paired t-tests 
#        to see if there are any differences in consumption trends over the two years.

# Return to the parent folder
os.chdir("..")  
# Set the relative path to the "Output" subfolder
relative_path = "Output"

# Change the working directory to the subfolder
os.chdir(relative_path)

# Import each DataFrame
df_master_15per = pd.read_csv('df_master_15per.csv',index_col="times")


# Seperate the periods
df_2021 = df_master_15per.iloc[:12]
df_2022 = df_master_15per.iloc[12:]

# Sum the power consumption for each substation
df_2021 = df_2021.sum(axis=0)
df_2022 = df_2022.sum(axis=0)


# Make a histgram
sns.histplot(data=df_2021, alpha=0.5, bins=30, kde=True, edgecolor=(0, 0, 0, 0.5),label='2021 Data')
sns.histplot(data=df_2022, alpha=0.5, bins=30, kde=True, edgecolor=(0, 0, 0, 0.5),label='2022 Data')
plt.title("Distribution of substations",fontweight='bold')
plt.xlabel("Annual energy consumption(MWh)",fontweight='bold')
plt.ylabel("Number of substations",fontweight='bold')
plt.xticks(fontweight='bold')
plt.yticks(fontweight='bold')
plt.grid(True)
plt.legend()
plt.show()

# Peformed paired t-test
t_statistic, p_value = stats.ttest_rel(df_2021,df_2022)
print("t_value = ", t_statistic)
print("p_value = ", p_value)
if p_value < 0.05:
    print("Statistically significant difference\n")
else:
    print("No statistically significant difference\n")
#Reult 2: Can not be disclosed

