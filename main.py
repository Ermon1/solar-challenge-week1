#!/usr/bin/env python3
"""
Main execution script for Solar Data Challenge
Orchestrates the complete data processing and analysis pipeline
"""

import os
import sys
import argparse
from datetime import datetime

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scripts.data_processing import batch_process_countries, load_and_clean_data
from scripts.visualization import create_analysis_report
from scripts.analysis import analyze_solar_data, SolarAnalyzer
from config.settings import COUNTRIES, FILE_SETTINGS, validate_settings

def setup_directories():
    """Create necessary directories"""
    directories = [
        FILE_SETTINGS['data_directory'],
        FILE_SETTINGS['output_directory'], 
        FILE_SETTINGS['reports_directory']
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def process_individual_country(country, data_dir=None):
    """
    Process data for a single country
    
    Args:
        country (str): Country name
        data_dir (str): Data directory path
    """
    if data_dir is None:
        data_dir = FILE_SETTINGS['data_directory']
    
    country_info = COUNTRIES.get(country)
    if not country_info:
        print(f"❌ Unknown country: {country}")
        return None
    
    input_file = os.path.join(data_dir, country_info['file'])
    output_file = os.path.join(data_dir, country_info['cleaned_file'])
    
    if not os.path.exists(input_file):
        print(f"❌ Input file not found: {input_file}")
        return None
    
    print(f"\n{'='*50}")
    print(f"🚀 PROCESSING {country.upper()}")
    print(f"{'='*50}")
    
    # Load and clean data
    df_cleaned = load_and_clean_data(input_file, output_file, country)
    
    if df_cleaned is not None:
        # Create analysis report
        create_analysis_report(df_cleaned, country, FILE_SETTINGS['reports_directory'])
        print(f"✅ Successfully processed {country}")
        return df_cleaned
    else:
        print(f"❌ Failed to process {country}")
        return None

def process_all_countries(data_dir=None):
    """
    Process data for all countries
    
    Args:
        data_dir (str): Data directory path
    """
    if data_dir is None:
        data_dir = FILE_SETTINGS['data_directory']
    
    print("\n" + "="*60)
    print("🌍 BATCH PROCESSING ALL COUNTRIES")
    print("="*60)
    
    country_data = {}
    
    for country in COUNTRIES.keys():
        df = process_individual_country(country, data_dir)
        if df is not None:
            country_data[country] = df
    
    return country_data

def run_comparative_analysis(country_data):
    """
    Run comparative analysis across countries
    
    Args:
        country_data (dict): Dictionary of {country: dataframe}
    """
    if len(country_data) < 2:
        print("❌ Need data from at least 2 countries for comparison")
        return
    
    print("\n" + "="*60)
    print("📊 RUNNING COMPARATIVE ANALYSIS")
    print("="*60)
    
    analyzer = SolarAnalyzer()
    insights = analyzer.generate_insights_report(country_data)
    
    return insights

def generate_final_report(insights, output_dir=None):
    """
    Generate final analysis report
    
    Args:
        insights (dict): Analysis insights
        output_dir (str): Output directory
    """
    if output_dir is None:
        output_dir = FILE_SETTINGS['output_directory']
    
    report_file = os.path.join(output_dir, f"final_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    
    with open(report_file, 'w') as f:
        f.write("SOLAR DATA CHALLENGE - FINAL ANALYSIS REPORT\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        if insights and 'top_country' in insights:
            f.write("PRIMARY RECOMMENDATION:\n")
            f.write(f"• Recommended Country: {insights['top_country']}\n")
            f.write(f"• Statistical Significance: {insights['statistical_significance']}\n\n")
            
            f.write("COUNTRY RANKINGS:\n")
            for i, (country, scores) in enumerate(insights['rankings'].items(), 1):
                f.write(f"{i}. {country} (Score: {scores['composite_score']:.2f})\n")
                f.write(f"   - Average GHI: {scores['average_ghi']:.2f} W/m²\n")
                f.write(f"   - Consistency: {scores['consistency']:.2f}%\n")
                f.write(f"   - High Potential Hours: {scores['high_potential_hours']}\n\n")
        
        f.write("METHODOLOGY:\n")
        f.write("• Data cleaning: Missing value imputation, outlier removal\n")
        f.write("• Statistical testing: ANOVA, Kruskal-Wallis\n")
        f.write("• Ranking: Composite scoring (GHI, consistency, operational hours)\n")
    
    print(f"💾 Final report saved: {report_file}")

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Solar Data Challenge Pipeline')
    parser.add_argument('--country', type=str, help='Process specific country')
    parser.add_argument('--all', action='store_true', help='Process all countries')
    parser.add_argument('--data-dir', type=str, default='data', help='Data directory')
    parser.add_argument('--analyze', action='store_true', help='Run comparative analysis')
    
    args = parser.parse_args()
    
    print("🔧 SOLAR DATA CHALLENGE PIPELINE")
    print("�� ============================")
    
    # Setup
    setup_directories()
    validate_settings()
    
    # Process data
    country_data = {}
    
    if args.country:
        # Process specific country
        df = process_individual_country(args.country, args.data_dir)
        if df is not None:
            country_data[args.country] = df
    
    elif args.all or (not args.country and not args.analyze):
        # Process all countries
        country_data = process_all_countries(args.data_dir)
    
    # Run analysis if requested or if we have data
    if args.analyze or country_data:
        insights = run_comparative_analysis(country_data)
        if insights:
            generate_final_report(insights)
    
    print("\n🎉 PIPELINE EXECUTION COMPLETED!")
    print("📁 Check the following directories for outputs:")
    print(f"   • Data: {FILE_SETTINGS['data_directory']}/")
    print(f"   • Reports: {FILE_SETTINGS['reports_directory']}/")
    print(f"   • Outputs: {FILE_SETTINGS['output_directory']}/")

if __name__ == "__main__":
    main()
