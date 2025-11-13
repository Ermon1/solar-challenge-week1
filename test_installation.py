#!/usr/bin/env python3
"""
Quick test to verify the installation and imports work correctly
"""

import sys
import os

print("🧪 Testing Solar Challenge Installation...")
print("=" * 40)

try:
    # Test basic imports
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    print("✅ Basic imports successful")
    
    # Test our custom modules
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    from scripts.data_processing import SolarDataProcessor
    from scripts.visualization import SolarVisualizer
    from scripts.analysis import SolarAnalyzer
    from config.settings import validate_settings, get_all_countries
    print("✅ Custom module imports successful")
    
    # Test configuration
    validate_settings()
    countries = get_all_countries()
    print(f"✅ Configuration loaded - Countries: {', '.join(countries)}")
    
    # Test class instantiation
    processor = SolarDataProcessor()
    visualizer = SolarVisualizer()
    analyzer = SolarAnalyzer()
    print("✅ Class instantiation successful")
    
    print("\n🎉 ALL TESTS PASSED! Your environment is ready.")
    print("\nNext steps:")
    print("1. Run: python run_pipeline.py --quick-start")
    print("2. Or: python main.py --all")
    print("3. Run tests: python run_pipeline.py --test")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    sys.exit(1)
