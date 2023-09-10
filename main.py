import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
smoking_data = pd.read_csv("smoking.csv")

# -----------------------
# 1. Trend Analysis
# -----------------------

# Calculate the difference in smoking percentage between the first and last year for each country
smoking_data_grouped = smoking_data.groupby('Country').agg({'Year': ['min', 'max'], 'Data.Percentage.Total': ['first', 'last']})
smoking_data_grouped.columns = ['Year_start', 'Year_end', 'Percentage_start', 'Percentage_end']
smoking_data_grouped['Percentage_change'] = smoking_data_grouped['Percentage_end'] - smoking_data_grouped['Percentage_start']

# Sort countries by the most significant increase and decrease
increased_smoking = smoking_data_grouped.sort_values('Percentage_change', ascending=False).head(5)
decreased_smoking = smoking_data_grouped.sort_values('Percentage_change', ascending=True).head(5)

# Trend Analysis Visuals
sns.set_style("whitegrid")  # Setting a grid style for the plots
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 12))

# Countries with the most significant increase
sns.barplot(x=increased_smoking.index, y='Percentage_change', data=increased_smoking, ax=axes[0], palette="Blues_d")
axes[0].set_title('Top 5 Countries with Most Significant Increase in Smoking Percentage (1980-2012)')
axes[0].set_ylabel('Percentage Point Increase')

# Countries with the most significant decrease
sns.barplot(x=decreased_smoking.index, y='Percentage_change', data=decreased_smoking, ax=axes[1], palette="Reds_d")
axes[1].set_title('Top 5 Countries with Most Significant Decrease in Smoking Percentage (1980-2012)')
axes[1].set_ylabel('Percentage Point Decrease')

# Adjust layout and display
plt.tight_layout()
plt.show()

# -----------------------
# 2. Gender Disparity Analysis
# -----------------------

# Filter data for the year 2012
latest_year_data = smoking_data[smoking_data['Year'] == 2012]

# Calculate the gender disparity
latest_year_data['Gender_Disparity'] = latest_year_data['Data.Percentage.Male'] - latest_year_data['Data.Percentage.Female']

# Sort by gender disparity for the top 5 countries
gender_disparity_sorted = latest_year_data[['Country', 'Gender_Disparity']].sort_values('Gender_Disparity', ascending=False).head(5)

# Gender Disparity Visuals
plt.figure(figsize=(10, 6))
sns.barplot(x='Country', y='Gender_Disparity', data=gender_disparity_sorted, palette="coolwarm_r")
plt.title('Top 5 Countries with Highest Gender Disparity in Smoking (2012)')
plt.ylabel('Difference in Percentage Points (Male - Female)')
plt.xticks(rotation=45)
plt.show()

# -----------------------
# 3. Intensity Analysis
# -----------------------

# Sort countries by daily cigarettes smoked in 2012 for the top 5 countries
intensity_sorted = latest_year_data[['Country', 'Data.Daily cigarettes']].sort_values('Data.Daily cigarettes', ascending=False).head(5)

# Intensity Analysis Visuals
plt.figure(figsize=(10, 6))
sns.barplot(x='Country', y='Data.Daily cigarettes', data=intensity_sorted, palette="Purples_d")
plt.title('Top 5 Countries by Daily Cigarette Consumption (2012)')
plt.ylabel('Average Daily Cigarettes Smoked')
plt.xticks(rotation=45)
plt.show()

# -----------------------
# 4. Absolute Numbers vs. Percentage Analysis
# -----------------------

# Sort countries by absolute number of smokers and percentage of smokers in 2012 for the top 5 countries in each category
absolute_sorted = latest_year_data[['Country', 'Data.Smokers.Total']].sort_values('Data.Smokers.Total', ascending=False).head(5)
percentage_sorted = latest_year_data[['Country', 'Data.Percentage.Total']].sort_values('Data.Percentage.Total', ascending=False).head(5)

# Absolute Numbers vs. Percentage Analysis Visuals
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 12))

# Countries with the highest absolute number of smokers
sns.barplot(x='Country', y='Data.Smokers.Total', data=absolute_sorted, ax=axes[0], palette="Greens_d")
axes[0].set_title('Top 5 Countries by Absolute Number of Smokers (2012)')
axes[0].set_ylabel('Total Number of Smokers')
axes[0].set_yscale('log')  # Using a log scale due to the large differences in values
axes[0].tick_params(axis='x', rotation=45)

# Countries with the highest percentage of smokers
sns.barplot(x='Country', y='Data.Percentage.Total', data=percentage_sorted, ax=axes[1], palette="Oranges_d")
axes[1].set_title('Top 5 Countries by Smoking Percentage (2012)')
axes[1].set_ylabel('Percentage of Smokers')
axes[1].tick_params(axis='x', rotation=45)

# Adjust layout and display
plt.tight_layout()
plt.show()

# -----------------------
# 5. Geographical Patterns Analysis
# -----------------------

# This section provides a simplified representation using a heatmap. A more detailed choropleth map would require additional tools and data.

# Create a dictionary mapping country names to latitude and longitude (center points)
country_coordinates = {
    'Afghanistan': [33.93911, 67.709953],
    'China': [35.86166, 104.195397],
    'India': [20.593684, 78.96288],
    'Indonesia': [-0.789275, 113.921327],
    'Russia': [61.52401, 105.318756],
    # ... add more countries as needed
}

# Add latitude and longitude to our dataset
latest_year_data['Latitude'] = latest_year_data['Country'].map(lambda x: country_coordinates.get(x, [None, None])[0])
latest_year_data['Longitude'] = latest_year_data['Country'].map(lambda x: country_coordinates.get(x, [None, None])[1])

# Plot heatmap
plt.figure(figsize=(15, 7))
sns.scatterplot(x='Longitude', y='Latitude', size='Data.Percentage.Total', hue='Data.Percentage.Total', 
                sizes=(10, 200), data=latest_year_data, palette="YlGnBu", legend=False)
plt.title('Geographical Patterns of Smoking Percentage (2012)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.show()
