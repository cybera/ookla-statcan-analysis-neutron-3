#importing libraries
import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go


@st.cache_data
@st.spinner('Waiting for the loading to finish...') 
def loadData(path):
    data = gpd.read_file(path)
    return data
data = loadData('data/model_data/output.geojson')
# Add a title
st.title("Top and Bottom 50 Regions based on Avg Download Speed")


st.header('Importance of Average Download Speed Analysis')

st.write('Understanding the average download speed across different regions in Canada is crucial in today\'s digital age. Here are a few reasons why this analysis is important:')

st.subheader('1. Internet Accessibility and Equity')
st.write('The average download speed provides insights into the accessibility and equity of internet services in various regions. Disparities in internet speeds can impact individuals, businesses, and educational institutions. Identifying regions with slower speeds helps policymakers and service providers focus on improving infrastructure and bridging the digital divide.')

st.subheader('2. User Experience and Productivity')
st.write('The average download speed directly affects the online user experience and productivity. Faster internet speeds enable smoother streaming, faster downloads, and seamless browsing. Regions with higher average download speeds are likely to offer better digital experiences, enhancing productivity for individuals, remote workers, and businesses.')

st.subheader('3. Economic Development and Innovation')
st.write('Reliable and high-speed internet connectivity is a catalyst for economic development and innovation. It fosters opportunities for e-commerce, telecommuting, and digital entrepreneurship. By identifying regions with top download speeds, policymakers and businesses can prioritize investments, attract talent, and stimulate economic growth through technology-driven initiatives.')

st.subheader('4. Infrastructure Planning and Investment')
st.write('Analyzing the average download speed helps inform infrastructure planning and investment decisions. By identifying regions with slower speeds, stakeholders can allocate resources for improving network infrastructure, expanding coverage, and upgrading existing technology. This data-driven approach ensures targeted investments that optimize connectivity and meet the evolving demands of users.')

st.write('By visualizing the top and bottom 50 regions based on average download speed, this chart provides valuable insights into the state of internet connectivity across Canada. It empowers policymakers, service providers, and users to make informed decisions, advocate for improvements, and work towards a more inclusive and connected digital future.')

#adding a selector box for the province
sel_column = st.selectbox('Select a Province',('NL','NS','NB','QC','ON','SK','AB','BC','MB','PE','YT','NT','NU'))



def calculate_top_bottom_50(selected_column):
    #reading the geopandas dataframe
    
    sd_df2 = data.dropna()
    filtered_data = sd_df2[sd_df2['PRCODE'] == selected_column]
    mean_pop2016 = filtered_data['Pop2016'].mean()
    filtered_data = filtered_data[filtered_data['Pop2016']>mean_pop2016]

    # Find top 50 and bottom 50 avg_d_speed
    top_50 = filtered_data.sort_values('avg_d_kbps', ascending=False).head(50)
    bottom_50 = filtered_data.sort_values('avg_d_kbps').head(50)

    merged_df = pd.concat([top_50, bottom_50], axis=0)

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
    return map

map2 = calculate_top_bottom_50(sel_column)
st_folium(map2, key="main-map", returned_objects=[], height=800, width=700)