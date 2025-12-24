# ---- Pullman: Monthly Means by Year (2017 vs 2018) ----
import os
import pandas as pd
import matplotlib.pyplot as plt

# ====== 1) Point to your Pullman file ======
DIR = r"C:\Users\adele.jamalzei\Desktop\Dissertation\Cold Tolerance Project-Done\Analysis_Result\Result_All_Final\Weather Analysis\Pullman"
FNAME = "Pullman_Master.xlsx"
PATH = os.path.join(DIR, FNAME)

if not os.path.exists(PATH):
    raise FileNotFoundError(f"File not found:\n{PATH}\n\nCheck files here:\n{os.listdir(DIR)}")

# ====== 2) Load & clean ======
df = pd.read_excel(PATH)

# Fix datetime
df['Date_Time'] = pd.to_datetime(
    df['Date_Time'].astype(str).str.replace(r'\s*(PDT|PST)$', '', regex=True),
    errors='coerce'
)
df = df.dropna(subset=['Date_Time']).copy()
df['Year']  = df['Date_Time'].dt.year
df['Month'] = df['Date_Time'].dt.month

# Keep only 2017–2018 and Jan–Sep
df = df[df['Year'].isin([2017, 2018])]
df = df[df['Month'].between(1, 9)]

# ====== 3) Helper: monthly means per year → wide (cols: 2017, 2018) ======
def monthly_means_by_year(frame: pd.DataFrame, value_col: str, convert_f_to_c=False):
    dat = frame[['Year', 'Month', value_col]].dropna().copy()
    if convert_f_to_c:
        dat[value_col] = (dat[value_col] - 32) * 5/9
    wide = (dat.groupby(['Month', 'Year'])[value_col].mean()
               .unstack('Year')   # columns: 2017, 2018
               .sort_index())
    return wide

plt.style.use('ggplot')

# ---- A) Air Temperature (°C), two lines ----
TEMP_COL = 'air_temp_set_1'
temp_wide = monthly_means_by_year(df, TEMP_COL, convert_f_to_c=True)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(temp_wide.index, temp_wide[2017], marker='o', linewidth=2, label='2017')
ax.plot(temp_wide.index, temp_wide[2018], marker='o', linewidth=2, label='2018')
ax.set_xticks(temp_wide.index)
ax.set_xticklabels(pd.to_datetime([f'2023-{m:02d}-01' for m in temp_wide.index]).strftime('%b'), fontsize=12)
ax.set_xlabel('Month', fontsize=14, fontweight='bold')
ax.set_ylabel('Average Air Temperature (°C)', fontsize=14, fontweight='bold')
ax.set_title('Monthly Average Air Temperature — Pullman (2017-2018)', fontsize=16, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.6)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.legend(frameon=True, title='Year', fontsize=12)
plt.tight_layout(); plt.show()

# ---- B) Relative Humidity (%), two lines ----
RH_COL = 'relative_humidity_set_1'
rh_wide = monthly_means_by_year(df, RH_COL, convert_f_to_c=False)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(rh_wide.index, rh_wide[2017], marker='o', linewidth=2, label='2017')
ax.plot(rh_wide.index, rh_wide[2018], marker='o', linewidth=2, label='2018')
ax.set_xticks(rh_wide.index)
ax.set_xticklabels(pd.to_datetime([f'2023-{m:02d}-01' for m in rh_wide.index]).strftime('%b'), fontsize=12)
ax.set_xlabel('Month', fontsize=14, fontweight='bold')
ax.set_ylabel('Average Relative Humidity (%)', fontsize=14, fontweight='bold')
ax.set_title('Monthly Average Relative Humidity — Pullman (2017-2018)', fontsize=16, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.6)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.legend(frameon=True, title='Year', fontsize=12)
plt.tight_layout(); plt.show()
