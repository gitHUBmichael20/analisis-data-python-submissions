import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
day_df = pd.read_csv('data/day.csv')
hour_df = pd.read_csv('data/hour.csv')

# Dashboard Title
st.title('📊 Analisis Data Bike Sharing')
st.write("Dashboard ini memberikan wawasan tentang pola penggunaan sepeda berdasarkan data historis.")

# Analisis Data Harian
st.header('📅 Analisis Data Harian')

# 1. Tren Penggunaan Sepeda per Bulan
st.subheader('📈 Tren Penggunaan Sepeda per Bulan')
monthly_usage = day_df.groupby('mnth')['cnt'].mean()
fig, ax = plt.subplots(figsize=(10, 6))
monthly_usage.plot(kind='line', marker='o', ax=ax)
ax.set_title('Rata-rata Penggunaan Sepeda per Bulan')
ax.set_xlabel('Bulan')
ax.set_ylabel('Rata-rata Jumlah Peminjaman')
st.pyplot(fig)

# 2. Perbandingan Penggunaan berdasarkan Hari Kerja vs Hari Libur
st.subheader('🏢 Hari Kerja vs Hari Libur')
workday_usage = day_df.groupby('workingday')['cnt'].mean()
fig, ax = plt.subplots(figsize=(8, 6))
workday_usage.plot(kind='bar', ax=ax, color=['red', 'green'])
ax.set_title('Rata-rata Penggunaan: Hari Kerja vs Hari Libur')
ax.set_xlabel('Tipe Hari (0: Libur, 1: Kerja)')
ax.set_ylabel('Rata-rata Jumlah Peminjaman')
st.pyplot(fig)

# Analisis Data per Jam
st.header('⏰ Analisis Data per Jam')

# 3. Pola Penggunaan Sepeda Sepanjang Hari
st.subheader('🕒 Pola Penggunaan Sepeda per Jam')
hourly_usage = hour_df.groupby('hr')['cnt'].mean()
fig, ax = plt.subplots(figsize=(12, 6))
hourly_usage.plot(kind='line', marker='o', ax=ax, color='blue')
ax.set_title('Rata-rata Penggunaan Sepeda per Jam')
ax.set_xlabel('Jam')
ax.set_ylabel('Rata-rata Jumlah Peminjaman')
st.pyplot(fig)

# 4. Pengaruh Cuaca terhadap Penggunaan Sepeda
st.subheader('🌦️ Pengaruh Cuaca terhadap Penggunaan Sepeda')
weather_usage = hour_df.groupby('weathersit')['cnt'].mean()
fig, ax = plt.subplots(figsize=(10, 6))
weather_usage.plot(kind='bar', ax=ax, color=['blue', 'orange', 'gray', 'red'])
ax.set_title('Rata-rata Penggunaan Berdasarkan Kondisi Cuaca')
ax.set_xlabel('Kondisi Cuaca (1: Cerah, 2: Berkabut, 3: Hujan Ringan, 4: Hujan Lebat)')
ax.set_ylabel('Rata-rata Jumlah Peminjaman')
st.pyplot(fig)

# 5. Perbandingan Pengguna Casual vs Registered
st.subheader('👥 Perbandingan Pengguna Casual vs Registered')
user_means = day_df[['casual', 'registered']].mean()
fig, ax = plt.subplots(figsize=(8, 6))
user_means.plot(kind='pie', autopct='%1.1f%%', ax=ax, colors=['orange', 'blue'])
ax.set_title('Proporsi Tipe Pengguna')
ax.set_ylabel('')
st.pyplot(fig)

# Kesimpulan Dinamis
st.header('📌 Kesimpulan Analisis')
peak_hour = hourly_usage.idxmax()
peak_hour_value = hourly_usage.max()
low_hour = hourly_usage.idxmin()
low_hour_value = hourly_usage.min()

best_weather = weather_usage.idxmax()
worst_weather = weather_usage.idxmin()

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
""")
