"""
Visualization functions for Solar Challenge
Modular plotting functions for consistent visualizations
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

class SolarVisualizer:
    """Class for creating solar data visualizations"""
    
    def __init__(self, style='seaborn-v0_8'):
        self.style = style
        self.setup_style()
    
    def setup_style(self):
        """Set consistent plot style"""
        plt.style.use(self.style)
        sns.set_palette("husl")
    
    def create_time_series_plot(self, df, metrics=None, figsize=(15, 10), title_suffix=""):
        """
        Create time series plots for solar metrics
        
        Args:
            df (DataFrame): Data with timestamp
            metrics (list): Metrics to plot
            figsize (tuple): Figure size
            title_suffix (str): Additional title text
            
        Returns:
            matplotlib.figure.Figure: The created figure
        """
        if metrics is None:
            metrics = ['GHI', 'Tamb', 'DNI', 'WS']
        
        self.setup_style()
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        axes = axes.flatten()
        
        colors = ['blue', 'red', 'green', 'purple']
        
        for i, metric in enumerate(metrics):
            if i < len(axes) and metric in df.columns:
                axes[i].plot(df['Timestamp'], df[metric], 
                           alpha=0.7, linewidth=0.5, color=colors[i])
                axes[i].set_title(f'{metric} Over Time')
                axes[i].set_ylabel(self._get_metric_unit(metric))
                axes[i].tick_params(axis='x', rotation=45)
                axes[i].grid(True, alpha=0.3)
        
        plt.suptitle(f'Solar Metrics Time Series {title_suffix}', fontsize=16)
        plt.tight_layout()
        return fig
    
    def create_correlation_heatmap(self, df, columns=None, figsize=(12, 8)):
        """
        Create correlation heatmap for solar parameters
        
        Args:
            df (DataFrame): Input data
            columns (list): Columns to include
            figsize (tuple): Figure size
            
        Returns:
            matplotlib.figure.Figure: The created figure
        """
        if columns is None:
            columns = ['GHI', 'DNI', 'DHI', 'TModA', 'TModB', 'Tamb', 'RH', 'WS', 'BP']
        
        available_columns = [col for col in columns if col in df.columns]
        
        self.setup_style()
        fig, ax = plt.subplots(figsize=figsize)
        
        correlation_matrix = df[available_columns].corr()
        
        mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
        sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='RdBu_r', 
                   center=0, fmt='.2f', square=True, cbar_kws={'shrink': 0.8}, ax=ax)
        
        ax.set_title('Correlation Heatmap - Solar Parameters', fontsize=14, pad=20)
        return fig
    
    def create_distribution_plots(self, df, metrics=None, figsize=(15, 10)):
        """
        Create distribution plots for solar metrics
        
        Args:
            df (DataFrame): Input data
            metrics (list): Metrics to plot
            figsize (tuple): Figure size
            
        Returns:
            matplotlib.figure.Figure: The created figure
        """
        if metrics is None:
            metrics = ['GHI', 'Tamb', 'RH', 'WS']
        
        self.setup_style()
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        axes = axes.flatten()
        
        colors = ['gold', 'red', 'blue', 'skyblue']
        
        for i, metric in enumerate(metrics):
            if i < len(axes) and metric in df.columns:
                axes[i].hist(df[metric].dropna(), bins=50, alpha=0.7, 
                           color=colors[i], edgecolor='black')
                axes[i].set_title(f'{metric} Distribution')
                axes[i].set_xlabel(self._get_metric_unit(metric))
                axes[i].set_ylabel('Frequency')
                axes[i].grid(True, alpha=0.3)
        
        plt.suptitle('Solar Metrics Distribution', fontsize=16)
        plt.tight_layout()
        return fig
    
    def create_comparison_boxplots(self, data_dict, metric='GHI', figsize=(12, 6)):
        """
        Create boxplot comparison across multiple datasets
        
        Args:
            data_dict (dict): Dictionary of {country_name: dataframe}
            metric (str): Metric to compare
            figsize (tuple): Figure size
            
        Returns:
            matplotlib.figure.Figure: The created figure
        """
        self.setup_style()
        fig, ax = plt.subplots(figsize=figsize)
        
        plot_data = []
        labels = []
        for country, df in data_dict.items():
            if metric in df.columns:
                plot_data.append(df[metric].dropna())
                labels.append(country)
        
        ax.boxplot(plot_data, labels=labels)
        ax.set_title(f'{metric} Comparison Across Countries', fontsize=14)
        ax.set_ylabel(self._get_metric_unit(metric))
        ax.grid(True, alpha=0.3)
        ax.tick_params(axis='x', rotation=45)
        
        return fig
    
    def _get_metric_unit(self, metric):
        """Get proper unit label for metrics"""
        units = {
            'GHI': 'GHI (W/m²)',
            'DNI': 'DNI (W/m²)',
            'DHI': 'DHI (W/m²)',
            'Tamb': 'Temperature (°C)',
            'RH': 'Relative Humidity (%)',
            'WS': 'Wind Speed (m/s)',
            'BP': 'Pressure (hPa)'
        }
        return units.get(metric, metric)
    
    def save_plot(self, fig, filename, dpi=300):
        """
        Save plot to file
        
        Args:
            fig (matplotlib.figure.Figure): Figure to save
            filename (str): Output filename
            dpi (int): Resolution for saving
        """
        fig.savefig(filename, dpi=dpi, bbox_inches='tight')
        print(f"💾 Plot saved: {filename}")

# Convenience functions
def create_analysis_report(df, country_name, output_dir='reports'):
    """
    Create comprehensive analysis report for a country
    
    Args:
        df (DataFrame): Cleaned solar data
        country_name (str): Country name
        output_dir (str): Output directory for plots
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    visualizer = SolarVisualizer()
    
    # Create various plots
    time_series_fig = visualizer.create_time_series_plot(df, title_suffix=f"- {country_name}")
    visualizer.save_plot(time_series_fig, f"{output_dir}/{country_name}_time_series.png")
    
    correlation_fig = visualizer.create_correlation_heatmap(df)
    visualizer.save_plot(correlation_fig, f"{output_dir}/{country_name}_correlation.png")
    
    distribution_fig = visualizer.create_distribution_plots(df)
    visualizer.save_plot(distribution_fig, f"{output_dir}/{country_name}_distributions.png")
    
    plt.close('all')
    print(f"✅ Analysis report created for {country_name}")

if __name__ == "__main__":
    print("🧪 Testing visualization module...")
    visualizer = SolarVisualizer()
    print("✅ visualization module loaded successfully!")
