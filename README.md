# Fashion Studio ETL Pipeline

## Deskripsi Proyek

Proyek ini adalah implementasi **ETL (Extract, Transform, Load) Pipeline** untuk menganalisis data produk dari situs "Fashion Studio". Pipeline ini dirancang dengan prinsip modular dan dilengkapi dengan unit testing yang komprehensif untuk mencapai standar kualitas tinggi.

## Fitur Utama

### 🔍 Extract (Ekstraksi)
- Web scraping dari 50 halaman https://fashion-studio.dicoding.dev
- Error handling untuk masalah jaringan dan timeout
- Timestamp otomatis untuk pelacakan waktu ekstraksi
- Ekstraksi data: Title, Price, Rating, Colors, Size, Gender

### 🔄 Transform (Transformasi)
- Konversi harga dari USD ke IDR (1 USD = Rp 16.000)
- Pembersihan dan validasi data rating, colors, size, gender
- Penghapusan data duplikat dan tidak valid
- Konversi tipe data yang sesuai
- Penanganan nilai null dan missing values

### 💾 Load (Pemuatan)
- **CSV**: Simpan ke file `products.csv`
- **Google Sheets**: Simpan ke spreadsheet online
- **PostgreSQL**: Simpan ke database relasional

## Struktur Proyek

```
fashion-studio-ETL/
├── utils/
│   ├── __init__.py
│   ├── extract.py         # Modul ekstraksi data
│   ├── transform.py       # Modul transformasi data
│   └── load.py           # Modul pemuatan data
├── tests/
│   ├── test_extract.py   # Unit test untuk ekstraksi
│   ├── test_transform.py # Unit test untuk transformasi
│   └── test_load.py      # Unit test untuk pemuatan
├── main.py               # Skrip utama pipeline ETL
├── requirements.txt      # Dependencies
├── submission.txt        # Panduan lengkap
├── README.md            # Dokumentasi ini
└── products.csv         # Output data (dibuat otomatis)
```

## Instalasi dan Setup

### 1. Clone Repository
```bash
git clone https://github.com/Koerentji/etl-dicoding.git
cd etl-dicoding
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Google Sheets API (Opsional)
1. Buat project di [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Google Sheets API dan Google Drive API
3. Buat Service Account dan download kredensial JSON
4. Rename file kredensial menjadi `google-sheets-api.json`
5. Letakkan file di root directory proyek

### 4. Setup PostgreSQL (Opsional)
Edit konfigurasi database di `utils/load.py`:
```python
db_config = {
    'host': 'localhost',
    'database': 'fashion_studio',
    'user': 'postgres',
    'password': 'password',
    'port': '5432'
}
```

## Cara Penggunaan

### Menjalankan Pipeline ETL
```bash
python main.py
```

### Menjalankan Unit Tests
```bash
# Semua test
pytest tests/

# Test dengan output verbose
pytest tests/ -v

# Test spesifik
pytest tests/test_extract.py
```

### Test Coverage
```bash
# Jalankan coverage
coverage run -m pytest tests/

# Lihat laporan
coverage report -m

# Buat laporan HTML
coverage html
```

## Kriteria Penilaian yang Dipenuhi

### ✅ Kriteria 1: ETL Pipeline Modular (4 Poin)
- **Struktur Modular**: Setiap tahap ETL dipisah dalam file berbeda
- **Error Handling**: Implementasi try-catch di setiap modul
- **Timestamp**: Pelacakan waktu ekstraksi data
- **Dokumentasi**: Kode terdokumentasi dengan baik

### ✅ Kriteria 2: Repositori Data (4 Poin)
- **Flat File**: Export ke CSV
- **Google Sheets**: Integrasi dengan Google Sheets API
- **Database**: Simpan ke PostgreSQL dengan auto table creation

### ✅ Kriteria 3: Unit Testing (4 Poin)
- **Test Coverage**: Target 80-100%
- **Comprehensive Testing**: Test untuk semua skenario
- **Mocking**: Simulasi eksternal dependencies
- **Error Testing**: Test untuk error handling

## Teknologi yang Digunakan

- **Python 3.8+**
- **pandas**: Data manipulation
- **requests**: HTTP requests
- **BeautifulSoup4**: Web scraping
- **psycopg2**: PostgreSQL connector
- **gspread**: Google Sheets API
- **pytest**: Unit testing framework
- **coverage**: Test coverage measurement

## Output yang Dihasilkan

1. **products.csv**: File CSV dengan data produk yang sudah dibersihkan
2. **Google Sheets**: Spreadsheet online yang dapat diakses dan dibagikan
3. **PostgreSQL Table**: Tabel database untuk analisis lanjutan
4. **Test Reports**: Laporan coverage dan hasil testing

## Troubleshooting

### Error "Module not found"
```bash
pip install -r requirements.txt
```

### Error Google Sheets API
- Pastikan file `google-sheets-api.json` ada dan valid
- Pastikan Google Sheets API sudah diaktifkan

### Error PostgreSQL
- Pastikan PostgreSQL server berjalan
- Periksa konfigurasi koneksi

### Error saat Scraping
- Periksa koneksi internet
- Website mungkin mengalami perubahan struktur

## Kontribusi

Proyek ini dibuat untuk memenuhi submission Dicoding "Belajar Fundamental Pemrosesan Data". 

## Lisensi

MIT License - Lihat file LICENSE untuk detail lengkap.

---

**Dibuat dengan ❤️ untuk mencapai Bintang 5 ⭐⭐⭐⭐⭐**