import pandas as pd
import matplotlib.pyplot as plt

# ✅ File path (Update this if needed)
file_path = r"C:\Users\adele.jamalzei\Desktop\Dissertation\HighBiomass Project\CIMMYT\Weather Data\CIMMYT_Weather_Master.xlsx"

# ✅ Load dataset
weather_data = pd.read_excel(file_path)

# ✅ Convert Date to datetime format
weather_data['Date'] = pd.to_datetime(weather_data['Date'], errors='coerce')

# ✅ Define the growing seasons with a fixed end date (May)
season_periods = {
    "2021-2022": ("2021-11-01", "2022-05-09"),
    "2022-2023": ("2022-11-01", "2023-05-09"),  # Adjusted to end in May
    "2023-2024": ("2023-11-15", "2024-05-07"),
}

# ✅ Create a new column for Season Label
weather_data["Season"] = None

# ✅ Assign each row to its respective growing season
for season, (start, end) in season_periods.items():
    mask = (weather_data["Date"] >= start) & (weather_data["Date"] <= end)
    weather_data.loc[mask, "Season"] = season

# ✅ Drop rows that don’t belong to any season
weather_data = weather_data.dropna(subset=["Season"])

# ✅ Extract Month-Order within each season
weather_data["Month-Order"] = (
    (weather_data["Date"] - weather_data.groupby("Season")["Date"].transform("min")).dt.days // 30 + 1
)

# ✅ Compute the monthly average temperature for each season
seasonal_avg_temp = weather_data.groupby(["Season", "Month-Order"])["Average Temperature"].mean().unstack(level=0)

# ✅ Plot the seasonal temperature trends
plt.style.use('ggplot')
plt.figure(figsize=(10, 6))

for season in seasonal_avg_temp.columns:
    plt.plot(seasonal_avg_temp.index, seasonal_avg_temp[season], marker='o', markersize=8, linewidth=2, label=f"{season} Avg Temp (°C)")

# ✅ Customize x-axis labels (Only Nov-May)
plt.xticks(seasonal_avg_temp.index, ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May"], fontsize=12)
plt.xlabel('Growing Season Month', fontsize=14, fontweight='bold')

# ✅ Customize y-axis
plt.ylabel('Avg Air Temperature (°C)', fontsize=14, fontweight='bold')

# ✅ Update Title
plt.title('Monthly Average Air Temperature in Obregon, Mexico', fontsize=16, fontweight='bold')

# ✅ Add grid, legend, and cleanup
plt.grid(True, linestyle="--", alpha=0.6)
plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)
plt.legend(frameon=True, fontsize=12)

# ✅ Show plot
plt.tight_layout()
plt.show()

# ✅ Print final computed seasonal average temperatures
print("Final computed seasonal average temperatures:")
print(seasonal_avg_temp)
