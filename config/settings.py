"""
Configuration settings for Solar Challenge
Centralized configuration for data processing and analysis
"""

# Data Processing Settings
DATA_SETTINGS = {
    'timestamp_column': 'Timestamp',
    'solar_columns': ['GHI', 'DNI', 'DHI', 'ModA', 'ModB'],
    'environmental_columns': ['Tamb', 'RH', 'WS', 'WSgust', 'BP'],
    'maintenance_columns': ['Cleaning', 'Precipitation'],
    'key_metrics': ['GHI', 'DNI', 'DHI', 'Tamb', 'RH', 'WS']
}

# Cleaning Settings
CLEANING_SETTINGS = {
    'z_threshold': 3,
    'missing_value_strategy': 'median',
    'columns_to_impute': ['GHI', 'DNI', 'DHI', 'Tamb', 'WS', 'RH', 'BP'],
    'outlier_columns': ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust', 'Tamb']
}

# Visualization Settings
VISUALIZATION_SETTINGS = {
    'style': 'seaborn-v0_8',
    'color_palette': 'husl',
    'figure_size': (12, 8),
    'dpi': 300,
    'time_series_metrics': ['GHI', 'Tamb', 'DNI', 'WS'],
    'distribution_metrics': ['GHI', 'Tamb', 'RH', 'WS']
}

# Analysis Settings
ANALYSIS_SETTINGS = {
    'correlation_threshold': 0.3,
    'significance_level': 0.05,
    'solar_threshold': 50,  # Minimum GHI for operational hours
    'high_potential_threshold': 400  # GHI threshold for high potential
}

# File Path Settings
FILE_SETTINGS = {
    'data_directory': 'data',
    'output_directory': 'outputs',
    'reports_directory': 'reports',
    'cleaned_suffix': '_clean'
}

# Country-specific settings
COUNTRIES = {
    'Benin': {
        'file': 'benin-malanville.csv',
        'cleaned_file': 'benin_clean.csv',
        'location': 'Malanville'
    },
    'Sierra_Leone': {
        'file': 'sierra_leone.csv',
        'cleaned_file': 'sierra_leone_clean.csv',
        'location': 'Sierra Leone'
    },
    'Togo': {
        'file': 'togo.csv',
        'cleaned_file': 'togo_clean.csv',
        'location': 'Togo'
    }
}

def get_country_filepath(country, data_dir=None):
    """
    Get filepath for a country's data
    
    Args:
        country (str): Country name
        data_dir (str): Data directory path
        
    Returns:
        tuple: (raw_filepath, cleaned_filepath)
    """
    if data_dir is None:
        data_dir = FILE_SETTINGS['data_directory']
    
    country_info = COUNTRIES.get(country)
    if not country_info:
        raise ValueError(f"Unknown country: {country}")
    
    raw_path = f"{data_dir}/{country_info['file']}"
    cleaned_path = f"{data_dir}/{country_info['cleaned_file']}"
    
    return raw_path, cleaned_path

def get_all_countries():
    """Get list of all available countries"""
    return list(COUNTRIES.keys())

def validate_settings():
    """Validate all configuration settings"""
    required_dirs = [
        FILE_SETTINGS['data_directory'],
        FILE_SETTINGS['output_directory'],
        FILE_SETTINGS['reports_directory']
    ]
    
    print("✅ Configuration settings validated")
    return True

if __name__ == "__main__":
    print("🧪 Testing configuration...")
    validate_settings()
    print("✅ Configuration module loaded successfully!")
    print(f"Available countries: {', '.join(get_all_countries())}")
