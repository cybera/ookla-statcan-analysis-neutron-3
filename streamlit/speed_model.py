import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go


data = gpd.read_file('notebooks//output.geojson')

sd_df2 = data.dropna()

selected_column = st.selectbox('Select a column',('NL','NS','NB','QC','ON','SK','AB','BC','MB','PE','YT','NT','NU'))

# Filter based on a column
filtered_data = sd_df2[sd_df2['PRCODE'] == selected_column]
mean_pop2016 = filtered_data['Pop2016'].mean()
filtered_data = filtered_data[filtered_data['Pop2016']>mean_pop2016]

# Find top 20 and bottom 20 avg_d_speed
top_50 = filtered_data.sort_values('avg_d_kbps', ascending=False).head(50)
bottom_50 = filtered_data.sort_values('avg_d_kbps').head(50)

merged_df = pd.concat([top_50, bottom_50], axis=0)
st.write("# Hello4")
map = merged_df.explore(
    'ookla_50_10_percentile',scheme='equalinterval', k = 4, 
    tooltip=['HEXUID_PCPUID','Pop2016','Pop_Avail_50_10','ookla_50_10_percentile'],
    popup=[
        'HEXUID_PCPUID',
        'min_d_kbps','avg_d_kbps','max_d_kbps',
        'min_u_kbps','avg_u_kbps','max_u_kbps',
        'Pop2016','tests','num_tiles','unique_devices','connections',
        'Pop_Avail_50_10','ookla_50_10_percentile','Down_50_percentile','Up_10_percentile']
    )

st.write("# Hello5")

st.write("""
This is a space to work and make a new app!
""")
st_folium(map, key="main-map", returned_objects=[], height=800, width=700)