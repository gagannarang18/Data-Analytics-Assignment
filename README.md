# Solar PV Plant Performance Analysis

A comprehensive Python project for analyzing solar photovoltaic plant performance using Performance Ratio (PR) and Global Horizontal Irradiance (GHI) data. Processes 982 daily records from July 2019 to March 2022, generating visualizations with 30-day moving averages, budget line performance tracking, and GHI-based color coding.

## Features
- Data consolidation from multiple CSV files into single dataset
- Performance visualization with scatter plots and trend analysis  
- 30-day moving average calculation and visualization
- Dynamic budget line modeling (73.9% baseline with 0.8% annual degradation)
- Statistical dashboard showing 7/30/60-day averages
- Color-coded GHI analysis (Navy: <2, Light Blue: 2-4, Orange: 4-6, Brown: >6)
- Date range filtering for custom analysis periods

## Tech Stack
Python 3.7+, pandas, numpy, matplotlib, datetime, glob

## Usage
python solar_analysis.py


## Output Files
- `processed_solar_data.csv` - Consolidated dataset (Date, GHI, PR columns)
- `solar_performance_analysis.png` - Performance visualization chart

## Key Functions
- `process_data()` - Merges PR and GHI datasets
- `create_visualization()` - Generates comprehensive performance charts
- Bonus: Date filtering for custom range analysis

## Data Requirements
Place PR and GHI CSV files in respective folders organized by year-month. **Note: Large datasets not included in repository due to size constraints. Contact for data access.**

## Project Deliverables
Complete take-home assessment solution featuring data processing pipeline, statistical analysis, and professional visualization meeting all specified requirements including budget line calculations and performance metrics dashboard.
