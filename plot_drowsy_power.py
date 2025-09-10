import pandas as pd
import argparse
import os
import matplotlib.pyplot as plt
from datetime import datetime

parser = argparse.ArgumentParser(description='Plot Drowsy Power vs Research Experience and Dream Shards.')
parser.add_argument('folder', help='Folder containing report_info.csv and session_info.csv')
args = parser.parse_args()

report_csv = os.path.join(args.folder, 'report_info.csv')
session_csv = os.path.join(args.folder, 'session_info.csv')

# Read CSV files
report_df = pd.read_csv(report_csv)
session_df = pd.read_csv(session_csv)

# Standardize dates in report (YYYY-MM-DD) Report always comes on the next day!
report_df['date_std'] = pd.to_datetime(report_df['date'], format='%Y-%m-%d') - pd.Timedelta(days=1)

# Standardize dates in session (e.g., Monday, May 5, 2025)
def parse_session_date(date_str):
    try:
        return datetime.strptime(date_str, '%A, %B %d, %Y')
    except ValueError:
        # Try without weekday if needed
        return datetime.strptime(date_str, '%B %d, %Y')

session_df['date_std'] = session_df['date'].apply(parse_session_date)

# Merge dataframes on 'date'
merged_df = pd.merge(report_df, session_df, on='date_std')

print("report_df head:")
print(report_df.head())
print("\nsession_df head:")
print(session_df.head())
print("\nmerged_df head:")
print(merged_df.head())

# Plot Research Experience vs Drowsy Power
plt.figure(figsize=(10, 6))
# Plot Research Experience vs Drowsy Power, coloring by day of week
days = merged_df['date_std'].dt.day_name()
unique_days = days.unique()
colors = plt.cm.get_cmap('tab10', len(unique_days))

for idx, day in enumerate(unique_days):
    mask = days == day
    plt.scatter(
        merged_df.loc[mask, 'drowsy_power'],
        merged_df.loc[mask, 'research_exp'],
        label=f'Research Exp ({day})',
        color=colors(idx),
        marker='o'
    )

# Optionally, add day-of-week as text labels for each point
for i, row in merged_df.iterrows():
    plt.text(
        row['drowsy_power'],
        row['research_exp'],
        row['date_std'].strftime('%a'),
        fontsize=8,
        ha='right',
        va='bottom'
    )

# Plot Dream Shards vs Drowsy Power
plt.plot(merged_df['drowsy_power'], merged_df['dream_shards'], marker='s', label='Dream Shards vs Drowsy Power')

plt.xlabel('Drowsy Power')
plt.ylabel('Research Experience / Dream Shards')
plt.title('Research Experience and Dream Shards vs Drowsy Power')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()