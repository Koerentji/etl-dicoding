import pytest
import pandas as pd
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.load import load_to_csv, load_to_google_sheets, load_to_postgresql

class TestLoad:
    
    def setup_method(self):
        """Setup test data"""
        self.test_df = pd.DataFrame({
            'Title': ['Product 1', 'Product 2'],
            'Price': [100000.0, 200000.0],
            'Rating': [4.5, 3.8],
            'Colors': [3, 2],
            'Size': ['M', 'L'],
            'Gender': ['Unisex', 'Male'],
            'Timestamp': ['2024-01-01T00:00:00', '2024-01-01T00:00:01']
        })
    
    def test_load_to_csv_success(self):
        """Test menyimpan ke CSV dengan sukses"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp_file:
            temp_filename = tmp_file.name
        
        try:
            load_to_csv(self.test_df, temp_filename)
            
            # Verify file exists and has correct content
            assert os.path.exists(temp_filename)
            
            # Read back and verify
            loaded_df = pd.read_csv(temp_filename)
            assert len(loaded_df) == 2
            assert list(loaded_df.columns) == list(self.test_df.columns)
            
        finally:
            # Cleanup
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_load_to_csv_file_error(self):
        """Test error saat menyimpan ke CSV"""
        # Test dengan path yang tidak valid
        invalid_path = "/invalid/path/test.csv"
        
        # Should not raise exception, but print error message
        load_to_csv(self.test_df, invalid_path)
    
    @patch('utils.load.gspread.authorize')
    @patch('utils.load.Credentials.from_service_account_file')
    @patch('utils.load.os.path.exists')
    def test_load_to_google_sheets_success(self, mock_exists, mock_credentials, mock_authorize):
        """Test menyimpan ke Google Sheets dengan sukses"""
        # Setup mocks
        mock_exists.return_value = True
        mock_gc = Mock()
        mock_authorize.return_value = mock_gc
        
        mock_spreadsheet = Mock()
        mock_spreadsheet.url = "https://docs.google.com/spreadsheets/test"
        mock_worksheet = Mock()
        mock_spreadsheet.sheet1 = mock_worksheet
        
        mock_gc.open.return_value = mock_spreadsheet
        
        # Test function
        load_to_google_sheets(self.test_df)
        
        # Verify calls
        mock_worksheet.clear.assert_called_once()
        mock_worksheet.append_row.assert_called()
    
    @patch('utils.load.os.path.exists')
    def test_load_to_google_sheets_no_credentials(self, mock_exists):
        """Test Google Sheets tanpa file kredensial"""
        mock_exists.return_value = False
        
        # Should not raise exception, but print error message
        load_to_google_sheets(self.test_df)
    
    @patch('utils.load.gspread.authorize')
    @patch('utils.load.Credentials.from_service_account_file')
    @patch('utils.load.os.path.exists')
    def test_load_to_google_sheets_create_new(self, mock_exists, mock_credentials, mock_authorize):
        """Test membuat Google Sheets baru jika tidak ada"""
        # Setup mocks
        mock_exists.return_value = True
        mock_gc = Mock()
        mock_authorize.return_value = mock_gc
        
        # Mock spreadsheet not found, then create new
        mock_gc.open.side_effect = Exception("SpreadsheetNotFound")
        
        mock_new_spreadsheet = Mock()
        mock_new_spreadsheet.url = "https://docs.google.com/spreadsheets/new"
        mock_worksheet = Mock()
        mock_new_spreadsheet.sheet1 = mock_worksheet
        mock_gc.create.return_value = mock_new_spreadsheet
        
        # Test function
        load_to_google_sheets(self.test_df)
        
        # Verify new spreadsheet was created
        mock_gc.create.assert_called_once_with("Fashion Studio ETL Data")
        mock_new_spreadsheet.share.assert_called_once()
    
    @patch('utils.load.psycopg2.connect')
    def test_load_to_postgresql_success(self, mock_connect):
        """Test menyimpan ke PostgreSQL dengan sukses"""
        # Setup mocks
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        # Test function
        load_to_postgresql(self.test_df, 'test_table')
        
        # Verify calls
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
    
    @patch('utils.load.psycopg2.connect')
    def test_load_to_postgresql_connection_error(self, mock_connect):
        """Test error koneksi PostgreSQL"""
        # Mock connection error
        mock_connect.side_effect = Exception("Connection failed")
        
        # Should not raise exception, but print error message
        load_to_postgresql(self.test_df, 'test_table')
    
    @patch('utils.load.psycopg2.connect')
    def test_load_to_postgresql_table_creation(self, mock_connect):
        """Test pembuatan tabel PostgreSQL"""
        # Setup mocks
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        # Test function
        load_to_postgresql(self.test_df, 'products')
        
        # Verify table creation query was executed
        create_table_calls = [call for call in mock_cursor.execute.call_args_list 
                            if 'CREATE TABLE IF NOT EXISTS' in str(call)]
        assert len(create_table_calls) > 0
    
    def test_empty_dataframe_handling(self):
        """Test handling DataFrame kosong"""
        empty_df = pd.DataFrame()
        
        # Test with temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp_file:
            temp_filename = tmp_file.name
        
        try:
            load_to_csv(empty_df, temp_filename)
            
            # File should still be created
            assert os.path.exists(temp_filename)
            
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)