import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Caching untuk mempercepat loading data
@st.cache_data
def load_data():
    day_df = pd.read_csv('data/day.csv')
    hour_df = pd.read_csv('data/hour.csv')
    return day_df, hour_df

# Load datasets
day_df, hour_df = load_data()

# Show All Data button di bagian atas sidebar
st.sidebar.title("🔍 Filter Data")
show_all = st.sidebar.button("👁️ Tampilkan Semua Data", help="Klik untuk melihat visualisasi dari seluruh dataset")

# Filter temperatur dengan dropdown (termasuk opsi "Semua")
temp_ranges = [
    "Semua Temperatur",
    "Sangat Dingin (0.0-0.2)",
    "Dingin (0.2-0.4)",
    "Normal (0.4-0.6)",
    "Hangat (0.6-0.8)",
    "Panas (0.8-1.0)"
]
selected_temp = st.sidebar.selectbox("Temperatur", options=temp_ranges, disabled=show_all)
temp_range_map = {
    "Semua Temperatur": (0.0, 1.0),
    "Sangat Dingin (0.0-0.2)": (0.0, 0.2),
    "Dingin (0.2-0.4)": (0.2, 0.4),
    "Normal (0.4-0.6)": (0.4, 0.6),
    "Hangat (0.6-0.8)": (0.6, 0.8),
    "Panas (0.8-1.0)": (0.8, 1.0)
}
selected_temp_range = temp_range_map[selected_temp]

# Filter kondisi cuaca dengan dropdown (termasuk opsi "Semua")
weather_options = {
    0: "Semua Cuaca",
    1: "Clear/Partly Cloudy",
    2: "Misty/Cloudy",
    3: "Light Rain/Snow",
    4: "Heavy Rain/Snow"
}
selected_weather = st.sidebar.selectbox(
    "Cuaca",
    options=list(weather_options.keys()),
    format_func=lambda x: weather_options[x],
    disabled=show_all
)

# Filter hari kerja vs akhir pekan dengan dropdown (termasuk opsi "Semua")
workingday_options = {
    -1: "Semua Tipe Hari",
    0: "Akhir Pekan/Libur",
    1: "Hari Kerja"
}
selected_workingday = st.sidebar.selectbox(
    "Tipe Hari",
    options=list(workingday_options.keys()),
    format_func=lambda x: workingday_options[x],
    disabled=show_all
)

# Filter jam dengan dropdown (termasuk opsi "Semua")
hour_options = {-1: "Semua Jam"}
hour_options.update({i: f"{i:02d}:00" for i in range(24)})
selected_hour = st.sidebar.selectbox(
    "Jam",
    options=list(hour_options.keys()),
    format_func=lambda x: hour_options[x],
    disabled=show_all
)

# Filter musim dengan dropdown (termasuk opsi "Semua")
season_options = {
    0: "Semua Musim",
    1: "Musim Semi",
    2: "Musim Panas",
    3: "Musim Gugur",
    4: "Musim Dingin"
}
selected_season = st.sidebar.selectbox(
    "Musim",
    options=list(season_options.keys()),
    format_func=lambda x: season_options[x],
    disabled=show_all
)

# Dashboard Title
st.title('📊 Analisis Data Bike Sharing')
st.write("Dashboard ini memberikan wawasan tentang pola penggunaan sepeda berdasarkan data historis.")

# Fungsi untuk memfilter data berdasarkan kondisi
def filter_data(df):
    if show_all:
        return df
    
    filtered = df.copy()
    # Filter temperatur
    filtered = filtered[
        (filtered['temp'] >= selected_temp_range[0]) &
        (filtered['temp'] <= selected_temp_range[1])
    ]
    
    # Filter cuaca
    if selected_weather != 0:
        filtered = filtered[filtered['weathersit'] == selected_weather]
    
    # Filter tipe hari
    if selected_workingday != -1:
        filtered = filtered[filtered['workingday'] == selected_workingday]
    
    # Filter musim
    if selected_season != 0:
        filtered = filtered[filtered['season'] == selected_season]
    
    return filtered

# Filter hour data dengan tambahan filter jam
def filter_hour_data(df):
    filtered = filter_data(df)
    if selected_hour != -1 and not show_all:
        filtered = filtered[filtered['hr'] == selected_hour]
    return filtered

# Apply filters
filtered_day_df = filter_data(day_df)
filtered_hour_df = filter_hour_data(hour_df)

# Data Summary
st.subheader("📜 Ringkasan Data")
if show_all:
    st.write(f"Total dataset terdiri dari **{len(day_df)} hari** dan **{len(hour_df)} jam** pencatatan.")
else:
    st.write(f"Data terfilter terdiri dari **{len(filtered_day_df)} hari** dan **{len(filtered_hour_df)} jam** pencatatan.")
st.dataframe(filtered_day_df.head())

# Analisis Data Harian
st.header('📅 Analisis Data Harian')

# 1. Tren Penggunaan Sepeda berdasarkan Musim
st.subheader('📈 Tren Penggunaan Sepeda berdasarkan Musim')
if selected_season == 0 or show_all:
    seasonal_usage = filtered_day_df.groupby('season')['cnt'].mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=[season_options[s] for s in seasonal_usage.index], y=seasonal_usage.values, ax=ax)
    title = 'Rata-rata Penggunaan Sepeda per Musim'
else:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=[season_options[selected_season]], y=[filtered_day_df['cnt'].mean()], ax=ax)
    title = f'Rata-rata Penggunaan Sepeda - {season_options[selected_season]}'
ax.set_title(title)
ax.set_xlabel('Musim')
ax.set_ylabel('Rata-rata Jumlah Peminjaman')
plt.xticks(rotation=45)
st.pyplot(fig)

# 2. Pola Penggunaan Sepeda berdasarkan Cuaca
st.subheader('🕒 Pola Penggunaan Sepeda berdasarkan Cuaca')
if selected_weather == 0 or show_all:
    weather_usage = filtered_hour_df.groupby('weathersit')['cnt'].mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=[weather_options[w] for w in weather_usage.index if w in weather_options], 
                y=weather_usage.values,
                ax=ax,
                palette="coolwarm")
    title = 'Rata-rata Penggunaan Sepeda berdasarkan Cuaca'
else:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=[weather_options[selected_weather]], 
                y=[filtered_hour_df['cnt'].mean()], 
                ax=ax, 
                palette="coolwarm")
    title = f'Penggunaan Sepeda - {weather_options[selected_weather]}'
ax.set_title(title)
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Jumlah Peminjaman')
plt.xticks(rotation=45)
st.pyplot(fig)

# 3. Pengaruh Suhu terhadap Jumlah Peminjaman
st.subheader('🌡️ Pengaruh Suhu terhadap Penggunaan Sepeda')
fig, ax = plt.subplots(figsize=(10, 6))
if show_all or selected_season == 0:
    sns.scatterplot(data=filtered_day_df, x='temp', y='cnt', 
                    hue='season', palette='deep',
                    alpha=0.6, ax=ax)
    ax.legend(title='Musim', labels=[season_options[i] for i in range(1, 5)])
else:
    sns.scatterplot(data=filtered_day_df, x='temp', y='cnt', 
                    alpha=0.6, ax=ax, color='blue')
ax.set_title('Hubungan Suhu dengan Jumlah Peminjaman Sepeda')
ax.set_xlabel('Suhu (normalized)')
ax.set_ylabel('Jumlah Peminjaman')
st.pyplot(fig)

# 4. Perbandingan Pengguna Casual vs Registered
st.subheader('👥 Perbandingan Pengguna Casual vs Registered')
user_means = filtered_day_df[['casual', 'registered']].mean()
fig, ax = plt.subplots(figsize=(8, 6))
wedges, texts, autotexts = ax.pie(user_means, 
                                 labels=['Casual', 'Registered'], 
                                 autopct='%1.1f%%', 
                                 colors=['orange', 'blue'], 
                                 startangle=90,
                                 wedgeprops=dict(width=0.4))
ax.set_title('Proporsi Tipe Pengguna')
st.pyplot(fig)

# Kesimpulan Dinamis
st.header('📌 Kesimpulan Analisis')
total_rentals = filtered_day_df['cnt'].sum() if not filtered_day_df.empty else 0
avg_rentals = filtered_day_df['cnt'].mean() if not filtered_day_df.empty else 0
most_users = 'registered' if user_means['registered'] > user_means['casual'] else 'casual'
user_percentage = user_means[most_users] / user_means.sum() * 100 if user_means.sum() > 0 else 0

if show_all:
    st.write(f"""
    **Analisis Keseluruhan Dataset:**

    1. 📊 Total peminjaman sepeda: **{total_rentals:,.0f}** dengan rata-rata harian **{avg_rentals:.1f}** peminjaman
    2. 🌡️ Mencakup semua rentang temperatur
    3. 🌦️ Mencakup semua kondisi cuaca
    4. 📅 Mencakup semua tipe hari
    5. 🌺 Mencakup semua musim
    6. 👥 {'Mayoritas pengguna adalah ' + most_users + f' users dengan proporsi {user_percentage:.1f}%'}
    """)
else:
    filters_used = []
    if selected_temp != "Semua Temperatur":
        filters_used.append(f"🌡️ Temperature: **{selected_temp}**")
    if selected_weather != 0:
        filters_used.append(f"🌦️ Cuaca: **{weather_options[selected_weather]}**")
    if selected_workingday != -1:
        filters_used.append(f"📅 Tipe Hari: **{workingday_options[selected_workingday]}**")
    if selected_hour != -1:
        filters_used.append(f"🕒 Jam: **{hour_options[selected_hour]}**")
    if selected_season != 0:
        filters_used.append(f"🌺 Musim: **{season_options[selected_season]}**")
    
    st.write(f"""
    **Berdasarkan filter yang dipilih:**

    1. 📊 Total peminjaman sepeda: **{total_rentals:,.0f}** dengan rata-rata harian **{avg_rentals:.1f}** peminjaman
    
    2. Filter yang aktif:
    """)
    
    if filters_used:
        for filter_info in filters_used:
            st.write(f"   • {filter_info}")
    else:
        st.write("   • Tidak ada filter aktif")
    
    st.write(f"""
    3. 👥 {'Mayoritas pengguna adalah ' + most_users + f' users dengan proporsi {user_percentage:.1f}%' if user_percentage > 0 else 'Tidak ada data pengguna untuk filter yang dipilih'}
    """)