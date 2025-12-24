import pandas as pd
import matplotlib.pyplot as plt

# ✅ Correct file path for GDD data
file_path = r"C:\Users\adele.jamalzei\Desktop\Dissertation\Cold Tolerance Project-Done\Analysis_Result\Result_All_Final\Weather Analysis\GDD_per_month_df.csv"

# ✅ Load the dataset
GDD_per_month_df = pd.read_csv(file_path)
print("File loaded successfully!")

# ✅ Set the selected city for Pendleton
selected_city = 'Pendleton'

# ✅ Filter data for Pendleton (ONLY 2017, 2018)
selected_GDD_df = GDD_per_month_df[
    (GDD_per_month_df['city_name'] == selected_city) &
    (GDD_per_month_df['year'].isin([2017, 2018]))
]

# ✅ Define the correct month order (January to September only)
month_order = [
    'January', 'February', 'March', 'April', 'May', 'June', 'July',
    'August', 'September'
]

# ✅ Convert 'month' column to categorical type with the correct order
selected_GDD_df['month'] = pd.Categorical(
    selected_GDD_df['month'], categories=month_order, ordered=True
)

# ✅ Aggregate GDD (SUM) to remove duplicates
monthly_GDD = selected_GDD_df.groupby(['year', 'month'], as_index=False)['GDD'].sum()

# ✅ Pivot to reshape data (years as columns, months as rows)
pivot_df = monthly_GDD.pivot(index='month', columns='year', values='GDD').reindex(month_order)

# ✅ Ensure only 2017 and 2018 are included
pivot_df = pivot_df.loc[:, [col for col in pivot_df.columns if col in [2017, 2018]]]

# ✅ Fill missing months with 0
pivot_df.fillna(0, inplace=True)

# ✅ Print final dataset for verification
print("\nFinal GDD Data for Pendleton (Aggregated by Month - January to September):")
print(pivot_df)

# ✅ Set Matplotlib style
plt.style.use('bmh')

# ✅ Set figure size
plt.figure(figsize=(10, 5))

# ✅ Plot lines for 2017 and 2018
plt.plot(pivot_df.index, pivot_df[2017], marker='o', linestyle='-', color='blue', label='2017')
plt.plot(pivot_df.index, pivot_df[2018], marker='o', linestyle='-', color='red', label='2018')

# ✅ Customize the plot (updated title)
plt.title(f'Growing Degree Days (GDD) in {selected_city} (2017-2018)', 
          fontsize=14, fontweight="bold")
plt.ylabel('GDD (°C·days)', fontsize=14)     # consistent units
plt.xlabel('Month', fontsize=12)

# ✅ Keep months straight on x-axis
plt.xticks(rotation=0, fontsize=11)

# ✅ Add grid
plt.grid(True, linestyle='--', alpha=0.7)

# ✅ Format y-axis with comma separator
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: format(int(x), ',')))

# ✅ Add legend
plt.legend(title="Year", fontsize=12, title_fontsize=12, loc='upper right')

# ✅ Adjust layout
plt.tight_layout()

# ✅ Save and show the plot
output_path = r"C:\Users\adele.jamalzei\Desktop\Dissertation\Cold Tolerance Project-Done\Analysis_Result\Result_All_Final\Weather Analysis\Pendleton_GDD_chart_2017_2018_Jan_Sep.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.show()

print(f"Plot saved at: {output_path}")
