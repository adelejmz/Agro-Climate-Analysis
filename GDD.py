import pandas as pd
import os
import matplotlib.pyplot as plt

# File path to the master file
file_path = r"C:\Users\adele.jamalzei\Desktop\Dissertation\Cold Tolerance Project\Analysis_Result\Primary Analysis\Weather Analysis\Clean weather"
master_file = f"{file_path}\\Pullman_Master.xlsx"  # Ensure the file name is correct

# Base temperature for GDD calculation (in Fahrenheit)
base_temp_f = 32  # Base temperature set to 32°F

# Check if the file exists
if not os.path.exists(master_file):
    print(f"File not found: {master_file}")
else:
    # Load the dataset
    pullman_master = pd.read_excel(master_file)
    print("File loaded successfully!")

    # Convert Date_Time to datetime and extract Date
    pullman_master['Date_Time'] = pd.to_datetime(pullman_master['Date_Time'], errors="coerce")
    pullman_master['Date'] = pullman_master['Date_Time'].dt.date

    # Group by Date to calculate daily temp_min and temp_max
    daily_temps = pullman_master.groupby('Date')['air_temp_set_1'].agg(temp_min='min', temp_max='max').reset_index()

    # Calculate GDD for each date
    daily_temps['GDD'] = ((daily_temps['temp_max'] + daily_temps['temp_min']) / 2) - base_temp_f
    daily_temps['GDD'] = daily_temps['GDD'].apply(lambda x: x if x > 0 else 0)  # Set GDD to 0 if negative

    # Convert Date to datetime for grouping and plotting
    daily_temps['Date'] = pd.to_datetime(daily_temps['Date'])
    daily_temps['Year'] = daily_temps['Date'].dt.year
    daily_temps['Month'] = daily_temps['Date'].dt.month

    # Filter for the years 2017-2019
    daily_temps = daily_temps[daily_temps['Year'].isin([2017, 2018, 2019])]

    # Calculate cumulative GDD for each year
    daily_temps['Cumulative_GDD'] = daily_temps.groupby(['Year'])['GDD'].cumsum()

    # Calculate average cumulative GDD by month
    monthly_gdd = daily_temps.groupby(['Year', 'Month'])['Cumulative_GDD'].mean().reset_index()

    # Pivot table for better visualization
    monthly_gdd_pivot = monthly_gdd.pivot(index='Month', columns='Year', values='Cumulative_GDD')
    print("Monthly Average Cumulative GDD (°F):")
    print(monthly_gdd_pivot)

    # Plot the results
    plt.figure(figsize=(10, 6))
    for year in [2017, 2018, 2019]:
        if year in monthly_gdd_pivot.columns:
            plt.plot(monthly_gdd_pivot.index, monthly_gdd_pivot[year], marker='o', label=f'{year}')

    plt.title('Cumulative GDD in Pullman (2017-2019)', fontsize=16)
    plt.xlabel('Month', fontsize=14)
    plt.ylabel('Cumulative GDD (°F)', fontsize=14)
    plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.grid(True)
    plt.legend(title='Year', fontsize=10)
    plt.tight_layout()
    plt.show()
