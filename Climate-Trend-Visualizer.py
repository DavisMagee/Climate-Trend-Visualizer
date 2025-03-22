# -*- coding: utf-8 -*-
"""
Author: Davis Magee
Email: Davis.Magee01@gmail.com
Phone: (228) 474-9607
X (former Twitter): @DavisMagee_Wx
"""

# Importing the necessary libraries

import matplotlib.pyplot as plt # matplotlib is used to plot the data
import numpy as np # numpy is used to make a trend line


# Read the file
file = open('ShreveportDataFile.txt', 'r')
header1 = file.readline() # read header that contains size to iterate over
header2 = file.readline() # iterates over the separator
tmplist = file.readlines() # read rest of data after the sparator and puts it in a list
file.close() # closes the file to save ram

# saving the dates and tmins in seperate lists
dates = [] # creates the dates list
tmins = [] # creates the tmins list

for line in tmplist:
    date = line[-19:-10].strip() # grabs the date from the list and strips it of whitespace
    dates.append(date) # saves the date to the end of the dates list
    tmin_value = line[-10:-1].strip() # grabs the tmin from the list and strips it of whitespace
    tmins.append(int(tmin_value)) # save the tmin as an integer to the end of the tmins list
    

# create the lists that will how the year and number of days below freezing
years_in_data = []
days_below_freezing = []

# function to extract year and month from a date string
def get_year_month(date_str):
    year = int(date_str[:4])
    month = int(date_str[4:6])
    return year, month

# Iterating through the list
current_winter_start_year = None
current_winter_days = 0


for i in range(len(dates)):
    date_str = dates[i]
    temp = tmins[i]
    
    year, month = get_year_month(date_str)

    # grouping the months into their correct winter season
    if month >= 8:
        winter_start_year = year # sets first full winter of data to be the starting year
    elif month <= 4:
        winter_start_year = year - 1 # ensures that January and February are included
    else:
        continue # skips summer months
    
    # Sets the first season to record data and skips the first half winter so that the data is complete
    if current_winter_start_year is None: # If it's the first year of data
        if month >= 8:   # If it is atleast august, sets the first winter season
            current_winter_start_year = winter_start_year
        else:  # If it's not at least august, ignores the data
            continue
    
    # If we've moved to a new winter season, store the previous season's dates
    if winter_start_year != current_winter_start_year:
        days_below_freezing.append(current_winter_days)
        years_in_data.append(current_winter_start_year)
        
        # Reset for the new winter season
        current_winter_start_year = winter_start_year
        current_winter_days = 0
    
    # Count days at or below freezing
    if temp <= 32:
        current_winter_days += 1
        
        
# Append the final winter season's data
if current_winter_start_year is not None:
    days_below_freezing.append(current_winter_days)
    years_in_data.append(current_winter_start_year)

# Creating a trend line
slope, intercept = np.polyfit(years_in_data, days_below_freezing, 1)
trend_line = slope * np.array(years_in_data) + intercept

# Print the slope of the trend line
print(f"The slope of the trend line is: {slope:.4f}")

# Plotting the data on a line plot

# Create a figure and axis
fig, ax, = plt.subplots()

# Plot the data
ax.plot(years_in_data, days_below_freezing, linestyle='-', color='b', label="Days Below Freezing")
ax.plot(years_in_data, trend_line, linestyle='--', color='r', label='Trend Line')

# Sets the x-axis to display every 10 years starting in 1965 and ending in 2025
plt.xticks(np.arange(min(years_in_data), max(years_in_data) + 2, 10))

# Set the y-axis minimum to 0
plt.ylim(ymin=0, ymax=100)

# Add labels and title
ax.set_xlabel("Winter Season")
ax.set_ylabel('Days Below Freezing')
ax.set_title('Days Below Freezing over Years in Shreveport, LA (1965 - 2025)')

# Add a legend
ax.legend()

# Show the plot
plt.show()



# Some extra code for fun facts
# counting how many days were at or below freezing in total
numberfreezing = 0 # set a running variable to count how many days were freezing
    
for t in tmins: # runs through list of tmin values
    if t <= 32: # if tmin value was at or below freezing
        numberfreezing += 1 # increment number of freezing days up by 1

