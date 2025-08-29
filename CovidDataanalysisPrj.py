import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

CovidData = pd.read_csv(r'C:\Users\user\.cache\kagglehub\datasets\sudalairajkumar\covid19-in-india\versions\237\covid_19_india.csv')
print("Displaying the first few rows of the dataset")
print(CovidData.head())
# Displaying the shape of the dataset
print("Displaying the shape of the dataset")
print(CovidData.shape)

# check for null values
print("Checking for null values in the dataset")
print(CovidData.isnull().sum())

# Dropping rows with null values in specific columns
CovidData = CovidData.dropna(subset=['Sno', 'Time', 'ConfirmedIndianNational', 'ConfirmedForeignNational'])

# Convert date column to datetime format
CovidData['Date'] = pd.to_datetime(CovidData['Date'], format='%Y-%m-%d')

# Finding the active cases
CovidData['Active'] = CovidData['Confirmed'] - (CovidData['Cured'] + CovidData['Deaths'])

# Statewise pivot table
statewise = CovidData.pivot_table(index='State/UnionTerritory', values=['Confirmed', 'Cured', 'Deaths'], aggfunc=np.sum)
# Displaying the first few rows of the statewise DataFrame
print("Displaying the first few rows of the statewise DataFrame")
print(statewise.head(5))

# Finding recovery rate
statewise['Recovery Rate'] = (statewise['Cured'] / statewise['Confirmed']) * 100
# Finding death rate
statewise['Death Rate'] = (statewise['Deaths'] / statewise['Confirmed']) * 100

#Sorting the statewise DataFrame by confirmed  in higher order
statewise = statewise.sort_values(by='Confirmed', ascending=False)
# Displaying the first few rows of the statewise DataFrame after sorting
print("Displaying the first few rows of the statewise DataFrame after sorting")
print(statewise.head(5))


statewise.style.background_gradient(cmap='cubehelix', subset=['Confirmed', 'Cured', 'Deaths', 'Recovery Rate', 'Death Rate'])

# Plotting the data
plt.figure(figsize=(10, 5))
statewise['Confirmed'].plot(kind='bar', color='blue', label='Confirmed Cases')
statewise['Cured'].plot(kind='bar', color='green', label='Cured Cases')
statewise['Deaths'].plot(kind='bar', color='red', label='Death Cases')
plt.title('Statewise COVID-19 Cases in India')
plt.xlabel('States/Union Territories')
plt.ylabel('Number of Cases')
plt.xticks(rotation=90)
plt.legend()
plt.tight_layout()
plt.show()


# Top 10 states with highest active cases
top_10_active = CovidData.groupby('State/UnionTerritory')['Active'].max().nlargest(10)
plt.figure(figsize=(10, 5))
plt.bar(top_10_active.index, top_10_active.values, color='orange')
plt.title('Top 10 States with Highest Active COVID-19 Cases')
plt.xlabel('States/Union Territories')
plt.ylabel('Number of Active Cases')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


#Top 10 statres with highest recovery rate
top_10_recovery = statewise['Recovery Rate'].nlargest(10)
plt.figure(figsize=(10, 5))
ax = sns.barplot(x=top_10_recovery.index, y=top_10_recovery.values, palette='viridis')
plt.title('Top 10 States with Highest Recovery Rate')
plt.xlabel('States/Union Territories')
plt.ylabel('Recovery Rate (%)')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


# Top 10 states with highest death rate
top_10_death = statewise['Death Rate'].nlargest(10)
plt.figure(figsize=(10, 5))
ax = sns.barplot(x=top_10_death.index, y=top_10_death.values, palette='magma')
plt.title('Top 10 States with Highest Death Rate')
plt.xlabel('States/Union Territories')
plt.ylabel('Death Rate (%)')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


# Top 5 highest affected states
top_5_affected = statewise['Confirmed'].nlargest(5)
fig = plt.figure(figsize=(10, 5))
ax = sns.lineplot(data=CovidData[CovidData['State/UnionTerritory'].isin(['Maharashtra', 'Tamil Nadu', 'Karnataka', 'Andhra Pradesh', 'Uttar Pradesh'])],x='Date', y='Confirmed', hue='State/UnionTerritory', palette='Set1', marker='o')
plt.title('Top 5 Most Affected States Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Confirmed Cases')
plt.xticks(rotation=90)
plt.legend(title='States/Union Territories')
plt.tight_layout()
plt.show()



