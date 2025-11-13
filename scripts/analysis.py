"""
Statistical Analysis Functions for Solar Challenge
Modular functions for statistical testing and insights
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import f_oneway, kruskal
import warnings
warnings.filterwarnings('ignore')

class SolarAnalyzer:
    """Class for statistical analysis of solar data"""
    
    def __init__(self):
        self.analysis_results = {}
    
    def calculate_summary_statistics(self, df, country_name=None):
        """
        Calculate comprehensive summary statistics
        
        Args:
            df (DataFrame): Input data
            country_name (str): Country name for reporting
            
        Returns:
            dict: Summary statistics
        """
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        summary = {
            'count': df[numeric_columns].count(),
            'mean': df[numeric_columns].mean(),
            'median': df[numeric_columns].median(),
            'std': df[numeric_columns].std(),
            'min': df[numeric_columns].min(),
            'max': df[numeric_columns].max(),
            'q25': df[numeric_columns].quantile(0.25),
            'q75': df[numeric_columns].quantile(0.75)
        }
        
        if country_name:
            print(f"�� Summary statistics for {country_name}:")
            print(f"   • Records: {len(df)}")
            print(f"   • Average GHI: {df['GHI'].mean():.2f} ± {df['GHI'].std():.2f} W/m²")
            print(f"   • Average Temperature: {df['Tamb'].mean():.2f} °C")
            if 'RH' in df.columns:
                print(f"   • Average Humidity: {df['RH'].mean():.2f} %")
        
        return summary
    
    def analyze_correlations(self, df, target_column='GHI', threshold=0.3):
        """
        Analyze correlations with target variable
        
        Args:
            df (DataFrame): Input data
            target_column (str): Target variable for correlation
            threshold (float): Minimum correlation to report
            
        Returns:
            dict: Significant correlations
        """
        if target_column not in df.columns:
            print(f"❌ Target column {target_column} not found")
            return {}
        
        numeric_df = df.select_dtypes(include=[np.number])
        correlations = numeric_df.corr()[target_column].sort_values(ascending=False)
        
        significant_correlations = {}
        for col, corr in correlations.items():
            if col != target_column and abs(corr) >= threshold:
                significant_correlations[col] = corr
        
        print(f"🔗 Significant correlations with {target_column} (|r| ≥ {threshold}):")
        for col, corr in significant_correlations.items():
            direction = "positive" if corr > 0 else "negative"
            print(f"   • {col}: {corr:.3f} ({direction})")
        
        return significant_correlations
    
    def compare_countries_statistical(self, country_data_dict, metric='GHI'):
        """
        Perform statistical comparison between countries
        
        Args:
            country_data_dict (dict): {country_name: dataframe}
            metric (str): Metric to compare
            
        Returns:
            dict: Statistical test results
        """
        # Prepare data for testing
        country_samples = {}
        for country, df in country_data_dict.items():
            if metric in df.columns:
                country_samples[country] = df[metric].dropna()
        
        if len(country_samples) < 2:
            print("❌ Need at least 2 countries for comparison")
            return {}
        
        # One-way ANOVA
        anova_result = f_oneway(*country_samples.values())
        
        # Kruskal-Wallis (non-parametric alternative)
        kruskal_result = kruskal(*country_samples.values())
        
        results = {
            'countries': list(country_samples.keys()),
            'sample_sizes': {country: len(sample) for country, sample in country_samples.items()},
            'anova': {
                'f_statistic': anova_result.statistic,
                'p_value': anova_result.pvalue,
                'significant': anova_result.pvalue < 0.05
            },
            'kruskal_wallis': {
                'h_statistic': kruskal_result.statistic,
                'p_value': kruskal_result.pvalue,
                'significant': kruskal_result.pvalue < 0.05
            }
        }
        
        print(f"📈 Statistical Comparison for {metric}:")
        print(f"   • Countries: {', '.join(results['countries'])}")
        print(f"   • ANOVA F-statistic: {results['anova']['f_statistic']:.4f}")
        print(f"   • ANOVA p-value: {results['anova']['p_value']:.4f}")
        print(f"   • Kruskal-Wallis H-statistic: {results['kruskal_wallis']['h_statistic']:.4f}")
        print(f"   • Kruskal-Wallis p-value: {results['kruskal_wallis']['p_value']:.4f}")
        
        if results['anova']['significant']:
            print("   • ✅ Statistically significant differences found (p < 0.05)")
        else:
            print("   • ❌ No statistically significant differences (p ≥ 0.05)")
        
        return results
    
    def calculate_solar_potential_metrics(self, df, country_name=None):
        """
        Calculate solar potential specific metrics
        
        Args:
            df (DataFrame): Input data
            country_name (str): Country name for reporting
            
        Returns:
            dict: Solar potential metrics
        """
        if 'GHI' not in df.columns:
            print("❌ GHI data required for solar potential analysis")
            return {}
        
        ghi_data = df['GHI'].dropna()
        
        metrics = {
            'average_ghi': ghi_data.mean(),
            'std_ghi': ghi_data.std(),
            'cv_ghi': (ghi_data.std() / ghi_data.mean()) * 100,  # Coefficient of variation
            'peak_ghi': ghi_data.max(),
            'peak_95th': ghi_data.quantile(0.95),
            'consistency_score': 100 - (ghi_data.std() / ghi_data.mean()) * 100,
            'operational_hours': len(ghi_data[ghi_data > 50]),  # Hours with meaningful solar
            'high_potential_hours': len(ghi_data[ghi_data > 400])  # Hours with high solar
        }
        
        if country_name:
            print(f"☀️ Solar Potential Metrics for {country_name}:")
            print(f"   • Average GHI: {metrics['average_ghi']:.2f} W/m²")
            print(f"   • Peak GHI (95th %): {metrics['peak_95th']:.2f} W/m²")
            print(f"   • Consistency (CV): {metrics['cv_ghi']:.2f}%")
            print(f"   • High Potential Hours: {metrics['high_potential_hours']}")
        
        return metrics
    
    def rank_countries(self, country_data_dict):
        """
        Rank countries based on multiple solar potential factors
        
        Args:
            country_data_dict (dict): {country_name: dataframe}
            
        Returns:
            dict: Country rankings and scores
        """
        rankings = {}
        
        for country, df in country_data_dict.items():
            metrics = self.calculate_solar_potential_metrics(df, country_name=None)
            
            if metrics:
                # Composite score (weighted)
                composite_score = (
                    metrics['average_ghi'] * 0.4 +          # GHI most important
                    (100 - metrics['cv_ghi']) * 0.3 +       # Consistency important
                    metrics['high_potential_hours'] * 0.2 + # Operational hours
                    metrics['peak_95th'] * 0.1              # Peak performance
                )
                
                rankings[country] = {
                    'composite_score': composite_score,
                    'average_ghi': metrics['average_ghi'],
                    'consistency': 100 - metrics['cv_ghi'],
                    'high_potential_hours': metrics['high_potential_hours'],
                    'metrics': metrics
                }
        
        # Sort by composite score
        sorted_rankings = dict(sorted(rankings.items(), 
                                    key=lambda x: x[1]['composite_score'], 
                                    reverse=True))
        
        print("🏆 Country Rankings by Solar Potential:")
        for i, (country, scores) in enumerate(sorted_rankings.items(), 1):
            print(f"   {i}. {country}:")
            print(f"      • Composite Score: {scores['composite_score']:.2f}")
            print(f"      • Average GHI: {scores['average_ghi']:.2f} W/m²")
            print(f"      • Consistency: {scores['consistency']:.2f}%")
            print(f"      • High Potential Hours: {scores['high_potential_hours']}")
        
        return sorted_rankings
    
    def generate_insights_report(self, country_data_dict):
        """
        Generate comprehensive insights report
        
        Args:
            country_data_dict (dict): {country_name: dataframe}
            
        Returns:
            dict: Comprehensive insights
        """
        print("\n" + "="*60)
        print("📋 COMPREHENSIVE SOLAR ANALYSIS INSIGHTS")
        print("="*60)
        
        # Calculate metrics for each country
        country_metrics = {}
        for country, df in country_data_dict.items():
            country_metrics[country] = self.calculate_solar_potential_metrics(df)
        
        # Statistical comparison
        statistical_results = self.compare_countries_statistical(country_data_dict, 'GHI')
        
        # Rankings
        rankings = self.rank_countries(country_data_dict)
        
        # Generate insights
        insights = {
            'top_country': list(rankings.keys())[0] if rankings else None,
            'statistical_significance': statistical_results.get('anova', {}).get('significant', False),
            'country_metrics': country_metrics,
            'rankings': rankings,
            'statistical_tests': statistical_results
        }
        
        # Print key insights
        if insights['top_country']:
            print(f"\n🎯 PRIMARY RECOMMENDATION: {insights['top_country']}")
            top_metrics = insights['rankings'][insights['top_country']]
            print(f"   • Best composite solar potential score")
            print(f"   • Average GHI: {top_metrics['average_ghi']:.2f} W/m²")
            print(f"   • High consistency: {top_metrics['consistency']:.2f}%")
        
        if insights['statistical_significance']:
            print(f"\n📊 STATISTICAL FINDINGS:")
            print(f"   • Significant differences confirmed (p < 0.05)")
            print(f"   • Ranking is statistically supported")
        else:
            print(f"\n📊 STATISTICAL FINDINGS:")
            print(f"   • Differences not statistically significant")
            print(f"   • Consider other factors for final decision")
        
        print(f"\n💡 STRATEGIC RECOMMENDATIONS:")
        print(f"   • Focus on {insights['top_country']} for primary investment")
        print(f"   • Consider secondary options based on local factors")
        print(f"   • Monitor environmental conditions for optimal performance")
        
        return insights

# Convenience function
def analyze_solar_data(filepaths, country_names=None):
    """
    Convenience function for complete solar data analysis
    
    Args:
        filepaths (list): List of CSV file paths
        country_names (list): Corresponding country names
        
    Returns:
        dict: Analysis results
    """
    from scripts.data_processing import load_and_clean_data
    
    if country_names is None:
        country_names = [f"Country_{i+1}" for i in range(len(filepaths))]
    
    country_data = {}
    analyzer = SolarAnalyzer()
    
    for filepath, country in zip(filepaths, country_names):
        print(f"\n🔍 Analyzing {country}...")
        df = load_and_clean_data(filepath, country_name=country)
        if df is not None:
            country_data[country] = df
            analyzer.calculate_summary_statistics(df, country)
            analyzer.analyze_correlations(df)
    
    if len(country_data) >= 2:
        insights = analyzer.generate_insights_report(country_data)
        return insights
    else:
        print("❌ Need data from at least 2 countries for comparison")
        return {}

if __name__ == "__main__":
    print("🧪 Testing analysis module...")
    analyzer = SolarAnalyzer()
    print("✅ analysis module loaded successfully!")
