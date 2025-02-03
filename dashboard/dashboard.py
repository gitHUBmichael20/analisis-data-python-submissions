import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Bike Sharing Analysis Dashboard",
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

# 2. Exploratory Data Analysis Functions
def analyze_temporal_patterns(df):
    """Analyze temporal patterns of bike rentals"""
    # Hourly analysis
    hourly_usage = df.groupby('hr')['cnt'].mean()
    peak_hours = hourly_usage.nlargest(3)
    
    # Daily analysis
    daily_usage = df.groupby('weekday')['cnt'].mean()
    peak_days = daily_usage.nlargest(3)
    
    return {
        'peak_hours': peak_hours,
        'peak_days': peak_days,
        'avg_hourly_usage': hourly_usage.mean(),
        'total_rentals': df['cnt'].sum()
    }

def analyze_weather_impact(df):
    """Analyze the impact of weather on bike rentals"""
    # Weather situation analysis
    weather_usage = df.groupby('weathersit')['cnt'].agg(['mean', 'count'])
    
    # Temperature correlation
    temp_correlation = df['temp'].corr(df['cnt'])
    
    # Rental reduction in bad weather
    baseline_rentals = df[df['weathersit'] == 'Clear']['cnt'].mean()
    weather_impact = {}
    for weather in df['weathersit'].unique():
        if weather != 'Clear':
            weather_rentals = df[df['weathersit'] == weather]['cnt'].mean()
            weather_impact[weather] = (baseline_rentals - weather_rentals) / baseline_rentals * 100
    
    return {
        'weather_usage': weather_usage,
        'temp_correlation': temp_correlation,
        'rental_reduction': weather_impact
    }

# 3. Additional Analysis Functions
def analyze_seasonal_yearly_trends(df):
    """Analyze seasonal and yearly trends"""
    seasonal_yearly_rental = df.groupby(['yr', 'season'])['cnt'].mean().unstack()
    return seasonal_yearly_rental

def analyze_holiday_impact(df):
    """Analyze the impact of holidays on rentals"""
    holiday_rental = df.groupby('holiday')['cnt'].agg(['mean', 'median', 'count'])
    return holiday_rental

def analyze_weather_comfort(df):
    """Analyze weather comfort factors"""
    comfort_factors = ['temp', 'atemp', 'hum', 'windspeed', 'cnt']
    correlation_matrix = df[comfort_factors].corr()
    return correlation_matrix

def analyze_user_characteristics(df):
    """Analyze user characteristics across time"""
    hourly_user_dist = df.groupby('hr')[['casual', 'registered']].mean()
    return hourly_user_dist

# 4. Visualization Functions
def create_peak_hours_visualization(hourly_usage):
    """Create visualization of peak hours"""
    fig, ax = plt.subplots(figsize=(12, 6))
    hourly_usage.plot(kind='line', marker='o', ax=ax)
    ax.set_title('Average Bike Rentals by Hour of Day')
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Average Number of Rentals')
    return fig

def create_weather_impact_visualization(df):
    """Create visualization of weather impact"""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x='weathersit', y='cnt', ax=ax)
    ax.set_title('Bike Rentals by Weather Situation')
    ax.set_xlabel('Weather Condition')
    ax.set_ylabel('Number of Rentals')
    plt.xticks(rotation=45)
    return fig

# 5. Dashboard Layout
st.title('🚲 Comprehensive Bike Sharing Analysis')

# Sidebar for Business Questions
st.sidebar.title('🎯 Business Insights')
business_question = st.sidebar.selectbox(
    'Select Business Insight',
    [
        'Q1: Optimizing Rental Capacity',
        'Q2: Weather Impact Mitigation',
        'Q3: Seasonal and Yearly Trends',
        'Q4: Holiday Impact Analysis',
        'Q5: Weather Comfort Factors',
        'Q6: User Characteristics'
    ]
)

# Main Dashboard Content
if business_question == 'Q1: Optimizing Rental Capacity':
    st.header('📊 Rental Capacity Optimization Analysis')
    
    # Temporal Pattern Analysis
    temporal_analysis = analyze_temporal_patterns(hour_df)
    
    # Key Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Total Rentals', f"{temporal_analysis['total_rentals']:,}")
    with col2:
        st.metric('Average Hourly Rentals', f"{temporal_analysis['avg_hourly_usage']:.0f}")
    with col3:
        st.metric('Peak Hour Rental', f"{temporal_analysis['peak_hours'].max():.0f}")
    
    # Peak Hours Visualization
    st.subheader('🕒 Peak Rental Hours')
    st.pyplot(create_peak_hours_visualization(hour_df.groupby('hr')['cnt'].mean()))
    
    # Detailed Insights
    st.subheader('🔍 Key Insights')
    st.markdown(f"""
    - **Top 3 Peak Hours:** 
      {', '.join([f"{hour}:00" for hour in temporal_analysis['peak_hours'].index])}
    - **Highest Hourly Average:** {temporal_analysis['peak_hours'].max():.0f} rentals
    - **Recommended Capacity Allocation:** Focus on peak hours during workdays
    """)

elif business_question == 'Q2: Weather Impact Mitigation':
    st.header('🌦️ Weather Impact Analysis')
    
    # Weather Impact Analysis
    weather_analysis = analyze_weather_impact(day_df)
    
    # Key Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Temperature Correlation', f"{weather_analysis['temp_correlation']:.2f}")
    with col2:
        st.metric('Clear Weather Rentals', f"{weather_analysis['weather_usage'].loc['Clear', 'mean']:.0f}")
    with col3:
        st.metric('Worst Weather Rental Drop', f"{max(weather_analysis['rental_reduction'].values()):.1f}%")
    
    # Weather Impact Visualization
    st.subheader('🌈 Rental Performance by Weather')
    st.pyplot(create_weather_impact_visualization(day_df))
    
    # Detailed Insights
    st.subheader('🔍 Weather Mitigation Strategies')
    st.markdown("""
    - **Rental Reduction by Weather:**
    {}
    - **Recommendation:** Develop targeted marketing and operational strategies for different weather conditions
    """.format(
        '\n'.join([f"  - {weather}: {reduction:.1f}% decrease" 
                   for weather, reduction in weather_analysis['rental_reduction'].items()])
    ))

elif business_question == 'Q3: Seasonal and Yearly Trends':
    st.header('🍂 Seasonal and Yearly Trends Analysis')
    
    # Seasonal Yearly Analysis
    seasonal_trends = analyze_seasonal_yearly_trends(day_df)
    
    # Visualization
    fig, ax = plt.subplots(figsize=(12, 6))
    seasonal_trends.plot(kind='bar', ax=ax)
    ax.set_title('Average Bike Rentals by Season and Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Average Number of Rentals')
    ax.legend(title='Season')
    
    st.pyplot(fig)
    
    # Insights
    st.subheader('🔍 Key Insights')
    st.markdown("""
    - Analyze rental patterns across different seasons
    - Identify potential seasonal variations
    - Compare rental trends between years
    """)

elif business_question == 'Q4: Holiday Impact Analysis':
    st.header('🏖️ Holiday Impact on Bike Rentals')
    
    # Holiday Impact Analysis
    holiday_analysis = analyze_holiday_impact(day_df)
    
    # Visualization
    fig, ax = plt.subplots(figsize=(10, 6))
    holiday_analysis['mean'].plot(kind='bar', ax=ax)
    ax.set_title('Average Bike Rentals: Holiday vs Non-Holiday')
    ax.set_xlabel('Holiday Status')
    ax.set_ylabel('Average Number of Rentals')
    
    st.pyplot(fig)
    
    # Insights
    st.subheader('🔍 Key Insights')
    st.markdown(f"""
    - **Holiday Rentals:** {holiday_analysis.loc[1, 'mean']:.0f}
    - **Non-Holiday Rentals:** {holiday_analysis.loc[0, 'mean']:.0f}
    - **Difference:** {abs(holiday_analysis.loc[1, 'mean'] - holiday_analysis.loc[0, 'mean']):.0f} rentals
    - Understand rental behavior during holidays
    """)

elif business_question == 'Q5: Weather Comfort Factors':
    st.header('🌡️ Weather Comfort and Rental Correlation')
    
    # Weather Comfort Analysis
    comfort_correlation = analyze_weather_comfort(day_df)
    
    # Visualization
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(comfort_correlation, annot=True, cmap='coolwarm', center=0, ax=ax)
    ax.set_title('Correlation between Weather Factors and Rentals')
    
    st.pyplot(fig)
    
    # Insights
    st.subheader('🔍 Key Insights')
    st.markdown("""
    - Analyze correlations between weather factors
    - Identify which factors most impact bike rentals
    - Use insights for demand prediction
    """)

elif business_question == 'Q6: User Characteristics':
    st.header('👥 User Type Characteristics')
    
    # User Characteristics Analysis
    user_dist = analyze_user_characteristics(hour_df)
    
    # Visualization
    fig, ax = plt.subplots(figsize=(12, 6))
    user_dist.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title('Casual vs Registered Users Across Hours')
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Average Number of Users')
    ax.legend(title='User Type')
    
    st.pyplot(fig)
    
    # Insights
    st.subheader('🔍 Key Insights')
    st.markdown("""
    - Analyze user type distribution throughout the day
    - Identify peak times for casual and registered users
    - Develop targeted strategies for different user types
    """)

# Footer
st.markdown('---')
st.markdown('*Data-driven insights for bike sharing optimization*')