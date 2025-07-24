import pandas as pd
import re

# Nilai tukar Dolar ke Rupiah
EXCHANGE_RATE = 16000

def transform_data(data: list):
    """
    Membersihkan dan mentransformasi data produk.
    
    Args:
        data (list): Daftar produk mentah dari tahap ekstraksi.
        
    Returns:
        pd.DataFrame: DataFrame yang sudah bersih dan siap dimuat.
    """
    if not data:
        print("Tidak ada data untuk ditransformasi.")
        return pd.DataFrame()
        
    try:
        # Buat DataFrame dari data mentah
        df = pd.DataFrame(data)
        print(f"Data awal: {len(df)} baris")

        # 1. Hapus produk yang tidak valid
        df = df[df['Title'] != 'Unknown Product'].copy()
        print(f"Setelah menghapus 'Unknown Product': {len(df)} baris")

        # 2. Transformasi kolom 'Price'
        # Ubah menjadi numerik, kalikan dengan kurs, tangani nilai yang tidak valid
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        df = df.dropna(subset=['Price']).copy()
        df['Price'] = df['Price'] * EXCHANGE_RATE
        print(f"Setelah membersihkan Price: {len(df)} baris")

        # 3. Transformasi kolom 'Rating'
        # Ekstrak angka rating saja dan konversi ke float
        def clean_rating(rating_str):
            if pd.isna(rating_str) or rating_str == 'Invalid':
                return None
            # Ekstrak angka dari string rating
            match = re.search(r'(\d+\.?\d*)', str(rating_str))
            if match:
                return float(match.group(1))
            return None
        
        df['Rating'] = df['Rating'].apply(clean_rating)
        df = df.dropna(subset=['Rating']).copy()
        print(f"Setelah membersihkan Rating: {len(df)} baris")

        # 4. Transformasi kolom 'Colors'
        # Ekstrak angka jumlah warna dan konversi ke integer
        def clean_colors(colors_str):
            if pd.isna(colors_str) or colors_str == 'N/A':
                return None
            # Ekstrak angka dari string colors
            match = re.search(r'(\d+)', str(colors_str))
            if match:
                return int(match.group(1))
            return None
        
        df['Colors'] = df['Colors'].apply(clean_colors)
        df = df.dropna(subset=['Colors']).copy()
        print(f"Setelah membersihkan Colors: {len(df)} baris")
        
        # 5. Bersihkan kolom Size dan Gender dari prefix
        df['Size'] = df['Size'].astype(str).str.replace('Size:', '').str.strip()
        df['Gender'] = df['Gender'].astype(str).str.replace('Gender:', '').str.strip()
        
        # Hapus data dengan Size atau Gender yang tidak valid
        df = df[(df['Size'] != 'N/A') & (df['Gender'] != 'N/A')].copy()
        print(f"Setelah membersihkan Size dan Gender: {len(df)} baris")
        
        # 6. Hapus duplikat
        df = df.drop_duplicates().copy()
        print(f"Setelah menghapus duplikat: {len(df)} baris")
        
        # 7. Pastikan tipe data sesuai
        df = df.astype({
            'Title': 'object',
            'Price': 'float64',
            'Rating': 'float64',
            'Colors': 'int64',
            'Size': 'object',
            'Gender': 'object',
            'Timestamp': 'object'
        })
        
        print(f"Transformasi selesai. Jumlah data bersih: {len(df)}")
        return df
    
    except Exception as e:
        # Fitur Advanced: Tangani error tak terduga selama transformasi
        print(f"Terjadi error saat transformasi: {e}")
        return pd.DataFrame()  # Kembalikan DataFrame kosong jika error