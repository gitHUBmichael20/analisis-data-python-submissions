import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(
    page_title="Bike Sharing Analysis Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Load and Prepare Data
@st.cache_data
def load_data():
    day_df = pd.read_csv('data/day.csv')
    hour_df = pd.read_csv('data/hour.csv')
    
    # Convert dates to datetime
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    # Define categorical labels
    season_labels = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    weather_labels = {
        1: 'Clear', 2: 'Mist/Cloudy', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'
    }
    
    # Apply labels
    day_df['season'] = day_df['season'].map(season_labels)
    hour_df['season'] = hour_df['season'].map(season_labels)
    day_df['weathersit'] = day_df['weathersit'].map(weather_labels)
    hour_df['weathersit'] = hour_df['weathersit'].map(weather_labels)
    
    return day_df, hour_df

day_df, hour_df = load_data()

# Sidebar Filters
st.sidebar.title("🔍 Filters")
selected_season = st.sidebar.multiselect("Select Season", options=day_df['season'].unique(), default=day_df['season'].unique())
selected_weather = st.sidebar.multiselect("Select Weather", options=day_df['weathersit'].unique(), default=day_df['weathersit'].unique())

filtered_day_df = day_df[(day_df['season'].isin(selected_season)) & (day_df['weathersit'].isin(selected_weather))]

# Main Dashboard Content
st.title("🚲 Bike Sharing Analysis Dashboard")
st.markdown("### 📌 Pertanyaan Penelitian")
st.write("1️⃣ **Bagaimana pola penggunaan sepeda sepanjang hari dan musim?**")
st.write("2️⃣ **Bagaimana cuaca mempengaruhi jumlah penyewaan sepeda?**")

# Visualization
st.subheader("📊 Pola Penggunaan Sepeda")
daily_usage = filtered_day_df.groupby('season')['cnt'].mean()
fig, ax = plt.subplots()
daily_usage.plot(kind='bar', color='skyblue', ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda per Musim")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

st.subheader("🌦️ Pengaruh Cuaca terhadap Penyewaan")
fig, ax = plt.subplots()
sns.boxplot(data=filtered_day_df, x='weathersit', y='cnt', ax=ax)
ax.set_title("Distribusi Penyewaan Sepeda Berdasarkan Cuaca")
st.pyplot(fig)

# Dynamic Conclusion
st.subheader("📌 Kesimpulan Dinamis")
st.markdown(f"- **Musim dengan rata-rata penyewaan tertinggi:** {daily_usage.idxmax()} dengan {daily_usage.max():.0f} penyewaan rata-rata per hari.")
st.markdown(f"- **Musim dengan rata-rata penyewaan terendah:** {daily_usage.idxmin()} dengan {daily_usage.min():.0f} penyewaan rata-rata per hari.")
