from utils.extract import scrape_products
from utils.transform import transform_data
from utils.load import load_to_csv, load_to_google_sheets, load_to_postgresql

def main():
    """
    Fungsi utama untuk menjalankan seluruh pipeline ETL.
    """
    print("=" * 50)
    print("FASHION STUDIO ETL PIPELINE")
    print("=" * 50)
    
    # 1. Tahap Ekstraksi
    print("\n🔍 Tahap 1: Ekstraksi data dari website...")
    print("Mengambil data dari https://fashion-studio.dicoding.dev")
    
    raw_products = scrape_products()
    if not raw_products:
        print("❌ Ekstraksi gagal, tidak ada data yang diambil. Pipeline dihentikan.")
        return

    print(f"✅ Ekstraksi selesai! Total produk ditemukan: {len(raw_products)}")

    # 2. Tahap Transformasi
    print("\n🔄 Tahap 2: Transformasi dan pembersihan data...")
    
    cleaned_df = transform_data(raw_products)
    if cleaned_df.empty:
        print("❌ Transformasi gagal, tidak ada data valid. Pipeline dihentikan.")
        return
        
    print(f"✅ Transformasi selesai! Data bersih: {len(cleaned_df)} baris")
    print("\nContoh data yang sudah bersih:")
    print(cleaned_df.head())
    
    print(f"\nInfo dataset:")
    print(f"- Kolom: {list(cleaned_df.columns)}")
    print(f"- Tipe data:")
    print(cleaned_df.dtypes)

    # 3. Tahap Pemuatan
    print("\n💾 Tahap 3: Memuat data ke repositori...")
    
    success_count = 0
    
    try:
        # Memuat ke CSV
        print("\n📄 Menyimpan ke CSV...")
        load_to_csv(cleaned_df, 'products.csv')
        success_count += 1
        
    except Exception as e:
        print(f"❌ Error saat menyimpan ke CSV: {e}")
    
    try:
        # Memuat ke Google Sheets
        print("\n📊 Menyimpan ke Google Sheets...")
        load_to_google_sheets(cleaned_df)
        success_count += 1
        
    except Exception as e:
        print(f"❌ Error saat menyimpan ke Google Sheets: {e}")
    
    try:
        # Memuat ke PostgreSQL
        print("\n🗄️ Menyimpan ke PostgreSQL...")
        load_to_postgresql(cleaned_df, 'products')
        success_count += 1
        
    except Exception as e:
        print(f"❌ Error saat menyimpan ke PostgreSQL: {e}")
        
    # Summary
    print("\n" + "=" * 50)
    print("📋 RINGKASAN PIPELINE ETL")
    print("=" * 50)
    print(f"✅ Data berhasil diekstrak: {len(raw_products)} produk")
    print(f"✅ Data berhasil ditransformasi: {len(cleaned_df)} produk")
    print(f"✅ Repositori berhasil disimpan: {success_count}/3")
    
    if success_count == 3:
        print("🎉 Pipeline ETL berhasil diselesaikan dengan sempurna!")
    else:
        print("⚠️ Pipeline ETL selesai dengan beberapa masalah pada tahap pemuatan.")
    
    print("=" * 50)

if __name__ == "__main__":
    main()