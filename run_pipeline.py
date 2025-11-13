#!/usr/bin/env python3
"""
Simple runner script for the Solar Data Challenge pipeline
Easy-to-use interface for common operations
"""

import os
import sys
import argparse

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_quick_start():
    """Run the quick start pipeline"""
    print("🚀 SOLAR DATA CHALLENGE - QUICK START")
    print("=====================================")
    
    # Import after path modification
    from main import process_all_countries, run_comparative_analysis, generate_final_report
    from config.settings import FILE_SETTINGS
    
    try:
        # Process all countries
        print("\n1. 📁 Processing country data...")
        country_data = process_all_countries()
        
        # Run comparative analysis
        print("\n2. 📊 Running comparative analysis...")
        insights = run_comparative_analysis(country_data)
        
        # Generate final report
        print("\n3. 📋 Generating final report...")
        generate_final_report(insights)
        
        print("\n✅ QUICK START COMPLETED SUCCESSFULLY!")
        print(f"📂 Outputs available in: {FILE_SETTINGS['output_directory']}/")
        
    except Exception as e:
        print(f"❌ Error during quick start: {e}")
        return False
    
    return True

def run_test_suite():
    """Run the test suite"""
    print("🧪 RUNNING TEST SUITE")
    print("====================")
    
    import subprocess
    import sys
    
    try:
        # Run the tests
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 'tests/', '-v'
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def show_usage_examples():
    """Show usage examples"""
    print("💡 USAGE EXAMPLES")
    print("================")
    print("\n1. Quick start (process all data and generate report):")
    print("   python run_pipeline.py --quick-start")
    
    print("\n2. Process specific country:")
    print("   python main.py --country Benin")
    
    print("\n3. Process all countries:")
    print("   python main.py --all")
    
    print("\n4. Run tests:")
    print("   python run_pipeline.py --test")
    
    print("\n5. Use modular scripts directly:")
    print("   python -c \"from scripts.data_processing import load_and_clean_data; df = load_and_clean_data('data/benin.csv')\"")
    
    print("\n6. Run comparative analysis only:")
    print("   python main.py --analyze")

def main():
    """Main function for the runner script"""
    parser = argparse.ArgumentParser(description='Solar Data Challenge Runner')
    parser.add_argument('--quick-start', action='store_true', help='Run the complete pipeline')
    parser.add_argument('--test', action='store_true', help='Run test suite')
    parser.add_argument('--examples', action='store_true', help='Show usage examples')
    
    args = parser.parse_args()
    
    if args.quick_start:
        success = run_quick_start()
        sys.exit(0 if success else 1)
    
    elif args.test:
        success = run_test_suite()
        sys.exit(0 if success else 1)
    
    elif args.examples:
        show_usage_examples()
    
    else:
        # Show help if no arguments provided
        print("🔧 SOLAR DATA CHALLENGE RUNNER")
        print("=============================")
        print("\nAvailable commands:")
        print("  --quick-start  Run the complete pipeline")
        print("  --test         Run the test suite") 
        print("  --examples     Show usage examples")
        print("\nExample: python run_pipeline.py --quick-start")

if __name__ == "__main__":
    main()
