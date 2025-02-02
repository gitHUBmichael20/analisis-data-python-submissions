# Bike Sharing Analysis Dashboard

## Deskripsi
Project ini menganalisis dataset Bike Sharing untuk memahami pola penggunaan sepeda sewaan berdasarkan berbagai faktor seperti cuaca, waktu, dan tipe hari. Dashboard interaktif dibuat menggunakan Streamlit untuk memvisualisasikan insight dari data.

## Setup Project
1. Pastikan Python sudah terinstall di sistem anda
2. Install dependencies yang diperlukan:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan dashboard:
   ```bash
   streamlit run dashboard.py
   ```

## Struktur Project
```
├── dashboard/
│   ├── dashboard.py
│   └── data/
│       ├── day.csv
│       └── hour.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Dataset
Dataset yang digunakan adalah Bike Sharing Dataset yang berisi informasi peminjaman sepeda per jam dan per hari, termasuk:
- Informasi cuaca (temperatur, kelembaban, kecepatan angin)
- Informasi waktu (jam, hari, bulan, tahun)
- Tipe hari (hari kerja/libur)
- Jumlah peminjaman (casual, registered, total)