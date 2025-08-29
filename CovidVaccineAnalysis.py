import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

Covid_Vaccine_Data = pd.read_csv(r'C:\Users\user\.cache\kagglehub\datasets\gpreda\covid-world-vaccination-progress\versions\249\country_vaccinations.csv')
print("Displaying the first few rows of the dataset")
print(Covid_Vaccine_Data.head(10))

print("Checking for null values in the dataset")
print(Covid_Vaccine_Data.isnull().sum())

# Dropping rows with null values in specific columns
print("Dropping rows with null values in specific columns")
Covid_Vaccine_Data.dropna(
    subset=[
        'country',
        'date',
        'total_vaccinations',
        'people_vaccinated',
        'people_fully_vaccinated',
        'daily_vaccinations_raw',
        'source_website' 
    ],
    inplace=True
)
# Displaying the columns of the dataset
print("Displaying the columns of the dataset")
print(Covid_Vaccine_Data.columns.tolist())

# Displaying the first few rows of the dataset after dropping null values
print("Displaying the first few rows of the dataset after dropping null values")
print(Covid_Vaccine_Data.head(5))
# Displaying the shape of the dataset
print("Displaying the shape of the dataset")
print(Covid_Vaccine_Data.shape)


#Storing new dataframe with only required columns in a new df
new_df = Covid_Vaccine_Data[['country', 'date', 'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated', 'daily_vaccinations_raw', 'source_website']]
# Displaying the first few rows of the new DataFrame
print("Displaying the first few rows of the new DataFrame")
print(new_df.head(5))
# Displaying the shape of the new DataFrame
print("Displaying the shape of the new DataFrame")  
print(new_df.shape)


# Convert 'date' column to datetime format
new_df['date'] = pd.to_datetime(new_df['date'], format='%Y-%m-%d')

# Group by country and date, summing the total vaccinations
Countrywise = new_df.pivot_table(
    index='country',
    values=['total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated', 'daily_vaccinations_raw'],
    aggfunc=max
)
#Displaying the first few rows of the Countrywise DataFrame
print("Displaying the first few rows of the Countrywise DataFrame")
print(Countrywise.head())

# Calculate the percentage of people vaccinated and fully vaccinated of new DataFrame
Countrywise['people_vaccinated_per_hundred'] =  ((Countrywise['people_vaccinated'] / Countrywise['total_vaccinations']) * 100).astype(int)
Countrywise['people_fully_vaccinated_per_hundred'] = ((Countrywise['people_fully_vaccinated'] / Countrywise['total_vaccinations']) * 100).astype(int)


# Sort the DataFrame by total number of  vaccinations
Countrywise = Countrywise.sort_values(by='total_vaccinations', ascending=False)


# Display the top 10 countries with the highest total vaccinations
print("Displaying the top 10 countries with the highest total vaccinations")
print(Countrywise.head(10))


formatter = plt.FuncFormatter(lambda x, _: f'{int(x):,}')  # Format y-axis with commas

# Plotting the top 10, people vaccinated vs fully vaccinated
top_10_countries = Countrywise.head(10)

plt.figure(figsize=(10, 5))
top_10_countries['people_vaccinated'].plot(kind='bar', color='green', label='People Vaccinated')
top_10_countries['people_fully_vaccinated'].plot(kind='bar', color='red', label='People Fully Vaccinated')

# Dispay the value on yaxis above the bar
for i, v in enumerate(top_10_countries['people_vaccinated']):
    plt.text(i, v + 0.05 * v, f'{int(v):,}', ha='center', va='bottom')
plt.gca().yaxis.set_major_formatter(formatter)

plt.title('Top 10 Countries with Highest COVID-19 Vaccinations')
plt.xlabel('Countries')
plt.ylabel('Number of Vaccinations')
plt.xticks(rotation=90)
plt.legend()
plt.tight_layout()
plt.show()

# plot the percentage of people getting vaccicnated daily
plt.figure(figsize=(10, 5))
top_10_countries['daily_vaccinations_raw'].plot(kind='bar', color='purple', label='Daily Vaccinations Raw')
 
# Dispay the value on yaxis above the bar
for i, v in enumerate(top_10_countries['daily_vaccinations_raw']):
    plt.text(i, v + 0.05 * v, f'{int(v):,}', ha='center', va='bottom')
plt.gca().yaxis.set_major_formatter(formatter)


plt.title('Top 10 Countries with Highest Daily COVID-19 Vaccinations')
plt.xlabel('Countries')
plt.ylabel('Number of Daily Vaccinations')
plt.xticks(rotation=90)
plt.legend()
plt.tight_layout()
plt.show()


# Display the top 10 countries with the highest percentage of people vaccinated
top_10_vaccinated = Countrywise.nlargest(10, 'people_vaccinated_per_hundred')
plt.figure(figsize=(10, 5))
ax = sns.barplot(x=top_10_vaccinated.index, y=top_10_vaccinated['people_vaccinated_per_hundred'], palette='viridis')
plt.title('Top 10 Countries with Highest Percentage of People Vaccinated')
plt.xlabel('Countries')
plt.ylabel('Percentage of People Vaccinated (%)')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


# Get the number of sources for vaccination data
source_counts = new_df['source_website'].value_counts()
#Display the top 10 sources for vaccination data
print("Displaying the top 10 sources for vaccination data")
print(source_counts.head())


#Get the number of peoople vaccinated each year

new_df['year'] = new_df['date'].dt.year
yearly_vaccinations = new_df.groupby('year')['people_vaccinated'].max().reset_index() #Grouping the culumative data
yearly_vaccinations['people_vaccinated'] = yearly_vaccinations['people_vaccinated']
# Displaying the first few rows of the yearly vaccinations DataFrame
print("Displaying the first few rows of the yearly vaccinations DataFrame")
print(yearly_vaccinations.head())


# Plotting the yearly vaccinations
plt.figure(figsize=(8, 5))
plt.plot(yearly_vaccinations['year'], yearly_vaccinations['people_vaccinated'], marker='o', linestyle='-', color='purple')

# dispay the value on yaxis above the line
for i, v in enumerate(yearly_vaccinations['people_vaccinated']):
    plt.text(yearly_vaccinations['year'][i], v + 0.05 * v, f'{int(v):,}', ha='center', va='bottom')
plt.gca().yaxis.set_major_formatter(formatter)

plt.xticks(yearly_vaccinations['year'], rotation=45)
plt.title('Yearly COVID-19 Vaccinations')
plt.xlabel('Year')
plt.ylabel('Number of People Vaccinated')
plt.grid(True)
plt.tight_layout()
plt.show()






