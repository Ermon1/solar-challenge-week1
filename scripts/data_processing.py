"""
Data Processing Pipeline for Solar Challenge
Modular functions for cleaning and processing solar data
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class SolarDataProcessor:
    """Main class for processing solar data"""
    
    def __init__(self):
        self.cleaning_report = {}
    
    def load_data(self, filepath, country_name=None):
        """
        Load solar data from CSV file
        
        Args:
            filepath (str): Path to CSV file
            country_name (str): Optional country name for reporting
            
        Returns:
            pandas.DataFrame: Loaded solar data
        """
        try:
            df = pd.read_csv(filepath)
            if country_name:
                print(f"✅ Loaded {country_name} data: {df.shape}")
            else:
                print(f"✅ Loaded data: {df.shape}")
            return df
        except Exception as e:
            print(f"❌ Error loading {filepath}: {e}")
            return None
    
    def handle_missing_values(self, df, columns_to_impute=None):
        """
        Handle missing values in solar dataset
        
        Args:
            df (DataFrame): Input data
            columns_to_impute (list): Columns to impute
            
        Returns:
            DataFrame: Data with missing values handled
        """
        if columns_to_impute is None:
            columns_to_impute = ['GHI', 'DNI', 'DHI', 'Tamb', 'WS', 'RH', 'BP']
        
        missing_report = {}
        for col in columns_to_impute:
            if col in df.columns:
                missing_count = df[col].isna().sum()
                if missing_count > 0:
                    df[col].fillna(df[col].median(), inplace=True)
                    missing_report[col] = missing_count
                    print(f"✅ Imputed {missing_count} missing values in {col}")
        
        self.cleaning_report['missing_values'] = missing_report
        return df
    
    def detect_outliers(self, df, columns=None, z_threshold=3):
        """
        Detect outliers using Z-score method
        
        Args:
            df (DataFrame): Input data
            columns (list): Columns to check for outliers
            z_threshold (float): Z-score threshold
            
        Returns:
            dict: Outlier report
        """
        if columns is None:
            columns = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust', 'Tamb']
        
        outliers_report = {}
        for col in columns:
            if col in df.columns and df[col].dtype in ['float64', 'int64']:
                z_scores = np.abs(stats.zscore(df[col].dropna()))
                outlier_count = np.sum(z_scores > z_threshold)
                outliers_report[col] = outlier_count
                if outlier_count > 0:
                    print(f"📊 {col}: {outlier_count} outliers ({outlier_count/len(df)*100:.2f}%)")
        
        return outliers_report
    
    def remove_outliers(self, df, columns=None, z_threshold=3):
        """
        Remove outliers using Z-score method
        
        Args:
            df (DataFrame): Input data
            columns (list): Columns to check for outliers
            z_threshold (float): Z-score threshold
            
        Returns:
            DataFrame: Data with outliers removed
        """
        initial_shape = df.shape
        
        if columns is None:
            columns = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust', 'Tamb']
        
        for col in columns:
            if col in df.columns:
                z_scores = np.abs(stats.zscore(df[col].dropna()))
                outlier_mask = z_scores > z_threshold
                if outlier_mask.any():
                    df = df[~outlier_mask]
        
        removed_count = initial_shape[0] - df.shape[0]
        print(f"✅ Removed {removed_count} outlier rows")
        self.cleaning_report['outliers_removed'] = removed_count
        
        return df
    
    def process_timestamp(self, df, timestamp_col='Timestamp'):
        """
        Process timestamp and extract temporal features
        
        Args:
            df (DataFrame): Input data
            timestamp_col (str): Timestamp column name
            
        Returns:
            DataFrame: Data with temporal features
        """
        if timestamp_col in df.columns:
            df[timestamp_col] = pd.to_datetime(df[timestamp_col])
            df['Hour'] = df[timestamp_col].dt.hour
            df['Month'] = df[timestamp_col].dt.month
            df['DayOfWeek'] = df[timestamp_col].dt.dayofweek
            df['Season'] = (df[timestamp_col].dt.month % 12 + 3) // 3
            print("✅ Processed timestamp and extracted temporal features")
        
        return df
    
    def get_cleaning_summary(self):
        """Get summary of cleaning operations"""
        return self.cleaning_report
    
    def clean_solar_data(self, filepath, export_path=None, country_name=None):
        """
        Complete data cleaning pipeline for solar data
        
        Args:
            filepath (str): Path to raw data CSV
            export_path (str): Path to save cleaned data
            country_name (str): Country name for reporting
            
        Returns:
            DataFrame: Cleaned solar data
        """
        print(f"\n{'='*50}")
        print(f"�� Processing {country_name if country_name else 'solar'} data...")
        print(f"{'='*50}")
        
        # Load data
        df = self.load_data(filepath, country_name)
        if df is None:
            return None
        
        initial_shape = df.shape
        
        # Handle missing values
        df = self.handle_missing_values(df)
        
        # Detect outliers
        outliers_report = self.detect_outliers(df)
        self.cleaning_report['outliers_detected'] = outliers_report
        
        # Remove outliers
        df = self.remove_outliers(df)
        
        # Process timestamp
        df = self.process_timestamp(df)
        
        # Export if path provided
        if export_path:
            df.to_csv(export_path, index=False)
            print(f"💾 Cleaned data exported to: {export_path}")
        
        # Final report
        print(f"\n📊 CLEANING SUMMARY for {country_name}:")
        print(f"   • Initial records: {initial_shape[0]}")
        print(f"   • Final records: {df.shape[0]}")
        print(f"   • Records removed: {initial_shape[0] - df.shape[0]}")
        print(f"   • Columns processed: {df.shape[1]}")
        
        return df

# Convenience functions
def load_and_clean_data(filepath, export_path=None, country_name=None):
    """
    Convenience function for one-line data loading and cleaning
    """
    processor = SolarDataProcessor()
    return processor.clean_solar_data(filepath, export_path, country_name)

def batch_process_countries(data_dir, output_dir):
    """
    Process all country data files in a directory
    
    Args:
        data_dir (str): Directory containing raw data files
        output_dir (str): Directory for cleaned outputs
    """
    import os
    
    country_files = {
        'Benin': 'benin-malanville.csv',
        'Sierra_Leone': 'sierra_leone.csv', 
        'Togo': 'togo.csv'
    }
    
    results = {}
    for country, filename in country_files.items():
        input_path = os.path.join(data_dir, filename)
        output_path = os.path.join(output_dir, f"{country.lower()}_clean.csv")
        
        if os.path.exists(input_path):
            print(f"\n🎯 Processing {country}...")
            df = load_and_clean_data(input_path, output_path, country)
            results[country] = df
        else:
            print(f"❌ File not found: {input_path}")
    
    return results

if __name__ == "__main__":
    # Test the module
    print("🧪 Testing data_processing module...")
    processor = SolarDataProcessor()
    print("✅ data_processing module loaded successfully!")
