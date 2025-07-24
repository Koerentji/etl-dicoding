import pytest
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.transform import transform_data

class TestTransform:
    
    def test_transform_data_valid_input(self):
        """Test transformasi dengan data valid"""
        input_data = [
            {
                'Title': 'Test Product 1',
                'Price': '25.99',
                'Rating': '4.5',
                'Colors': '3',
                'Size': 'M',
                'Gender': 'Unisex',
                'Timestamp': '2024-01-01T00:00:00'
            },
            {
                'Title': 'Test Product 2',
                'Price': '35.50',
                'Rating': '3.8',
                'Colors': '2',
                'Size': 'L',
                'Gender': 'Male',
                'Timestamp': '2024-01-01T00:00:01'
            }
        ]
        
        result = transform_data(input_data)
        
        # Assertions
        assert len(result) == 2
        assert result['Price'].dtype == 'float64'
        assert result['Rating'].dtype == 'float64'
        assert result['Colors'].dtype == 'int64'
        
        # Check price conversion (USD to IDR)
        assert result.iloc[0]['Price'] == 25.99 * 16000
        assert result.iloc[1]['Price'] == 35.50 * 16000
        
        # Check rating conversion
        assert result.iloc[0]['Rating'] == 4.5
        assert result.iloc[1]['Rating'] == 3.8
        
        # Check colors conversion
        assert result.iloc[0]['Colors'] == 3
        assert result.iloc[1]['Colors'] == 2
    
    def test_transform_data_empty_input(self):
        """Test transformasi dengan input kosong"""
        result = transform_data([])
        
        assert result.empty
        assert isinstance(result, pd.DataFrame)
    
    def test_transform_data_unknown_product(self):
        """Test transformasi dengan produk 'Unknown Product'"""
        input_data = [
            {
                'Title': 'Unknown Product',
                'Price': '25.99',
                'Rating': '4.5',
                'Colors': '3',
                'Size': 'M',
                'Gender': 'Unisex',
                'Timestamp': '2024-01-01T00:00:00'
            },
            {
                'Title': 'Valid Product',
                'Price': '35.50',
                'Rating': '3.8',
                'Colors': '2',
                'Size': 'L',
                'Gender': 'Male',
                'Timestamp': '2024-01-01T00:00:01'
            }
        ]
        
        result = transform_data(input_data)
        
        # Should only have the valid product
        assert len(result) == 1
        assert result.iloc[0]['Title'] == 'Valid Product'
    
    def test_transform_data_invalid_price(self):
        """Test transformasi dengan harga tidak valid"""
        input_data = [
            {
                'Title': 'Test Product 1',
                'Price': 'N/A',
                'Rating': '4.5',
                'Colors': '3',
                'Size': 'M',
                'Gender': 'Unisex',
                'Timestamp': '2024-01-01T00:00:00'
            },
            {
                'Title': 'Test Product 2',
                'Price': '35.50',
                'Rating': '3.8',
                'Colors': '2',
                'Size': 'L',
                'Gender': 'Male',
                'Timestamp': '2024-01-01T00:00:01'
            }
        ]
        
        result = transform_data(input_data)
        
        # Should only have the product with valid price
        assert len(result) == 1
        assert result.iloc[0]['Title'] == 'Test Product 2'
    
    def test_transform_data_invalid_rating(self):
        """Test transformasi dengan rating tidak valid"""
        input_data = [
            {
                'Title': 'Test Product 1',
                'Price': '25.99',
                'Rating': 'Invalid',
                'Colors': '3',
                'Size': 'M',
                'Gender': 'Unisex',
                'Timestamp': '2024-01-01T00:00:00'
            },
            {
                'Title': 'Test Product 2',
                'Price': '35.50',
                'Rating': '3.8',
                'Colors': '2',
                'Size': 'L',
                'Gender': 'Male',
                'Timestamp': '2024-01-01T00:00:01'
            }
        ]
        
        result = transform_data(input_data)
        
        # Should only have the product with valid rating
        assert len(result) == 1
        assert result.iloc[0]['Title'] == 'Test Product 2'
    
    def test_transform_data_invalid_colors(self):
        """Test transformasi dengan colors tidak valid"""
        input_data = [
            {
                'Title': 'Test Product 1',
                'Price': '25.99',
                'Rating': '4.5',
                'Colors': 'N/A',
                'Size': 'M',
                'Gender': 'Unisex',
                'Timestamp': '2024-01-01T00:00:00'
            },
            {
                'Title': 'Test Product 2',
                'Price': '35.50',
                'Rating': '3.8',
                'Colors': '2',
                'Size': 'L',
                'Gender': 'Male',
                'Timestamp': '2024-01-01T00:00:01'
            }
        ]
        
        result = transform_data(input_data)
        
        # Should only have the product with valid colors
        assert len(result) == 1
        assert result.iloc[0]['Title'] == 'Test Product 2'
    
    def test_transform_data_duplicates(self):
        """Test transformasi dengan data duplikat"""
        input_data = [
            {
                'Title': 'Test Product',
                'Price': '25.99',
                'Rating': '4.5',
                'Colors': '3',
                'Size': 'M',
                'Gender': 'Unisex',
                'Timestamp': '2024-01-01T00:00:00'
            },
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
        
        result = transform_data(input_data)
        
        # Should remove duplicates
        assert len(result) == 1
    
    def test_transform_data_na_size_gender(self):
        """Test transformasi dengan Size dan Gender N/A"""
        input_data = [
            {
                'Title': 'Test Product 1',
                'Price': '25.99',
                'Rating': '4.5',
                'Colors': '3',
                'Size': 'N/A',
                'Gender': 'Unisex',
                'Timestamp': '2024-01-01T00:00:00'
            },
            {
                'Title': 'Test Product 2',
                'Price': '35.50',
                'Rating': '3.8',
                'Colors': '2',
                'Size': 'L',
                'Gender': 'N/A',
                'Timestamp': '2024-01-01T00:00:01'
            },
            {
                'Title': 'Test Product 3',
                'Price': '45.00',
                'Rating': '4.0',
                'Colors': '1',
                'Size': 'M',
                'Gender': 'Female',
                'Timestamp': '2024-01-01T00:00:02'
            }
        ]
        
        result = transform_data(input_data)
        
        # Should only have the product with valid size and gender
        assert len(result) == 1
        assert result.iloc[0]['Title'] == 'Test Product 3'
    
    def test_transform_data_exception_handling(self):
        """Test error handling saat transformasi"""
        # Test dengan data yang akan menyebabkan error
        invalid_data = "not a list"
        
        result = transform_data(invalid_data)
        
        # Should return empty DataFrame on error
        assert result.empty
        assert isinstance(result, pd.DataFrame)