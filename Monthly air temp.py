import pandas as pd
import matplotlib.pyplot as plt
import os

# ✅ Correct file path and file name for Pendleton
file_path = r"C:\Users\adele.jamalzei\Desktop\Dissertation\Cold Tolerance Project\Analysis_Result\Result_All_Final\Weather Analysis\Pendlton"
master_file = os.path.join(file_path, "Pendlton_Master.xlsx")

# ✅ Check if the file exists
if not os.path.exists(master_file):
    print(f"File not found: {master_file}")
else:
    print(f"File found: {master_file}")

    # ✅ Load the dataset from Excel
    pendlton_master = pd.read_excel(master_file)
    print("File loaded successfully!")

    # ✅ Convert Date_Time to datetime format
    pendlton_master['Date_Time'] = pd.to_datetime(
        pendlton_master['Date_Time'].astype(str).str.replace(r' PDT| PST', '', regex=True),
        errors="coerce"
    )
    print("Converted 'Date_Time' to datetime format.")

    # ✅ Drop rows with invalid dates
    pendlton_master.dropna(subset=['Date_Time'], inplace=True)

    # ✅ Extract the year and month
    pendlton_master['Year'] = pendlton_master['Date_Time'].dt.year
    pendlton_master['Month'] = pendlton_master['Date_Time'].dt.month

    # ✅ Keep only 2017 and 2018
    pendlton_master = pendlton_master[pendlton_master['Year'].isin([2017, 2018])]

    # ✅ Keep only months from January to September
    pendlton_master = pendlton_master[pendlton_master['Month'] <= 9]

    # ✅ Convert air temperature from Fahrenheit to Celsius
    pendlton_master['air_temp_set_1'] = (pendlton_master['air_temp_set_1'] - 32) * 5/9

    # ✅ Separate data for 2017 and 2018
    pendlton_2017 = pendlton_master[pendlton_master['Year'] == 2017].copy()
    pendlton_2018 = pendlton_master[pendlton_master['Year'] == 2018].copy()

    # ✅ Compute the average monthly air temperature (°C) for each year separately
    monthly_avg_2017 = pendlton_2017.groupby('Month')['air_temp_set_1'].mean()
    monthly_avg_2018 = pendlton_2018.groupby('Month')['air_temp_set_1'].mean()

    # ✅ Merge both years, keeping only valid months
    combined_avg_temp = pd.DataFrame({'2017': monthly_avg_2017, '2018': monthly_avg_2018})

    # ✅ Identify valid months in 2017 & 2018
    valid_months_2017 = monthly_avg_2017.index.tolist()
    valid_months_2018 = monthly_avg_2018.index.tolist()

    # ✅ Determine the final set of months to use (January to September)
    valid_months = sorted(set(valid_months_2017) | set(valid_months_2018))

    # ✅ Compute the overall average for valid months
    combined_avg_temp['Avg'] = combined_avg_temp.mean(axis=1, skipna=True)

    # ✅ Keep only January to September data
    combined_avg_temp = combined_avg_temp.loc[valid_months]

    print("Final computed average air temperature in Pendleton (Jan-Sep only, converted to °C):")
    print(combined_avg_temp)

    # ✅ Set Matplotlib style
    plt.style.use('ggplot')

    # ✅ Plot the monthly average air temperature trend
    plt.figure(figsize=(8, 5))
    plt.plot(combined_avg_temp.index, combined_avg_temp['Avg'], marker='o', markersize=8, linewidth=2, color="red", label="Avg Air Temp (°C)")

    # ✅ Customize x-axis labels (only January to September)
    month_labels = [pd.to_datetime(f"2023-{m:02d}-01").strftime('%b') for m in valid_months]
    plt.xticks(valid_months, month_labels, fontsize=12)
    plt.xlabel('Month', fontsize=14, fontweight='bold')

    # ✅ Customize y-axis
    plt.ylabel('Avg Air Temperature (°C)', fontsize=14, fontweight='bold')

    # ✅ Update Title
    plt.title('Monthly Average Air Temperature in Pendleton (2017-2018)', fontsize=16, fontweight='bold')

    # ✅ Add grid for readability
    plt.grid(True, linestyle="--", alpha=0.6)

    # ✅ Remove unnecessary borders
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    # ✅ Add legend
    plt.legend(frameon=True, fontsize=12)

    # ✅ Tight layout for better spacing
    plt.tight_layout()

    # ✅ Show the plot
    plt.show()
