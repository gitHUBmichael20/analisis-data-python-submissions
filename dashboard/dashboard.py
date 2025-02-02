import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
day_df = pd.read_csv('data\day.csv')
hour_df = pd.read_csv('data\hour.csv')

# Dashboard Title
st.title('Analisis Data Bike Sharing')

# Analisis Data Harian
st.header('Analisis Data Harian')

# 1. Tren Penggunaan Sepeda per Bulan
st.subheader('Tren Penggunaan Sepeda per Bulan')
monthly_usage = day_df.groupby('mnth')['cnt'].mean()
fig, ax = plt.subplots(figsize=(10, 6))
monthly_usage.plot(kind='line', marker='o')
plt.title('Rata-rata Penggunaan Sepeda per Bulan')
plt.xlabel('Bulan')
plt.ylabel('Rata-rata Jumlah Peminjaman')
st.pyplot(fig)

# 2. Perbandingan Penggunaan berdasarkan Hari Kerja vs Hari Libur
st.subheader('Penggunaan pada Hari Kerja vs Hari Libur')
workday_usage = day_df.groupby('workingday')['cnt'].mean()
fig, ax = plt.subplots(figsize=(8, 6))
workday_usage.plot(kind='bar')
plt.title('Rata-rata Penggunaan: Hari Kerja vs Hari Libur')
plt.xlabel('Tipe Hari (0: Libur, 1: Kerja)')
plt.ylabel('Rata-rata Jumlah Peminjaman')
st.pyplot(fig)

# Analisis Data per Jam
st.header('Analisis Data per Jam')

# 3. Pola Penggunaan Sepeda Sepanjang Hari
st.subheader('Pola Penggunaan Sepeda Sepanjang Hari')
hourly_usage = hour_df.groupby('hr')['cnt'].mean()
fig, ax = plt.subplots(figsize=(12, 6))
hourly_usage.plot(kind='line', marker='o')
plt.title('Rata-rata Penggunaan Sepeda per Jam')
plt.xlabel('Jam')
plt.ylabel('Rata-rata Jumlah Peminjaman')
st.pyplot(fig)

# 4. Pengaruh Cuaca terhadap Penggunaan Sepeda
st.subheader('Pengaruh Cuaca terhadap Penggunaan Sepeda')
weather_usage = hour_df.groupby('weathersit')['cnt'].mean()
fig, ax = plt.subplots(figsize=(10, 6))
weather_usage.plot(kind='bar')
plt.title('Rata-rata Penggunaan Berdasarkan Kondisi Cuaca')
plt.xlabel('Kondisi Cuaca (1: Clear, 2: Mist, 3: Light Rain, 4: Heavy Rain)')
plt.ylabel('Rata-rata Jumlah Peminjaman')
st.pyplot(fig)

# 5. Perbandingan Pengguna Casual vs Registered (Data Harian)
st.subheader('Perbandingan Tipe Pengguna')
user_types = ['casual', 'registered']
user_means = day_df[user_types].mean()
fig, ax = plt.subplots(figsize=(8, 6))
user_means.plot(kind='pie', autopct='%1.1f%%')
plt.title('Proporsi Tipe Pengguna')
st.pyplot(fig)

# Kesimpulan
st.header('Kesimpulan Analisis')
st.write("""
Berdasarkan analisis data di atas, dapat disimpulkan:

1. Terdapat pola penggunaan yang jelas berdasarkan waktu:
   - Puncak penggunaan terjadi pada jam-jam sibuk (berangkat dan pulang kerja)
   - Hari kerja memiliki pola penggunaan yang berbeda dengan hari libur

2. Faktor cuaca mempengaruhi penggunaan sepeda:
   - Cuaca cerah menghasilkan jumlah peminjaman tertinggi
   - Penggunaan menurun signifikan saat hujan

3. Karakteristik pengguna:
   - Mayoritas pengguna adalah pengguna terdaftar (registered users)
   - Pengguna casual memiliki pola penggunaan yang berbeda

4. Tren bulanan menunjukkan:
   - Penggunaan lebih tinggi pada bulan-bulan dengan cuaca yang baik
   - Terdapat variasi musiman dalam penggunaan sepeda
""")