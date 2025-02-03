import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Bike Sharing Analysis",
    page_icon="🚲",
    layout="wide"
)

# 1. Data Wrangling
@st.cache_data
def load_data():
    """Load and prepare the datasets"""
    # Load datasets
    day_df = pd.read_csv('data/day.csv')
    hour_df = pd.read_csv('data/hour.csv')
    
    # Data cleaning and preparation
    # Convert dates to datetime
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    # Create meaningful category labels
    season_labels = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    weather_labels = {
        1: 'Clear',
        2: 'Mist/Cloudy',
        3: 'Light Rain/Snow',
        4: 'Heavy Rain/Snow'
    }
    
    # Apply labels
    day_df['season'] = day_df['season'].map(season_labels)
    hour_df['season'] = hour_df['season'].map(season_labels)
    day_df['weathersit'] = day_df['weathersit'].map(weather_labels)
    hour_df['weathersit'] = hour_df['weathersit'].map(weather_labels)
    
    return day_df, hour_df

# Load data
day_df, hour_df = load_data()

# 2. Exploratory Data Analysis
def calculate_summary_stats(df):
    """Calculate key statistics from the data"""
    stats = {
        'total_rentals': df['cnt'].sum(),
        'avg_daily_rentals': df['cnt'].mean(),
        'max_rentals': df['cnt'].max(),
        'min_rentals': df['cnt'].min(),
        'casual_ratio': df['casual'].sum() / df['cnt'].sum(),
        'registered_ratio': df['registered'].sum() / df['cnt'].sum()
    }
    return stats

# 3. Data Visualization Functions
def create_rental_trend(df):
    """Create time series plot of rental trends"""
    fig, ax = plt.subplots(figsize=(12, 6))
    df.groupby('dteday')['cnt'].mean().plot(ax=ax)
    ax.set_title('Rental Trends Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Rentals')
    return fig

def create_season_analysis(df):
    """Create seasonal analysis visualization"""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x='season', y='cnt', ax=ax)
    ax.set_title('Rental Distribution by Season')
    ax.set_xlabel('Season')
    ax.set_ylabel('Number of Rentals')
    plt.xticks(rotation=45)
    return fig

def create_weather_impact(df):
    """Create weather impact visualization"""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df, x='weathersit', y='cnt', ax=ax)
    ax.set_title('Average Rentals by Weather Condition')
    ax.set_xlabel('Weather Condition')
    ax.set_ylabel('Average Number of Rentals')
    plt.xticks(rotation=45)
    return fig

def create_hourly_pattern(df):
    """Create hourly pattern visualization"""
    hourly_avg = df.groupby('hr')['cnt'].mean()
    fig, ax = plt.subplots(figsize=(12, 6))
    hourly_avg.plot(kind='line', marker='o', ax=ax)
    ax.set_title('Average Rentals by Hour')
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Average Number of Rentals')
    return fig

# 4. Dashboard Layout
st.title('🚲 Bike Sharing Analysis Dashboard')
st.write('Analysis of bike sharing patterns based on historical data')

# Sidebar filters
st.sidebar.title('📊 Analysis Options')
analysis_type = st.sidebar.selectbox(
    'Select Analysis View',
    ['Overview', 'Temporal Analysis', 'Weather Impact', 'User Patterns']
)

# Main content based on selected analysis
if analysis_type == 'Overview':
    # Summary statistics
    st.header('📈 Key Metrics')
    stats = calculate_summary_stats(day_df)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Total Rentals', f"{stats['total_rentals']:,.0f}")
    with col2:
        st.metric('Average Daily Rentals', f"{stats['avg_daily_rentals']:,.0f}")
    with col3:
        st.metric('Maximum Daily Rentals', f"{stats['max_rentals']:,.0f}")
    
    # Overall trend
    st.subheader('📊 Overall Rental Trends')
    st.pyplot(create_rental_trend(day_df))

elif analysis_type == 'Temporal Analysis':
    st.header('⏰ Temporal Analysis')
    
    # Seasonal patterns
    st.subheader('🌺 Seasonal Patterns')
    st.pyplot(create_season_analysis(day_df))
    
    # Hourly patterns
    st.subheader('🕒 Hourly Patterns')
    st.pyplot(create_hourly_pattern(hour_df))

elif analysis_type == 'Weather Impact':
    st.header('🌤️ Weather Impact Analysis')
    
    # Weather impact
    st.pyplot(create_weather_impact(day_df))
    
    # Temperature correlation
    st.subheader('🌡️ Temperature Impact')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=day_df, x='temp', y='cnt', hue='season', ax=ax)
    ax.set_title('Rental Count vs Temperature by Season')
    st.pyplot(fig)

elif analysis_type == 'User Patterns':
    st.header('👥 User Pattern Analysis')
    
    # Calculate user statistics for this section
    user_stats = calculate_summary_stats(day_df)
    
    # User type distribution
    st.subheader('📊 Distribution of User Types')
    user_dist = pd.DataFrame({
        'User Type': ['Casual', 'Registered'],
        'Percentage': [user_stats['casual_ratio'] * 100, user_stats['registered_ratio'] * 100]
    })
    
    fig, ax = plt.subplots(figsize=(8, 8))
    plt.pie(user_dist['Percentage'], 
            labels=user_dist['User Type'], 
            autopct='%1.1f%%',
            colors=['lightblue', 'lightcoral'])
    plt.title('Distribution of User Types')
    st.pyplot(fig)
    
    # User patterns by day type
    st.subheader('📅 Usage Patterns by Day Type')
    workday_avg = day_df.groupby('workingday')[['casual', 'registered']].mean()
    
    # Create a more informative bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    workday_avg.plot(kind='bar', ax=ax)
    plt.title('Average Users by Day Type')
    plt.xlabel('Day Type (0 = Weekend/Holiday, 1 = Workday)')
    plt.ylabel('Average Number of Users')
    plt.legend(title='User Type')
    plt.xticks(rotation=0)
    st.pyplot(fig)

# Footer
st.markdown('---')
st.markdown('*Data source: Bike Sharing Dataset*')