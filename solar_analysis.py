import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def process_data(pr_path, ghi_path):
    """
    Process all PR and GHI CSV files and merge them into a single DataFrame
    
    Parameters:
    pr_path: path to PR data folder
    ghi_path: path to GHI data folder
    
    Returns: DataFrame with columns [Date, GHI, PR]
    """
    print("=== DATA PROCESSING ===\n")
    
    print("1. Reading all PR files...")
    pr_files = glob.glob(os.path.join(pr_path, "*", "*.csv"))
    pr_files.sort()
    
    pr_data_list = []
    for file in pr_files:
        df = pd.read_csv(file)
        pr_data_list.append(df)
    
    pr_combined = pd.concat(pr_data_list, ignore_index=True)
    print(f"   Total PR records: {len(pr_combined)}")
    
    print("2. Reading all GHI files...")
    ghi_files = glob.glob(os.path.join(ghi_path, "*", "*.csv"))
    ghi_files.sort()
    
    ghi_data_list = []
    for file in ghi_files:
        df = pd.read_csv(file)
        ghi_data_list.append(df)
    
    ghi_combined = pd.concat(ghi_data_list, ignore_index=True)
    print(f"   Total GHI records: {len(ghi_combined)}")
    
    print("3. Merging PR and GHI data...")
    pr_combined['Date'] = pd.to_datetime(pr_combined['Date'])
    ghi_combined['Date'] = pd.to_datetime(ghi_combined['Date'])
    
    merged_data = pd.merge(pr_combined, ghi_combined, on='Date', how='inner')
    merged_data = merged_data[['Date', 'GHI', 'PR']]
    
    print(f"   Merged records: {len(merged_data)}")
    return merged_data

def create_visualization(df, start_date=None, end_date=None):
    """
    Create visualization with scatter plot, moving average, and budget line
    
    Parameters:
    df: processed DataFrame
    start_date: optional start date for filtering (YYYY-MM-DD format)
    end_date: optional end date for filtering (YYYY-MM-DD format)
    """
    print("\n=== DATA VISUALIZATION ===\n")
    
    # Applying date filtering if provided 
    if start_date or end_date:
        if start_date:
            start_date = pd.to_datetime(start_date)
            df = df[df['Date'] >= start_date]
        if end_date:
            end_date = pd.to_datetime(end_date)
            df = df[df['Date'] <= end_date]
    
    # Calculating 30-day moving average
    df['PR_30MA'] = df['PR'].rolling(window=30, center=True).mean()
    
    # Calculating budget line
    start_budget = 73.9
    annual_degradation = 0.008
    start_date_data = df['Date'].min()
    df['days_from_start'] = (df['Date'] - start_date_data).dt.days
    df['years_from_start'] = df['days_from_start'] / 365.25
    df['budget_line'] = start_budget * ((1 - annual_degradation) ** df['years_from_start'])
    
    # GHI-based color mapping
    def get_color(ghi_value):
        if ghi_value < 2:
            return 'navy'
        elif ghi_value < 4:
            return 'lightblue'
        elif ghi_value < 6:
            return 'orange'
        else:
            return 'brown'
    
    df['color'] = df['GHI'].apply(get_color)
    
    # visualization
    plt.figure(figsize=(15, 10))
    
    # Scatter plot with GHI-based colors
    for color_name in ['navy', 'lightblue', 'orange', 'brown']:
        mask = df['color'] == color_name
        if mask.any():
            plt.scatter(df[mask]['Date'], df[mask]['PR'], 
                       c=color_name, s=20, alpha=0.6,
                       label=f'GHI: {get_ghi_range(color_name)}')
    
    # Moving average and budget lines
    valid_ma = df.dropna(subset=['PR_30MA'])
    plt.plot(valid_ma['Date'], valid_ma['PR_30MA'], 
             color='red', linewidth=2, label='30-day Moving Average')
    plt.plot(df['Date'], df['budget_line'], 
             color='green', linewidth=2, linestyle='--', label='Budget Line')
    
    # Calculating statistics
    latest_date = df['Date'].max()
    
    last_7_days = df[df['Date'] > (latest_date - timedelta(days=7))]
    avg_7_day = last_7_days['PR'].mean()
    
    last_30_days = df[df['Date'] > (latest_date - timedelta(days=30))]
    avg_30_day = last_30_days['PR'].mean()
    
    last_60_days = df[df['Date'] > (latest_date - timedelta(days=60))]
    avg_60_day = last_60_days['PR'].mean()
    
    # Yearly statistics
    df['year'] = df['Date'].dt.year
    yearly_stats = {}
    for year in df['year'].unique():
        year_data = df[df['year'] == year]
        above_budget = (year_data['PR'] > year_data['budget_line']).sum()
        yearly_stats[year] = above_budget
    
    # Statistics text box
    stats_text = f"Statistics:\n"
    stats_text += f"7-day avg: {avg_7_day:.1f}%\n"
    stats_text += f"30-day avg: {avg_30_day:.1f}%\n"
    stats_text += f"60-day avg: {avg_60_day:.1f}%\n\n"
    stats_text += "Points above budget:\n"
    for year, count in yearly_stats.items():
        stats_text += f"{year}: {count}\n"
    
    plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
             fontsize=10)
    
    # Formatting for more readability
    plt.title('Solar PV Plant Performance Analysis', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Performance Ratio (%)', fontsize=12)
    plt.legend(loc='upper right', bbox_to_anchor=(0.98, 0.65))
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Saving visualization
    plt.savefig("solar_performance_analysis.png", dpi=300, bbox_inches='tight')
    plt.show()
    
    return df

def get_ghi_range(color):
    """Helper function to get GHI range for legend"""
    ranges = {
        'navy': '<2',
        'lightblue': '2-4', 
        'orange': '4-6',
        'brown': '>6'
    }
    return ranges.get(color, '')

def main():
    """Main execution function"""
    # Data paths
    pr_path = r"C:\Users\91989\Downloads\dataaa\data\PR"
    ghi_path = r"C:\Users\91989\Downloads\dataaa\data\GHI"
    
    # Process data
    processed_data = process_data(pr_path, ghi_path)
    
    # Save CSV
    output_csv = "processed_solar_data.csv"
    processed_data.to_csv(output_csv, index=False)
    print(f"\n Data saved to: {output_csv}")
    
    # Creating visualization
    final_data = create_visualization(processed_data)
    
    print(f"\n Visualization saved as: solar_performance_analysis.png")
    print(f" Total rows processed: {len(final_data)}")
    print("\n TASK COMPLETED! ")

if __name__ == "__main__":
    main()
