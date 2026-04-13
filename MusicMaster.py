import streamlit as st
st.set_page_config(layout="wide", page_title="Music Streaming Dashboard")

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv('Global_Music_Streaming_Listener_Preferences.csv')
    return df

df = load_data()

st.title("🎵 Global Music Streaming Listener Preferences Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=df['Country'].unique(),
    default=df['Country'].unique()
)

selected_platforms = st.sidebar.multiselect(
    "Select Streaming Platforms",
    options=df['Streaming Platform'].unique(),
    default=df['Streaming Platform'].unique()
)

selected_genres = st.sidebar.multiselect(
    "Select Top Genres",
    options=df['Top Genre'].unique(),
    default=df['Top Genre'].unique()
)

age_range = st.sidebar.slider(
    "Select Age Range",
    min_value=int(df['Age'].min()),
    max_value=int(df['Age'].max()),
    value=(int(df['Age'].min()), int(df['Age'].max()))
)

# Apply filters
filtered_df = df[
    (df['Country'].isin(selected_countries)) &
    (df['Streaming Platform'].isin(selected_platforms)) &
    (df['Top Genre'].isin(selected_genres)) &
    (df['Age'] >= age_range[0]) &
    (df['Age'] <= age_range[1])
]

# Overview section
st.header("📊 Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Users", len(filtered_df))
col2.metric("Average Minutes Streamed/Day", round(filtered_df['Minutes Streamed Per Day'].mean(), 1))
col3.metric("Average Songs Liked", round(filtered_df['Number of Songs Liked'].mean(), 1))

# Platform and Genre Distribution
st.header("📈 Platform and Genre Distribution")
tab1, tab2, tab3 = st.tabs(["Platform Distribution", "Genre Distribution", "Platform vs Genre"])

with tab1:
    platform_counts = filtered_df['Streaming Platform'].value_counts().reset_index()
    platform_counts.columns = ['Platform', 'Count']
    fig1 = px.pie(platform_counts, values='Count', names='Platform', 
                 title='Streaming Platform Market Share')
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    genre_counts = filtered_df['Top Genre'].value_counts().reset_index()
    genre_counts.columns = ['Genre', 'Count']
    fig2 = px.bar(genre_counts.sort_values('Count', ascending=False), 
                 x='Genre', y='Count', 
                 title='Top Genre Popularity')
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    platform_genre = filtered_df.groupby(['Streaming Platform', 'Top Genre']).size().reset_index()
    platform_genre.columns = ['Platform', 'Genre', 'Count']
    fig3 = px.sunburst(platform_genre, path=['Platform', 'Genre'], values='Count',
                      title='Genre Distribution by Platform')
    st.plotly_chart(fig3, use_container_width=True)

# Geographic Distribution
st.header("🌍 Geographic Distribution")
geo_col1, geo_col2 = st.columns(2)

with geo_col1:
    country_counts = filtered_df['Country'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Count']
    fig4 = px.choropleth(country_counts, 
                        locations='Country', 
                        locationmode='country names',
                        color='Count',
                        title='User Distribution by Country')
    st.plotly_chart(fig4, use_container_width=True)

with geo_col2:
    country_platform = filtered_df.groupby(['Country', 'Streaming Platform']).size().reset_index()
    country_platform.columns = ['Country', 'Platform', 'Count']
    fig5 = px.bar(country_platform, 
                 x='Country', 
                 y='Count', 
                 color='Platform',
                 title='Platform Popularity by Country')
    st.plotly_chart(fig5, use_container_width=True)

# User Behavior Analysis
st.header("👤 User Behavior Analysis")
behavior_tab1, behavior_tab2, behavior_tab3 = st.tabs(["Listening Time", "Subscription Type", "Artist Popularity"])

with behavior_tab1:
    listening_time = filtered_df['Listening Time (Morning/Afternoon/Night)'].value_counts().reset_index()
    listening_time.columns = ['Time', 'Count']
    fig6 = px.pie(listening_time, values='Count', names='Time', 
                 title='Preferred Listening Times')
    st.plotly_chart(fig6, use_container_width=True)

with behavior_tab2:
    subscription_counts = filtered_df['Subscription Type'].value_counts().reset_index()
    subscription_counts.columns = ['Type', 'Count']
    fig7 = px.bar(subscription_counts, 
                 x='Type', 
                 y='Count', 
                 color='Type',
                 title='Free vs Premium Subscriptions')
    st.plotly_chart(fig7, use_container_width=True)

with behavior_tab3:
    top_artists = filtered_df['Most Played Artist'].value_counts().head(10).reset_index()
    top_artists.columns = ['Artist', 'Count']
    fig8 = px.bar(top_artists.sort_values('Count', ascending=True), 
                 x='Count', 
                 y='Artist', 
                 orientation='h',
                 title='Top 10 Most Played Artists')
    st.plotly_chart(fig8, use_container_width=True)

# Age and Streaming Patterns
st.header("👥 Age and Streaming Patterns")
age_tab1, age_tab2 = st.tabs(["Age Distribution", "Age vs Streaming"])

with age_tab1:
    fig9 = px.histogram(filtered_df, x='Age', nbins=20, 
                       title='Age Distribution of Users')
    st.plotly_chart(fig9, use_container_width=True)

with age_tab2:
    fig10 = px.scatter(filtered_df, 
                      x='Age', 
                      y='Minutes Streamed Per Day', 
                      color='Subscription Type',
                      title='Daily Streaming Minutes by Age')
    st.plotly_chart(fig10, use_container_width=True)

# Engagement Metrics
st.header("📱 Engagement Metrics")
engage_col1, engage_col2 = st.columns(2)

with engage_col1:
    fig11 = px.box(filtered_df, 
                  y='Discover Weekly Engagement (%)', 
                  title='Discover Weekly Engagement Distribution')
    st.plotly_chart(fig11, use_container_width=True)

with engage_col2:
    fig12 = px.box(filtered_df, 
                  y='Repeat Song Rate (%)', 
                  title='Repeat Song Rate Distribution')
    st.plotly_chart(fig12, use_container_width=True)

# Correlation Analysis
st.header("🔗 Correlation Analysis")
corr_tab1, corr_tab2 = st.tabs(["Numerical Features", "Custom Comparison"])

with corr_tab1:
    numerical_cols = ['Age', 'Minutes Streamed Per Day', 'Number of Songs Liked', 
                     'Discover Weekly Engagement (%)', 'Repeat Song Rate (%)']
    corr_df = filtered_df[numerical_cols].corr()
    fig13 = px.imshow(corr_df, 
                     text_auto=True, 
                     aspect="auto",
                     title='Correlation Matrix of Numerical Features')
    st.plotly_chart(fig13, use_container_width=True)

with corr_tab2:
    col1, col2 = st.columns(2)
    with col1:
        x_axis = st.selectbox("X-axis", options=numerical_cols, index=0)
    with col2:
        y_axis = st.selectbox("Y-axis", options=numerical_cols, index=1)
    
    color_by = st.selectbox("Color by", options=['Subscription Type', 'Streaming Platform', 'Top Genre'])
    
    fig14 = px.scatter(filtered_df, 
                      x=x_axis, 
                      y=y_axis, 
                      color=color_by,
                      title=f'{x_axis} vs {y_axis} by {color_by}')
    st.plotly_chart(fig14, use_container_width=True)

# Data Table
st.header("📋 Raw Data")
st.dataframe(filtered_df)
