import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("Time_Series_Cleaned.csv")
df['datetime_local'] = pd.to_datetime(df['datetime_local'])


# 1. Line Chart - Temperature over time
plt.figure(figsize=(12, 4))
plt.plot(df['datetime_local'], df['temperature'], color='red', linewidth=1)
plt.xlabel('Date')
plt.ylabel('Temperature (C)')
plt.title('Temperature Over Time')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('1_line_temperature.png')
plt.show()


# 2. Bar Chart - Average temperature per day
daily_avg = df.groupby('day')['temperature'].mean()

plt.figure(figsize=(12, 4))
plt.bar(daily_avg.index, daily_avg.values, color='steelblue')
plt.xlabel('Day')
plt.ylabel('Avg Temperature (C)')
plt.title('Average Temperature Per Day')
plt.tight_layout()
plt.savefig('2_bar_avg_temp.png')
plt.show()


# 3. Pie Chart - Weather condition breakdown
condition_counts = df['icon'].value_counts()

plt.figure(figsize=(8, 8))
plt.pie(condition_counts.values, labels=condition_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Weather Condition Breakdown')
plt.tight_layout()
plt.savefig('3_pie_conditions.png')
plt.show()


# 4. Histogram - How temperature values are spread
plt.figure(figsize=(8, 4))
plt.hist(df['temperature'], bins=15, color='orange', edgecolor='black')
plt.xlabel('Temperature (C)')
plt.ylabel('Count')
plt.title('Temperature Distribution')
plt.tight_layout()
plt.savefig('4_histogram_temp.png')
plt.show()


# 5. Scatter Plot - Temperature vs Humidity
plt.figure(figsize=(7, 5))
plt.scatter(df['temperature'], df['humidity'], alpha=0.4, color='teal', s=15)
plt.xlabel('Temperature (C)')
plt.ylabel('Humidity (%)')
plt.title('Temperature vs Humidity')
plt.tight_layout()
plt.savefig('5_scatter_temp_humidity.png')
plt.show()


# 6. Box Plot - Temperature spread each day
days = sorted(df['day'].unique())
temp_per_day = [df[df['day'] == d]['temperature'].values for d in days]

plt.figure(figsize=(14, 5))
plt.boxplot(temp_per_day, tick_labels=days, patch_artist=True,
            boxprops=dict(facecolor='lightblue'))
plt.xlabel('Day')
plt.ylabel('Temperature (C)')
plt.title('Temperature Spread Per Day')
plt.tight_layout()
plt.savefig('6_boxplot_temp.png')
plt.show()


# 7. Area Chart - Humidity over time
plt.figure(figsize=(12, 4))
plt.fill_between(df['datetime_local'], df['humidity'], alpha=0.5, color='cornflowerblue')
plt.plot(df['datetime_local'], df['humidity'], color='blue', linewidth=0.8)
plt.xlabel('Date')
plt.ylabel('Humidity (%)')
plt.title('Humidity Over Time')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('7_area_humidity.png')
plt.show()


# 8. Donut Chart - Wind speed categories
bins   = [0, 2, 4, 6, 100]
labels = ['Calm', 'Light', 'Moderate', 'Strong']
df['wind_cat'] = pd.cut(df['wind_speed'], bins=bins, labels=labels)
counts = df['wind_cat'].value_counts()

plt.figure(figsize=(7, 7))
plt.pie(counts.values, labels=counts.index, autopct='%1.1f%%',
        wedgeprops=dict(width=0.5), startangle=90)
plt.title('Wind Speed Categories')
plt.tight_layout()
plt.savefig('8_donut_wind.png')
plt.show()


# 9. Heatmap - Avg temperature by hour and day
pivot = df.pivot_table(values='temperature', index='hour', columns='day', aggfunc='mean')

plt.figure(figsize=(16, 6))
plt.imshow(pivot, cmap='RdYlBu_r', aspect='auto')
plt.colorbar(label='Temp (C)')
plt.xlabel('Day')
plt.ylabel('Hour')
plt.title('Temperature Heatmap (Hour vs Day)')
plt.xticks(range(len(pivot.columns)), pivot.columns)
plt.yticks(range(len(pivot.index)), pivot.index)
plt.tight_layout()
plt.savefig('9_heatmap_temp.png')
plt.show()


# 10. Violin Plot - Humidity by day
hum_per_day = [df[df['day'] == d]['humidity'].values for d in days]

plt.figure(figsize=(14, 5))
parts = plt.violinplot(hum_per_day, positions=days, showmedians=True)
for pc in parts['bodies']:
    pc.set_facecolor('mediumpurple')
    pc.set_alpha(0.7)
plt.xlabel('Day')
plt.ylabel('Humidity (%)')
plt.title('Humidity Distribution Per Day')
plt.tight_layout()
plt.savefig('10_violin_humidity.png')
plt.show()


# 11. Horizontal Bar Chart - Overall averages
metrics = {
    'Temperature': df['temperature'].mean(),
    'Dew Point':   df['dew_point'].mean(),
    'Humidity':    df['humidity'].mean(),
    'Wind Speed':  df['wind_speed'].mean(),
    'UV Index':    df['uv_index'].mean(),
}

plt.figure(figsize=(8, 5))
plt.barh(list(metrics.keys()), list(metrics.values()), color='salmon')
plt.xlabel('Average Value')
plt.title('Overall Weather Averages')
plt.tight_layout()
plt.savefig('11_hbar_averages.png')
plt.show()


# 12. Step Chart - Avg UV index by hour
uv_by_hour = df.groupby('hour')['uv_index'].mean()

plt.figure(figsize=(10, 4))
plt.step(uv_by_hour.index, uv_by_hour.values, where='mid', color='darkorange', linewidth=2)
plt.fill_between(uv_by_hour.index, uv_by_hour.values, step='mid', alpha=0.3, color='gold')
plt.xlabel('Hour of Day')
plt.ylabel('UV Index')
plt.title('Average UV Index by Hour')
plt.xticks(range(0, 24))
plt.tight_layout()
plt.savefig('12_step_uv.png')
plt.show()


# 13. Dual Axis - Temperature and Pressure together
fig, ax1 = plt.subplots(figsize=(12, 4))
ax1.plot(df['datetime_local'], df['temperature'], color='red', label='Temperature')
ax1.set_ylabel('Temperature (C)', color='red')

ax2 = ax1.twinx()
ax2.plot(df['datetime_local'], df['pressure'], color='blue', linestyle='--', label='Pressure')
ax2.set_ylabel('Pressure (hPa)', color='blue')

plt.title('Temperature and Pressure Over Time')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('13_dual_temp_pressure.png')
plt.show()


# 14. Pie Chart - Day vs Night hours
day_count   = df[(df['hour'] >= 6) & (df['hour'] <= 18)].shape[0]
night_count = df.shape[0] - day_count

plt.figure(figsize=(6, 6))
plt.pie([day_count, night_count], labels=['Daytime', 'Nighttime'],
        autopct='%1.1f%%', colors=['gold', 'navy'], startangle=90)
plt.title('Day vs Night Hours')
plt.tight_layout()
plt.savefig('14_pie_day_night.png')
plt.show()


# 15. Line Chart - Wind speed and gust together
plt.figure(figsize=(12, 4))
plt.plot(df['datetime_local'], df['wind_speed'], label='Wind Speed', color='green')
plt.plot(df['datetime_local'], df['wind_gust'],  label='Wind Gust',  color='orange', linestyle='--')
plt.xlabel('Date')
plt.ylabel('m/s')
plt.title('Wind Speed vs Wind Gust')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('15_line_wind.png')
plt.show()


# 16. Histogram - Wind speed distribution
plt.figure(figsize=(8, 4))
plt.hist(df['wind_speed'], bins=15, color='mediumseagreen', edgecolor='black')
plt.xlabel('Wind Speed (m/s)')
plt.ylabel('Count')
plt.title('Wind Speed Distribution')
plt.tight_layout()
plt.savefig('16_histogram_wind.png')
plt.show()
