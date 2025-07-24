import requests
from bs4 import BeautifulSoup
import datetime

# Konstanta untuk URL dasar dan header untuk menghindari deteksi sebagai bot
BASE_URL = "https://fashion-studio.dicoding.dev/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def scrape_page(page_num):
    """
    Mengekstrak data produk dari satu halaman.
    
    Args:
        page_num (int): Nomor halaman yang akan di-scrape
        
    Returns:
        list: Daftar produk dari halaman tersebut
    """
    products = []
    url = f"{BASE_URL}?page={page_num}"
    
    try:
        # Lakukan request GET ke URL
        response = requests.get(url, headers=HEADERS, timeout=10)
        # Timbulkan error jika status code bukan 200
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Cari semua kartu produk
        products_on_page = soup.find_all('div', class_='collection-card')
        
        if not products_on_page:
            print(f"Halaman {page_num} tidak ditemukan atau tidak ada produk.")
            return products

        for product in products_on_page:
            try:
                # Ekstrak setiap detail produk dengan error handling
                title_elem = product.find('h3', class_='product-title')
                title = title_elem.text.strip() if title_elem else 'Unknown Product'
                
                price_span = product.find('span', class_='price')
                price = price_span.text.strip().replace('$', '') if price_span else 'N/A'
                
                # Ekstraksi data dengan penanganan jika elemen tidak ada
                rating_p = product.find('p', string=lambda text: text and 'Rating' in text)
                rating = rating_p.text.split('/')[0].replace('Rating:', '').strip() if rating_p else 'Invalid'
                
                colors_p = product.find('p', string=lambda text: text and 'Colors' in text)
                colors = colors_p.text.replace('Colors', '').strip() if colors_p else 'N/A'
                
                size_p = product.find('p', string=lambda text: text and 'Size:' in text)
                size = size_p.text.replace('Size:', '').strip() if size_p else 'N/A'

                gender_p = product.find('p', string=lambda text: text and 'Gender:' in text)
                gender = gender_p.text.replace('Gender:', '').strip() if gender_p else 'N/A'
                
                # Tambahkan data ke list
                products.append({
                    "Title": title,
                    "Price": price,
                    "Rating": rating,
                    "Colors": colors,
                    "Size": size,
                    "Gender": gender,
                    "Timestamp": datetime.datetime.now().isoformat()  # Fitur Advanced: Tambah timestamp
                })
                
            except Exception as e:
                print(f"Error mengekstrak produk di halaman {page_num}: {e}")
                continue
    
    except requests.exceptions.RequestException as e:
        # Fitur Advanced: Error handling untuk masalah jaringan
        print(f"Gagal mengakses halaman {page_num}: {e}")
        return []
    
    return products

def scrape_products():
    """
    Fungsi utama untuk mengekstrak data produk dari seluruh halaman.
    
    Returns:
        list: Daftar berisi dictionary dari semua produk yang berhasil di-scrape.
    """
    all_products = []
    
    # Loop dari halaman 1 hingga 50
    for page in range(1, 51):
        print(f"Scraping halaman: {page}/50...")
        
        page_products = scrape_page(page)
        
        if not page_products:
            # Jika tidak ada produk, lanjutkan ke halaman berikutnya
            continue
            
        all_products.extend(page_products)
    
    print(f"Total produk berhasil di-scrape: {len(all_products)}")
    return all_products