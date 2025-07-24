import pandas as pd
import os
from google.oauth2.service_account import Credentials
import gspread
import psycopg2
from psycopg2.extras import execute_values
import json

def load_to_csv(dataframe, filename):
    """
    Menyimpan DataFrame ke file CSV.
    
    Args:
        dataframe (pd.DataFrame): Data yang akan disimpan
        filename (str): Nama file CSV
    """
    try:
        dataframe.to_csv(filename, index=False)
        print(f"Data berhasil disimpan ke {filename}")
        print(f"Total baris yang disimpan: {len(dataframe)}")
    except FileNotFoundError as e:
        print(f"Error: File tidak dapat dibuat - {e}")
    except Exception as e:
        print(f"Error saat menyimpan ke CSV: {e}")

def load_to_google_sheets(dataframe):
    """
    Menyimpan DataFrame ke Google Sheets.
    
    Args:
        dataframe (pd.DataFrame): Data yang akan disimpan
    """
    try:
        # Path ke file kredensial Google Sheets API
        credentials_path = 'google-sheets-api.json'
        
        if not os.path.exists(credentials_path):
            print(f"File kredensial {credentials_path} tidak ditemukan.")
            print("Silakan buat service account di Google Cloud Console dan download kredensialnya.")
            return
        
        # Setup kredensial dan akses Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        
        credentials = Credentials.from_service_account_file(credentials_path, scopes=scope)
        gc = gspread.authorize(credentials)
        
        # Buka atau buat spreadsheet
        try:
            # Coba buka spreadsheet yang sudah ada
            spreadsheet = gc.open("Fashion Studio ETL Data")
        except gspread.SpreadsheetNotFound:
            # Jika tidak ada, buat spreadsheet baru
            spreadsheet = gc.create("Fashion Studio ETL Data")
            # Bagikan dengan akses edit untuk siapa saja dengan link
            spreadsheet.share('', perm_type='anyone', role='writer')
        
        # Pilih worksheet pertama
        worksheet = spreadsheet.sheet1
        
        # Hapus data lama dan tulis data baru
        worksheet.clear()
        
        # Tulis header
        headers = dataframe.columns.tolist()
        worksheet.append_row(headers)
        
        # Tulis data
        data_rows = dataframe.values.tolist()
        for row in data_rows:
            # Konversi semua nilai ke string untuk menghindari error
            str_row = [str(cell) for cell in row]
            worksheet.append_row(str_row)
        
        print(f"Data berhasil disimpan ke Google Sheets: {spreadsheet.url}")
        print(f"Total baris yang disimpan: {len(dataframe)}")
        
    except FileNotFoundError as e:
        print(f"Error: File kredensial tidak ditemukan - {e}")
    except Exception as e:
        print(f"Error saat menyimpan ke Google Sheets: {e}")

def load_to_postgresql(dataframe, table_name):
    """
    Menyimpan DataFrame ke database PostgreSQL.
    
    Args:
        dataframe (pd.DataFrame): Data yang akan disimpan
        table_name (str): Nama tabel di database
    """
    try:
        # Konfigurasi koneksi PostgreSQL
        # Dalam implementasi nyata, gunakan environment variables untuk keamanan
        db_config = {
            'host': 'localhost',
            'database': 'fashion_studio',
            'user': 'postgres',
            'password': 'password',
            'port': '5432'
        }
        
        # Koneksi ke database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Buat tabel jika belum ada
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            price FLOAT,
            rating FLOAT,
            colors INTEGER,
            size VARCHAR(50),
            gender VARCHAR(20),
            timestamp VARCHAR(50)
        );
        """
        cursor.execute(create_table_query)
        
        # Hapus data lama
        cursor.execute(f"DELETE FROM {table_name}")
        
        # Insert data baru
        columns = ['title', 'price', 'rating', 'colors', 'size', 'gender', 'timestamp']
        values = [tuple(row) for row in dataframe[['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp']].values]
        
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s"
        execute_values(cursor, insert_query, values)
        
        # Commit perubahan
        conn.commit()
        
        print(f"Data berhasil disimpan ke PostgreSQL tabel '{table_name}'")
        print(f"Total baris yang disimpan: {len(dataframe)}")
        
        # Tutup koneksi
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"Error koneksi PostgreSQL: {e}")
        print("Pastikan PostgreSQL berjalan dan konfigurasi koneksi benar.")
    except Exception as e:
        print(f"Error saat menyimpan ke PostgreSQL: {e}")