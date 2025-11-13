"""
Unit tests for data processing functions
"""

import unittest
import pandas as pd
import numpy as np
import os
import sys

# Add the parent directory to the path so we can import our scripts
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.data_processing import SolarDataProcessor, load_and_clean_data

class TestDataProcessing(unittest.TestCase):
    """Test cases for data processing functions"""
    
    def setUp(self):
        """Set up test data"""
        self.processor = SolarDataProcessor()
        
        # Create sample test data
        self.sample_data = pd.DataFrame({
            'Timestamp': pd.date_range('2023-01-01', periods=100, freq='H'),
            'GHI': np.random.normal(400, 100, 100),
            'DNI': np.random.normal(500, 150, 100),
            'DHI': np.random.normal(100, 50, 100),
            'Tamb': np.random.normal(25, 5, 100),
            'RH': np.random.normal(60, 20, 100),
            'WS': np.random.normal(3, 1, 100)
        })
        
        # Add some missing values and outliers for testing
        self.sample_data.loc[10:15, 'GHI'] = np.nan
        self.sample_data.loc[90, 'DNI'] = 1000  # Outlier
        
    def test_processor_initialization(self):
        """Test that processor initializes correctly"""
        self.assertIsInstance(self.processor, SolarDataProcessor)
        self.assertEqual(self.processor.cleaning_report, {})
    
    def test_handle_missing_values(self):
        """Test missing value handling"""
        df_with_missing = self.sample_data.copy()
        initial_missing = df_with_missing['GHI'].isna().sum()
        
        df_cleaned = self.processor.handle_missing_values(df_with_missing)
        
        # Check that missing values are filled
        self.assertEqual(df_cleaned['GHI'].isna().sum(), 0)
        self.assertIn('missing_values', self.processor.cleaning_report)
    
    def test_detect_outliers(self):
        """Test outlier detection"""
        outliers_report = self.processor.detect_outliers(self.sample_data)
        
        self.assertIsInstance(outliers_report, dict)
        # Should detect the outlier we added
        self.assertIn('DNI', outliers_report)
    
    def test_remove_outliers(self):
        """Test outlier removal"""
        initial_shape = self.sample_data.shape
        df_cleaned = self.processor.remove_outliers(self.sample_data)
        
        # Should remove at least one row (our outlier)
        self.assertLess(df_cleaned.shape[0], initial_shape[0])
        self.assertIn('outliers_removed', self.processor.cleaning_report)
    
    def test_process_timestamp(self):
        """Test timestamp processing"""
        df_processed = self.processor.process_timestamp(self.sample_data)
        
        # Check that new columns are created
        self.assertIn('Hour', df_processed.columns)
        self.assertIn('Month', df_processed.columns)
        self.assertIn('DayOfWeek', df_processed.columns)
        self.assertIn('Season', df_processed.columns)
        
        # Check data types
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df_processed['Timestamp']))
    
    def test_complete_cleaning_pipeline(self):
        """Test the complete cleaning pipeline"""
        # Create a test file
        test_file = 'test_sample_data.csv'
        self.sample_data.to_csv(test_file, index=False)
        
        try:
            # Test the complete pipeline
            df_cleaned = self.processor.clean_solar_data(
                test_file, 
                country_name='TestCountry'
            )
            
            # Check that data is returned
            self.assertIsNotNone(df_cleaned)
            self.assertIsInstance(df_cleaned, pd.DataFrame)
            
            # Check that cleaning report is populated
            self.assertIn('missing_values', self.processor.cleaning_report)
            self.assertIn('outliers_detected', self.processor.cleaning_report)
            self.assertIn('outliers_removed', self.processor.cleaning_report)
            
        finally:
            # Clean up
            if os.path.exists(test_file):
                os.remove(test_file)
    
    def test_load_and_clean_convenience_function(self):
        """Test the convenience function"""
        test_file = 'test_convenience.csv'
        self.sample_data.to_csv(test_file, index=False)
        
        try:
            df_cleaned = load_and_clean_data(test_file, country_name='TestConvenience')
            self.assertIsNotNone(df_cleaned)
            self.assertIsInstance(df_cleaned, pd.DataFrame)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

class TestConfiguration(unittest.TestCase):
    """Test configuration settings"""
    
    def test_country_configuration(self):
        """Test that country configuration is accessible"""
        from config.settings import COUNTRIES, get_all_countries
        
        countries = get_all_countries()
        self.assertIn('Benin', countries)
        self.assertIn('Sierra_Leone', countries)
        self.assertIn('Togo', countries)
        
        # Check that each country has required keys
        for country in countries:
            country_info = COUNTRIES[country]
            self.assertIn('file', country_info)
            self.assertIn('cleaned_file', country_info)
            self.assertIn('location', country_info)

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
