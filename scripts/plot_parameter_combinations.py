#!/usr/bin/env python3
"""
Script to plot all combinations of mortgage parameters with Weighted Monthly Payment on y-axis.
Creates multiple graphs showing different parameter combinations with various fixed values.
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os
from itertools import combinations

def load_and_filter_data():
    """Load the data and filter for the specified parameters"""
    print("📂 Loading mortgage data...")
    
    # Load the combined data
    df = pd.read_csv('data/analyzed/combined_summary_files.csv')
    print(f"✅ Data loaded: {len(df):,} total rows")
    
    # Select only the specified parameters
    parameter_mapping = {
        'Weighted Monthly Payment (30 years)': 'Weighted Monthly Payment (30 years)',
        'Term_Months': 'Term_Months',
        'Inflation_Rate': 'Inflation_Rate',
        'Interest_Rate': 'Interest_Rate',
        'Channel': 'loan_type',
        'Amortization_Method': 'Amortization_Method'
    }
    
    # Filter for columns that exist
    available_columns = [col for col in parameter_mapping.values() if col in df.columns]
    filtered_df = df[available_columns].copy()
    
    print(f"📊 Filtered data: {len(filtered_df):,} rows with {len(available_columns)} parameters")
    
    # Convert numeric columns
    numeric_columns = ['Weighted Monthly Payment (30 years)', 'Term_Months', 'Inflation_Rate', 'Interest_Rate']
    for col in numeric_columns:
        if col in filtered_df.columns:
            if col == 'Weighted Monthly Payment (30 years)':
                # Handle comma-separated numbers
                filtered_df[col] = filtered_df[col].str.replace(',', '').astype(float)
            else:
                filtered_df[col] = pd.to_numeric(filtered_df[col], errors='coerce')
    
    # Remove rows with missing weighted payment data
    original_count = len(filtered_df)
    filtered_df = filtered_df[filtered_df['Weighted Monthly Payment (30 years)'].notna()]
    print(f"📊 After removing missing weighted payment data: {len(filtered_df):,} rows")
    
    return filtered_df

def get_parameter_values(df, param):
    """Get unique values for a parameter"""
    if param in df.columns:
        values = df[param].unique()
        if param in ['Term_Months', 'Inflation_Rate', 'Interest_Rate']:
            # For numeric parameters, get a few representative values
            values = sorted(values)
            if len(values) > 5:
                # Take evenly spaced values
                indices = np.linspace(0, len(values)-1, 5, dtype=int)
                values = [values[i] for i in indices]
        return values
    return []

def create_parameter_combination_plots(df):
    """Create plots for all parameter combinations"""
    
    # Define parameters (excluding Weighted Monthly Payment which is always on y-axis)
    x_axis_params = ['Term_Months', 'Inflation_Rate', 'Interest_Rate', 'loan_type', 'Amortization_Method']
    available_params = [param for param in x_axis_params if param in df.columns]
    
    print(f"📊 Available parameters for x-axis: {available_params}")
    
    # Create all possible combinations of 2 parameters for x-axis and color
    param_combinations = list(combinations(available_params, 2))
    
    print(f"📊 Creating {len(param_combinations)} parameter combination plots...")
    
    for i, (x_param, color_param) in enumerate(param_combinations):
        print(f"  📈 Plot {i+1}: {x_param} vs Weighted Payment (colored by {color_param})")
        
        # Get sample values for the color parameter
        color_values = get_parameter_values(df, color_param)
        
        if len(color_values) == 0:
            continue
            
        # Create subplot for this combination
        fig = make_subplots(
            rows=1, cols=1,
            subplot_titles=[f'{x_param} vs Weighted Payment (colored by {color_param})']
        )
        
        # Create traces for each color value
        for color_value in color_values[:5]:  # Limit to 5 colors for clarity
            # Filter data for this color value
            if color_param in ['Term_Months', 'Inflation_Rate', 'Interest_Rate']:
                # For numeric parameters, use a range around the value
                if color_param == 'Term_Months':
                    tolerance = 12  # ±12 months
                elif color_param == 'Inflation_Rate':
                    tolerance = 0.5  # ±0.5%
                else:  # Interest_Rate
                    tolerance = 0.25  # ±0.25%
                    
                mask = (df[color_param] >= color_value - tolerance) & (df[color_param] <= color_value + tolerance)
            else:
                # For categorical parameters, exact match
                mask = df[color_param] == color_value
                
            subset = df[mask]
            
            if len(subset) > 0:
                # Sort by x parameter for better line visualization
                subset = subset.sort_values(x_param)
                
                fig.add_trace(
                    go.Scatter(
                        x=subset[x_param],
                        y=subset['Weighted Monthly Payment (30 years)'],
                        mode='markers',
                        name=f'{color_param}={color_value}',
                        marker=dict(size=6),
                        hovertemplate=f'<b>{color_param}: {color_value}</b><br>' +
                                    f'{x_param}: %{{x}}<br>' +
                                    'Weighted Payment: %{y:,.0f} NIS<br>' +
                                    '<extra></extra>'
                    )
                )
        
        # Update layout
        fig.update_layout(
            title=f'{x_param} vs Weighted Monthly Payment (colored by {color_param})',
            xaxis_title=x_param,
            yaxis_title='Weighted Monthly Payment (NIS)',
            width=800,
            height=500,
            showlegend=True
        )
        
        # Save the plot
        filename = f"parameter_combination_{i+1:02d}_{x_param}_vs_weighted_payment_colored_by_{color_param}.html"
        fig.write_html(filename)
        print(f"    ✅ Saved: {filename}")
        
        # Show the plot
        fig.show()

def create_fixed_value_plots(df):
    """Create plots with fixed parameter values"""
    
    # Define parameters
    params = ['Term_Months', 'Inflation_Rate', 'Interest_Rate', 'loan_type', 'Amortization_Method']
    available_params = [param for param in params if param in df.columns]
    
    print(f"\n📊 Creating fixed-value plots...")
    
    # Create plots for each parameter combination
    for i, (x_param, fixed_param) in enumerate(combinations(available_params, 2)):
        print(f"  📈 Fixed-value plot {i+1}: {x_param} vs Weighted Payment (fixed {fixed_param})")
        
        # Get sample values for the fixed parameter
        fixed_values = get_parameter_values(df, fixed_param)
        
        if len(fixed_values) == 0:
            continue
            
        # Create subplot for this combination
        fig = make_subplots(
            rows=1, cols=1,
            subplot_titles=[f'{x_param} vs Weighted Payment (fixed {fixed_param})']
        )
        
        # Create traces for each fixed value
        for fixed_value in fixed_values[:3]:  # Limit to 3 fixed values for clarity
            # Filter data for this fixed value
            if fixed_param in ['Term_Months', 'Inflation_Rate', 'Interest_Rate']:
                # For numeric parameters, use a range around the value
                if fixed_param == 'Term_Months':
                    tolerance = 12  # ±12 months
                elif fixed_param == 'Inflation_Rate':
                    tolerance = 0.5  # ±0.5%
                else:  # Interest_Rate
                    tolerance = 0.25  # ±0.25%
                    
                mask = (df[fixed_param] >= fixed_value - tolerance) & (df[fixed_param] <= fixed_value + tolerance)
            else:
                # For categorical parameters, exact match
                mask = df[fixed_param] == fixed_value
                
            subset = df[mask]
            
            if len(subset) > 0:
                # Sort by x parameter for better line visualization
                subset = subset.sort_values(x_param)
                
                fig.add_trace(
                    go.Scatter(
                        x=subset[x_param],
                        y=subset['Weighted Monthly Payment (30 years)'],
                        mode='markers',
                        name=f'{fixed_param}={fixed_value}',
                        marker=dict(size=8),
                        hovertemplate=f'<b>{fixed_param}: {fixed_value}</b><br>' +
                                    f'{x_param}: %{{x}}<br>' +
                                    'Weighted Payment: %{y:,.0f} NIS<br>' +
                                    '<extra></extra>'
                    )
                )
        
        # Update layout
        fig.update_layout(
            title=f'{x_param} vs Weighted Monthly Payment (fixed {fixed_param})',
            xaxis_title=x_param,
            yaxis_title='Weighted Monthly Payment (NIS)',
            width=800,
            height=500,
            showlegend=True
        )
        
        # Save the plot
        filename = f"fixed_value_plot_{i+1:02d}_{x_param}_vs_weighted_payment_fixed_{fixed_param}.html"
        fig.write_html(filename)
        print(f"    ✅ Saved: {filename}")
        
        # Show the plot
        fig.show()

def create_3d_plots(df):
    """Create 3D plots for parameter combinations"""
    
    # Define parameters for 3D plots
    params = ['Term_Months', 'Inflation_Rate', 'Interest_Rate']
    available_params = [param for param in params if param in df.columns]
    
    if len(available_params) < 2:
        print("❌ Not enough numeric parameters for 3D plots")
        return
    
    print(f"\n📊 Creating 3D plots...")
    
    # Create 3D plots for each combination
    for i, (x_param, y_param) in enumerate(combinations(available_params, 2)):
        print(f"  📈 3D plot {i+1}: {x_param} vs {y_param} vs Weighted Payment")
        
        fig = go.Figure()
        
        # Create 3D scatter plot
        fig.add_trace(
            go.Scatter3d(
                x=df[x_param],
                y=df[y_param],
                z=df['Weighted Monthly Payment (30 years)'],
                mode='markers',
                marker=dict(
                    size=4,
                    color=df['Weighted Monthly Payment (30 years)'],
                    colorscale='Viridis',
                    opacity=0.8
                ),
                hovertemplate=f'{x_param}: %{{x}}<br>' +
                            f'{y_param}: %{{y}}<br>' +
                            'Weighted Payment: %{z:,.0f} NIS<br>' +
                            '<extra></extra>'
            )
        )
        
        # Update layout
        fig.update_layout(
            title=f'3D: {x_param} vs {y_param} vs Weighted Monthly Payment',
            scene=dict(
                xaxis_title=x_param,
                yaxis_title=y_param,
                zaxis_title='Weighted Monthly Payment (NIS)'
            ),
            width=800,
            height=600
        )
        
        # Save the plot
        filename = f"3d_plot_{i+1:02d}_{x_param}_vs_{y_param}_vs_weighted_payment.html"
        fig.write_html(filename)
        print(f"    ✅ Saved: {filename}")
        
        # Show the plot
        fig.show()

def main():
    """Main function to run the analysis"""
    print("🏠 Mortgage Parameter Combination Analysis")
    print("=" * 50)
    
    # Load and filter data
    df = load_and_filter_data()
    
    if len(df) == 0:
        print("❌ No data found with weighted payment values")
        return
    
    print(f"\n📊 Data summary:")
    print(f"  • Total records: {len(df):,}")
    print(f"  • Available parameters: {list(df.columns)}")
    
    # Create parameter combination plots
    create_parameter_combination_plots(df)
    
    # Create fixed value plots
    create_fixed_value_plots(df)
    
    # Create 3D plots
    create_3d_plots(df)
    
    print("\n✅ Analysis complete!")
    print("📁 All plots have been saved as HTML files and displayed in browser")

if __name__ == "__main__":
    main() 