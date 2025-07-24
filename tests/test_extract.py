import pytest
from unittest.mock import Mock, patch
import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.extract import scrape_page, scrape_products

class TestExtract:
    
    @patch('utils.extract.requests.get')
    def test_scrape_page_success(self, mock_get):
        """Test scraping halaman dengan data valid"""
        # Mock response HTML dengan produk valid
        mock_html = '''
        <html>
            <div class="collection-card">
                <h3 class="product-title">Test Product</h3>
                <span class="price">$25.99</span>
                <p>Rating: 4.5 / 5</p>
                <p>Colors 3</p>
                <p>Size: M</p>
                <p>Gender: Unisex</p>
            </div>
        </html>
        '''
        
        mock_response = Mock()
        mock_response.text = mock_html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test function
        result = scrape_page(1)
        
        # Assertions
        assert len(result) == 1
        assert result[0]['Title'] == 'Test Product'
        assert result[0]['Price'] == '25.99'
        assert result[0]['Rating'] == '4.5'
        assert result[0]['Colors'] == '3'
        assert result[0]['Size'] == 'M'
        assert result[0]['Gender'] == 'Unisex'
        assert 'Timestamp' in result[0]
    
    @patch('utils.extract.requests.get')
    def test_scrape_page_no_products(self, mock_get):
        """Test scraping halaman tanpa produk"""
        mock_html = '<html><body>No products found</body></html>'
        
        mock_response = Mock()
        mock_response.text = mock_html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = scrape_page(1)
        
        assert result == []
    
    @patch('utils.extract.requests.get')
    def test_scrape_page_missing_elements(self, mock_get):
        """Test scraping halaman dengan elemen yang hilang"""
        mock_html = '''
        <html>
            <div class="collection-card">
                <h3 class="product-title">Incomplete Product</h3>
                <!-- Missing price, rating, etc. -->
            </div>
        </html>
        '''
        
        mock_response = Mock()
        mock_response.text = mock_html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = scrape_page(1)
        
        assert len(result) == 1
        assert result[0]['Title'] == 'Incomplete Product'
        assert result[0]['Price'] == 'N/A'
        assert result[0]['Rating'] == 'Invalid'
        assert result[0]['Colors'] == 'N/A'
    
    @patch('utils.extract.requests.get')
    def test_scrape_page_request_exception(self, mock_get):
        """Test error koneksi saat scraping"""
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")
        
        result = scrape_page(1)
        
        assert result == []
    
    @patch('utils.extract.requests.get')
    def test_scrape_page_timeout(self, mock_get):
        """Test timeout saat scraping"""
        mock_get.side_effect = requests.exceptions.Timeout("Request timeout")
        
        result = scrape_page(1)
        
        assert result == []
    
    @patch('utils.extract.scrape_page')
    def test_scrape_products_success(self, mock_scrape_page):
        """Test scraping semua produk dengan sukses"""
        # Mock scrape_page untuk mengembalikan data dummy
        mock_scrape_page.return_value = [
            {
                'Title': 'Test Product',
                'Price': '25.99',
                'Rating': '4.5',
                'Colors': '3',
                'Size': 'M',
                'Gender': 'Unisex',
                'Timestamp': '2024-01-01T00:00:00'
            }
        ]
        
        # Test hanya 3 halaman untuk testing
        with patch('utils.extract.range', return_value=range(1, 4)):
            result = scrape_products()
        
        assert len(result) == 3  # 3 halaman × 1 produk per halaman
        assert all('Title' in product for product in result)
    
    @patch('utils.extract.scrape_page')
    def test_scrape_products_empty_pages(self, mock_scrape_page):
        """Test scraping dengan halaman kosong"""
        mock_scrape_page.return_value = []
        
        with patch('utils.extract.range', return_value=range(1, 4)):
            result = scrape_products()
        
        assert result == []