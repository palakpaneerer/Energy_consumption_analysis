# Linear Regression
# This code studies if there is a correlation between CPIH and power consumption.
# Since the correlation between temperature and electricity usage is very strong, I will use multiple regression analysis to remove its influence.
# Examine this correlation for each group to find out which category groups changed their electricity consumption behaviour due to the cost of living crisis.

# Task 1: Load the Excel file
# Task 2: Examine the correlation between the average power consumption 
# for all substations and CPIH.
# Task 3: Save the results to a dataframe
# Task 4: Visualise the fit of the model using a graph.
# Task 5: Examine the correlation between average power consumption for each category 
# and CPIH. Save the results to the dataframe.


# Import the required libraries
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import os


# Task 1: Load the Excel file
# Set the relative path to the "Output" subfolder
relative_path = "Output"

# Change the working directory to the subfolder
os.chdir(relative_path)

# Import each DataFrame
df_master_15per = pd.read_csv('df_master_15per.csv', index_col="times")
df_master_15per.index = pd.to_datetime(df_master_15per.index)
df_master_15per.index = df_master_15per.index.strftime('%Y-%m')
df_class = pd.read_csv('Classification.csv', index_col="SubstationName")

# Return to the parent folder
os.chdir("..")  

# Set the relative path to the "Inflation" subfolder
relative_path = "Inflation"

# Change the working directory to the subfolder
os.chdir(relative_path)

# Import each DataFrame
df_cpih = pd.read_excel('CPIH.xlsx', index_col="Month")
df_cpih.index = df_cpih.index.strftime('%Y-%m')
# Return to the parent folder
os.chdir("..")  

# Set the relative path to the "Temperature" subfolder
relative_path = "Temperature"

# Change the working directory to the subfolder
os.chdir(relative_path)

# Import each DataFrame
df_temperature = pd.read_excel('Temperature.xlsx', index_col="Month")
df_temperature.index = df_temperature.index.strftime('%Y-%m')


# Task 2: Examine the correlation between the average power consumption 
# for all substations and CPIH.

# Create a data frame of average power　consumption for all substations
df_average = df_master_15per.mean(axis=1)
df_average = pd.DataFrame(df_average)
df_average = df_average.rename(columns={0: 'Avergae power consumption'})


# Set the relevant columns for regression
data = {
        'x1': df_cpih['CPIH'],
        'x2': df_temperature['Average Temperature'],
        'y': df_average['Avergae power consumption']
        }

df = pd.DataFrame(data)

# Define explanatory variables
X = df[['x1', 'x2']]

# Add constant term (to include intercept)
X = sm.add_constant(X)

# Define target variable
Y = df['y']

# Create multiple regression model
model = sm.OLS(Y, X).fit()

# Show model summary
print(model.summary())

# Result 2: Can not be disclosed

# Task 3: Save the results to a data frame
# Create a result DataFrame
# Create a list of column names
column_names = [
                "Category", 
                "P-value for CPIH", 
                "coef for CPIH", 
                "P-value for temp", "coef for temp"
                ]

# Create a Result data frame
df_result = pd.DataFrame(columns=column_names)

# Extract model results
category = "All substations"
p_value_cpih = model.pvalues['x1']
coef_cpih = model.params['x1']
p_value_temp = model.pvalues['x2']
coef_temp = model.params['x2']

# Add the extracted results to the data frame
df_result.loc[0] = [category, p_value_cpih, coef_cpih, p_value_temp, coef_temp]




# Task 4: Visualise the fit of the model using a graph.
# Extract the predicted values
predicted_values = model.predict(X)

# Plot the actual values and predicted values
plt.figure(figsize=(10, 6))
plt.plot(df.index, Y, label='Actual')
plt.plot(df.index, predicted_values, label='Predicted')
plt.xlabel('Month')
plt.ylabel('Average power consumption')
plt.title('Multiple Linear Regression')
plt.xticks(rotation=90)
plt.grid()
plt.legend()
plt.show()


# Task 5: Examine the correlation between average power consumption for each category 
# and CPIH. Save the results to the dataframe.

# Write all conditions
conditions = {
                'Income Group Low': df_class[df_class['Income Group'] == 'Low'],
                'Income Group Medium': df_class[df_class['Income Group'] == 'Medium'],
                'Income Group High': df_class[df_class['Income Group'] == 'High'],
                'Deprivation Group Low': df_class[df_class['Deprivation Group'] == 'Low'],
                'Deprivation Group Medium': df_class[df_class['Deprivation Group'] == 'Medium'],
                'Deprivation Group High': df_class[df_class['Deprivation Group'] == 'High'],
                'rural/urban Group rural': df_class[df_class['rural/urban Group'] == 'Rural'],
                'rural/urban Group urban': df_class[df_class['rural/urban Group'] == 'Urban'],
                'Retired Population Group Low': df_class[df_class['Retired Population Group'] == 'Low'],
                'Retired Population Group Medium': df_class[df_class['Retired Population Group'] == 'Medium'],
                'Retired Population Group High': df_class[df_class['Retired Population Group'] == 'High'],
                'Age Group Low': df_class[df_class['Age Group'] == 'Low'],
                'Age Group Medium': df_class[df_class['Age Group'] == 'Medium'],
                'Age Group High': df_class[df_class['Age Group'] == 'High'],
                'Gas Group Low': df_class[df_class['Gas Group'] == 'Low'],
                'Gas Group High': df_class[df_class['Gas Group'] == 'High'],
                'EPC Group Low': df_class[df_class['EPC Group'] == 'Low'],
                'EPC Group Medium': df_class[df_class['EPC Group'] == 'Medium'],
                'EPC Group High': df_class[df_class['EPC Group'] == 'High'],
                }

# Defined to specify the Row of the dataframe that saves the results in
i = 1

for key, value in conditions.items():
    # Extract information only for substations in the selected category
    selected_substation_data = df_master_15per.loc[:, value.index]
    
    # Update the y value for multiple regression analysis
    df['y'] = selected_substation_data.mean(axis=1)

    # Define explanatory variables
    X = df[['x1', 'x2']]

    # Add constant term (to include intercept)
    X = sm.add_constant(X)

    # Define target variable
    Y = df['y']

    # Create multiple regression model
    model = sm.OLS(Y, X).fit()
    
    # Extract the necessary information from the model results
    category = key
    p_value_cpih = model.pvalues['x1']
    coef_cpih = model.params['x1']
    p_value_temp = model.pvalues['x2']
    coef_temp = model.params['x2']

    # Add the extracted information to the dataframe
    df_result.loc[i] = [category, p_value_cpih, coef_cpih, p_value_temp, coef_temp]
    
    # Update i that specify the Row of the dataframe where the results will be saved in
    i += 1

# Result5: Can not be disclosed.