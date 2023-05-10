import pandas as pd
import geopandas as gp

data = gpd.read_file('notebooks//output.geojson')

sd_df2 = data.dropna()
# Filter based on a column
filtered_data = sd_df2[sd_df2['PRCODE'] == 'BC']
mean_pop2016 = filtered_data['Pop2016'].mean()
filtered_data = filtered_data[filtered_data['Pop2016']>mean_pop2016]

# Find top 20 and bottom 20 avg_d_speed
top_20 = filtered_data.sort_values('avg_d_kbps', ascending=False).head(20)
bottom_20 = filtered_data.sort_values('avg_d_kbps').head(20)

merged_df = pd.concat([top_20, bottom_20], axis=0)

merged_df.explore(
    'ookla_50_10_percentile',scheme='equalinterval', k = 4, 
    tooltip=['HEXUID_PCPUID','Pop2016','Pop_Avail_50_10','ookla_50_10_percentile'],
    popup=[
        'HEXUID_PCPUID',
        'min_d_kbps','avg_d_kbps','max_d_kbps',
        'min_u_kbps','avg_u_kbps','max_u_kbps',
        'Pop2016','tests','num_tiles','unique_devices','connections',
        'Pop_Avail_50_10','ookla_50_10_percentile','Down_50_percentile','Up_10_percentile']
    )