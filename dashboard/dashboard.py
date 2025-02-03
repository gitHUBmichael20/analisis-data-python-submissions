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

# Sidebar untuk interaksi pengguna
st.sidebar.title("🔍 Filter Data")
selected_month = st.sidebar.selectbox("Pilih Bulan", options=sorted(day_df['mnth'].unique()))
selected_hour = st.sidebar.slider("Pilih Jam", min_value=0, max_value=23, value=12)

# Dashboard Title
st.title('📊 Analisis Data Bike Sharing')
st.write("Dashboard ini memberikan wawasan tentang pola penggunaan sepeda berdasarkan data historis.")

# Data Summary
st.subheader("📜 Ringkasan Data")
st.write(f"Dataset terdiri dari **{len(day_df)} hari** dan **{len(hour_df)} jam** pencatatan.")
st.dataframe(day_df.head())  # Menampilkan sample data

# Analisis Data Harian
st.header('📅 Analisis Data Harian')

# 1. Tren Penggunaan Sepeda per Bulan
st.subheader('📈 Tren Penggunaan Sepeda per Bulan')
monthly_usage = day_df.groupby('mnth')['cnt'].mean()
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x=monthly_usage.index, y=monthly_usage.values, marker="o", ax=ax)
ax.set_title('Rata-rata Penggunaan Sepeda per Bulan')
ax.set_xlabel('Bulan')
ax.set_ylabel('Rata-rata Jumlah Peminjaman')
st.pyplot(fig)

# 2. Pola Penggunaan Sepeda per Jam (dengan filter jam)
st.subheader(f'🕒 Pola Penggunaan Sepeda pada Jam {selected_hour}')
hourly_filtered = hour_df[hour_df['hr'] == selected_hour]
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=hourly_filtered['weathersit'], y=hourly_filtered['cnt'], ax=ax, palette="coolwarm")
ax.set_title(f'Penggunaan Sepeda pada Jam {selected_hour} berdasarkan Cuaca')
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Jumlah Peminjaman')
st.pyplot(fig)

# 3. Pengaruh Suhu terhadap Jumlah Peminjaman
st.subheader('🌡️ Pengaruh Suhu terhadap Penggunaan Sepeda')
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x=day_df['temp'], y=day_df['cnt'], alpha=0.6, ax=ax)
ax.set_title('Hubungan Suhu dengan Jumlah Peminjaman Sepeda')
ax.set_xlabel('Suhu (normalized)')
ax.set_ylabel('Jumlah Peminjaman')
st.pyplot(fig)

# 4. Perbandingan Pengguna Casual vs Registered (Donut Chart)
st.subheader('👥 Perbandingan Pengguna Casual vs Registered')
user_means = day_df[['casual', 'registered']].mean()
fig, ax = plt.subplots(figsize=(8, 6))
wedges, texts, autotexts = ax.pie(user_means, labels=['Casual', 'Registered'], autopct='%1.1f%%', colors=['orange', 'blue'], startangle=90, wedgeprops=dict(width=0.4))
ax.set_title('Proporsi Tipe Pengguna')
st.pyplot(fig)

# Kesimpulan Dinamis
st.header('📌 Kesimpulan Analisis')
peak_hour = hour_df.groupby('hr')['cnt'].mean().idxmax()
peak_hour_value = hour_df.groupby('hr')['cnt'].mean().max()
low_hour = hour_df.groupby('hr')['cnt'].mean().idxmin()
low_hour_value = hour_df.groupby('hr')['cnt'].mean().min()

best_weather = hour_df.groupby('weathersit')['cnt'].mean().idxmax()
worst_weather = hour_df.groupby('weathersit')['cnt'].mean().idxmin()

most_users = 'registered' if user_means['registered'] > user_means['casual'] else 'casual'
user_percentage = user_means[most_users] / user_means.sum() * 100

st.write(f"""
**Berdasarkan analisis data, berikut adalah temuan utama:**

1. 🚀 Puncak penggunaan sepeda terjadi pada **jam {peak_hour}:00** dengan rata-rata **{peak_hour_value:.2f}** peminjaman.
   Sebaliknya, penggunaan terendah terjadi pada **jam {low_hour}:00** dengan **{low_hour_value:.2f}** peminjaman.

2. 🌦️ Kondisi cuaca sangat mempengaruhi penggunaan sepeda:
   - Penggunaan tertinggi saat cuaca **kategori {best_weather}**.
   - Penggunaan menurun drastis saat **kategori {worst_weather}**.

3. 👥 Mayoritas pengguna adalah **{most_users} users** dengan proporsi sekitar **{user_percentage:.1f}%**.

4. 📅 Penggunaan lebih tinggi pada **bulan-bulan tertentu** dibanding lainnya, menunjukkan pola musiman.

5. 🌡️ Terdapat korelasi antara suhu dan jumlah peminjaman, di mana suhu yang lebih nyaman cenderung meningkatkan jumlah pengguna.
""")
