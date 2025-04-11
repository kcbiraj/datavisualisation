# Importing Required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
%matplotlib inline


import requests
from io import StringIO

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv"
response = requests.get(url)
response.raise_for_status()  #Raises an error when requests fails

df = pd.read_csv(StringIO(response.text))
df.head()

# Checking the data types of the columns
df.columns
df.dtypes


import datetime as dt

df['Year'] = pd.to_datetime(df['Date']).dt.year
df['Month'] = pd.to_datetime(df['Date']).dt.month


plt.figure(figsize=(12,6))
# Grouping the data by 'Year' and calculating the mean of 'Estimated_fire_area'
df_new = df.groupby('Year')['Estimated_fire_area'].mean()
df_new.plot(x=df_new.index, y=df_new.values)
plt.xlabel('Year')
plt.ylabel('Average Estimate Fire Area (km²)')
plt.title('Estimated Fire Area Over Time')
plt.show()
plt.savefig('../../reports/australia_wildfire/Estimated_Fire_Area_Over_Time_Year.png', dpi=300, bbox_inches='tight')


# Grouping the data by both 'Year' and 'Month', and calculating the mean of 'Estimated_fire_area'

df_new = df.groupby(['Year','Month'])['Estimated_fire_area'].mean()

# Plotting the data
df_new.plot(x=df_new.index, y=df_new.values)
plt.xlabel('Year, Month')
plt.ylabel('Average Estimated Fire Area (km²)')
plt.title('Estimated Fire Area over Time')
plt.show()
plt.savefig('../../reports/australia_wildfire/Estimated_Fire_Area_Over_Time.png', dpi=300, bbox_inches='tight')


df['Region'].unique()
# Creating a bar plot using seaborn to visualize the distribution of mean estimated fire brightness across regions
plt.figure(figsize=(10, 6))
# Using seaborn's barplot function to create the plot
sns.barplot(data=df, x='Region', y='Mean_estimated_fire_brightness')
plt.xlabel('Region')
plt.ylabel('Mean Estimated Fire Brightness (Kelvin)')
plt.title('Distribution of Mean Estimated Fire Brightness across Regions')
plt.show()
plt.savefig('../../reports/australia_wildfire/Mean_Estimated_Fire_Brightness_Regions.png', dpi=300, bbox_inches='tight')


# Creating a pie chart to visualize the portion of count of pixels for presumed vegetation fires across regions
plt.figure(figsize=(10, 10))
# Grouping the data by region and summing the counts
region_counts = df.groupby('Region')['Count'].sum()
# Creating the pie chart using plt.pie function
# Labels are set to the region names, and autopct is used to display percentage
plt.pie(region_counts, labels=region_counts.index, autopct='%1.1f%%')
plt.title('Percentage of Pixels for Presumed Vegetation Fires by Region')
plt.axis('equal')
plt.show()
plt.savefig('../../reports/australia_wildfire/Percentage_of_Pixels_for_Presumed_Vegetation_Fires_by_Region.png', dpi=300, bbox_inches='tight')


import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))

# Grouping the data by 'Region' and summing the 'Count'
region_counts = df.groupby('Region')['Count'].sum()

# Creating the pie chart
plt.pie(region_counts, labels=region_counts.index, autopct='%1.1f%%')

# Formatting the legend manually
legend_labels = [f"{i}: {round(k/region_counts.sum()*100,2)}%" for i, k in zip(region_counts.index, region_counts)]
plt.legend(legend_labels, title="Regions", loc="best")

# Setting title and equal aspect ratio
plt.title('Percentage of Pixels for Presumed Vegetation Fires by Region')
plt.axis('equal')  # Ensures the pie chart is a circle
plt.show()
plt.savefig('../../reports/australia_wildfire/Percentage_of_Pixels_for_Presumed_Vegetation_Fires_by_Region1.png', dpi=300, bbox_inches='tight')


# Creating a histogram to visualize the distribution of mean estimated fire brightness
plt.figure(figsize=(10, 6))
# Using plt.hist to create the histogram
# Setting the number of bins to 20 for better visualization
plt.hist(x=df['Mean_estimated_fire_brightness'], bins=20)
plt.xlabel('Mean Estimated Fire Brightness (Kelvin)')
plt.ylabel('Count')
plt.title('Histogram of Mean Estimated Fire Brightness')
plt.show()
plt.savefig('../../reports/australia_wildfire/Histogram_of_Mean_Estimated_Fire_Brightness.png', dpi=300, bbox_inches='tight')


# Creating a histogram to visualize the distribution of mean estimated fire brightness across regions using Seaborn
# Using sns.histplot to create the histogram
# Specifying the DataFrame (data=df) and the column for the x-axis (x='Mean_estimated_fire_brightness')
# Adding hue='Region' to differentiate the distribution across regions
sns.histplot(data=df, x='Mean_estimated_fire_brightness', hue='Region')
plt.show()
plt.savefig('../../reports/australia_wildfire/Histogram_of_Mean_Estimated_Fire_Brightness_Regions_SNS.png', dpi=300, bbox_inches='tight')

# Creating a stacked histogram to visualize the distribution of mean estimated fire brightness across regions using Seaborn
# Using sns.histplot to create the stacked histogram
# Specifying the DataFrame (data=df) and the column for the x-axis (x='Mean_estimated_fire_brightness')
# Adding hue='Region' to differentiate the distribution across regions
# Setting multiple='stack' to stack the histograms for different regions
sns.histplot(data=df, x='Mean_estimated_fire_brightness', hue='Region', multiple='stack')
plt.show()
plt.savefig('../../reports/australia_wildfire/Stacked_Histogram_of_Mean_Estimated_Fire_Brightness_Regions_SNS.png', dpi=300, bbox_inches='tight')


# Creating a scatter plot to visualize the relationship between mean estimated fire radiative power and mean  confidence using Seaborn
plt.figure(figsize=(8, 6))
# Using sns.scatterplot to create the scatter plot
# Specifying the DataFrame (data=df) and the columns for the x-axis (x='Mean_confidence') and y-axis            (y='Mean_estimated_fire_radiative_power')    
sns.scatterplot(data=df, x='Mean_confidence', y='Mean_estimated_fire_radiative_power')
plt.xlabel('Mean Estimated Fire Radiative Power (MW)')

plt.ylabel('Mean Confidence')
plt.title('Mean Estimated Fire Radiative Power vs. Mean Confidence')
plt.show()
plt.savefig('../../reports/australia_wildfire/Mean_Estimated_Fire_Radiative_Power_vs_Mean_Confidence.png', dpi=300, bbox_inches='tight')


region_data = {'region':['NSW','QL','SA','TA','VI','WA','NT'], 'Lat':[-31.8759835,-22.1646782,-30.5343665,-42.035067,-36.5986096,-25.2303005,-19.491411], 
               'Lon':[147.2869493,144.5844903,135.6301212,146.6366887,144.6780052,121.0187246,132.550964]}
reg=pd.DataFrame(region_data)
reg

# instantiate a feature group 
aus_reg = folium.map.FeatureGroup()

# Create a Folium map centered on Australia
Aus_map = folium.Map(location=[-25, 135], zoom_start=4)

# loop through the region and add to feature group
for lat, lng, lab in zip(reg.Lat, reg.Lon, reg.region):
    aus_reg.add_child(
        folium.features.CircleMarker(
            [lat, lng],
            popup=lab,
            radius=5, # define how big you want the circle markers to be
            color='red',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6
        )
    )

# add incidents to map
Aus_map.add_child(aus_reg)
# save map to html file
Aus_map.save('../../reports/australia_wildfire/Australia_Wildfire_Incidents_Map.html')
# Display the map
Aus_map

# Create a Folium map centered on Australia
Aus_map = folium.Map(location=[-25, 135], zoom_start=4)
# Loop through the region and add to feature group
for lat, lng, lab in zip(reg.Lat, reg.Lon, reg.region):
    folium.Marker(
        location=[lat, lng],
        popup=lab,
        icon=folium.Icon(color='blue')
    ).add_to(Aus_map)
# Save map to html file
Aus_map.save('../../reports/australia_wildfire/Australia_Wildfire_Incidents_Map1.html')
# Display the map
Aus_map
