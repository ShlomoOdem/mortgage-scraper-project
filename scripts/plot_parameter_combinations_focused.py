#!/usr/bin/env python3
"""
Focused script to plot parameter combinations with better data filtering.
Shows clear visualizations of mortgage parameters with Weighted Monthly Payment on y-axis.
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os
from itertools import combinations

def load_and_filter_data():
    """Load the data and filter for the specified parameters with better quality control"""
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
    
    # Additional filtering for better data quality
    # Remove outliers (very high or very low weighted payments)
    q1 = filtered_df['Weighted Monthly Payment (30 years)'].quantile(0.01)
    q3 = filtered_df['Weighted Monthly Payment (30 years)'].quantile(0.99)
    filtered_df = filtered_df[
        (filtered_df['Weighted Monthly Payment (30 years)'] >= q1) &
        (filtered_df['Weighted Monthly Payment (30 years)'] <= q3)
    ]
    print(f"📊 After removing outliers: {len(filtered_df):,} rows")
    
    return filtered_df

def get_representative_values(df, param, max_values=5):
    """Get representative values for a parameter"""
    if param in df.columns:
        values = df[param].unique()
        if param in ['Term_Months', 'Inflation_Rate', 'Interest_Rate']:
            # For numeric parameters, get evenly spaced values
            values = sorted(values)
            if len(values) > max_values:
                indices = np.linspace(0, len(values)-1, max_values, dtype=int)
                values = [values[i] for i in indices]
        else:
            # For categorical parameters, take the most common values
            value_counts = df[param].value_counts()
            values = value_counts.head(max_values).index.tolist()
        return values
    return []

def create_focused_2d_plots(df):
    """Create focused 2D plots with clear parameter combinations"""
    
    # Define parameters for x-axis
    x_axis_params = ['Term_Months', 'Inflation_Rate', 'Interest_Rate']
    available_params = [param for param in x_axis_params if param in df.columns]
    
    print(f"📊 Creating focused 2D plots...")
    
    # Create plots for each x-axis parameter
    for i, x_param in enumerate(available_params):
        print(f"  📈 Plot {i+1}: {x_param} vs Weighted Payment")
        
        # Create subplot
        fig = make_subplots(
            rows=1, cols=1,
            subplot_titles=[f'{x_param} vs Weighted Monthly Payment']
        )
        
        # Get representative values for coloring
        color_params = ['Amortization_Method', 'loan_type']
        available_color_params = [p for p in color_params if p in df.columns]
        
        if available_color_params:
            color_param = available_color_params[0]  # Use first available color parameter
            color_values = get_representative_values(df, color_param, 3)
            
            # Create traces for each color value
            for color_value in color_values:
                mask = df[color_param] == color_value
                subset = df[mask]
                
                if len(subset) > 0:
                    # Sort by x parameter for better visualization
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
            title=f'{x_param} vs Weighted Monthly Payment',
            xaxis_title=x_param,
            yaxis_title='Weighted Monthly Payment (NIS)',
            width=800,
            height=500,
            showlegend=True
        )
        
        # Save the plot
        filename = f"focused_2d_plot_{i+1:02d}_{x_param}_vs_weighted_payment.html"
        fig.write_html(filename)
        print(f"    ✅ Saved: {filename}")
        
        # Show the plot
        fig.show()

def create_fixed_parameter_plots(df):
    """Create plots with fixed parameter values for clearer analysis"""
    
    # Define parameters
    params = ['Term_Months', 'Inflation_Rate', 'Interest_Rate']
    available_params = [param for param in params if param in df.columns]
    
    print(f"\n📊 Creating fixed-parameter plots...")
    
    # Create plots for each parameter combination
    for i, (x_param, fixed_param) in enumerate(combinations(available_params, 2)):
        print(f"  📈 Fixed-parameter plot {i+1}: {x_param} vs Weighted Payment (fixed {fixed_param})")
        
        # Get representative values for the fixed parameter
        fixed_values = get_representative_values(df, fixed_param, 3)
        
        # Create subplot for this combination
        fig = make_subplots(
            rows=1, cols=1,
            subplot_titles=[f'{x_param} vs Weighted Payment (fixed {fixed_param})']
        )
        
        # Create traces for each fixed value
        for fixed_value in fixed_values:
            # Filter data for this fixed value with tolerance
            if fixed_param == 'Term_Months':
                tolerance = 24  # ±24 months
            elif fixed_param == 'Inflation_Rate':
                tolerance = 1.0  # ±1.0%
            else:  # Interest_Rate
                tolerance = 0.5  # ±0.5%
                
            mask = (df[fixed_param] >= fixed_value - tolerance) & (df[fixed_param] <= fixed_value + tolerance)
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
        filename = f"fixed_parameter_plot_{i+1:02d}_{x_param}_vs_weighted_payment_fixed_{fixed_param}.html"
        fig.write_html(filename)
        print(f"    ✅ Saved: {filename}")
        
        # Show the plot
        fig.show()

def create_3d_focused_plots(df):
    """Create focused 3D plots for parameter combinations"""
    
    # Define parameters for 3D plots
    params = ['Term_Months', 'Inflation_Rate', 'Interest_Rate']
    available_params = [param for param in params if param in df.columns]
    
    if len(available_params) < 2:
        print("❌ Not enough numeric parameters for 3D plots")
        return
    
    print(f"\n📊 Creating focused 3D plots...")
    
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
        filename = f"focused_3d_plot_{i+1:02d}_{x_param}_vs_{y_param}_vs_weighted_payment.html"
        fig.write_html(filename)
        print(f"    ✅ Saved: {filename}")
        
        # Show the plot
        fig.show()

def create_summary_statistics(df):
    """Create summary plots showing parameter distributions"""
    
    print(f"\n📊 Creating summary statistics plots...")
    
    # Create subplots for parameter distributions
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[
            'Weighted Payment Distribution',
            'Term Distribution', 
            'Interest Rate Distribution',
            'Inflation Rate Distribution'
        ]
    )
    
    # 1. Weighted Payment Distribution
    fig.add_trace(
        go.Histogram(
            x=df['Weighted Monthly Payment (30 years)'],
            nbinsx=30,
            name='Weighted Payment',
            marker_color='lightblue'
        ),
        row=1, col=1
    )
    
    # 2. Term Distribution
    fig.add_trace(
        go.Histogram(
            x=df['Term_Months'],
            nbinsx=20,
            name='Term',
            marker_color='lightgreen'
        ),
        row=1, col=2
    )
    
    # 3. Interest Rate Distribution
    fig.add_trace(
        go.Histogram(
            x=df['Interest_Rate'],
            nbinsx=20,
            name='Interest Rate',
            marker_color='lightcoral'
        ),
        row=2, col=1
    )
    
    # 4. Inflation Rate Distribution
    fig.add_trace(
        go.Histogram(
            x=df['Inflation_Rate'],
            nbinsx=20,
            name='Inflation Rate',
            marker_color='lightyellow'
        ),
        row=2, col=2
    )
    
    # Update layout
    fig.update_layout(
        title='Parameter Distributions',
        height=800,
        showlegend=False
    )
    
    # Update axes labels
    fig.update_xaxes(title_text="Weighted Payment (NIS)", row=1, col=1)
    fig.update_yaxes(title_text="Count", row=1, col=1)
    fig.update_xaxes(title_text="Term (months)", row=1, col=2)
    fig.update_yaxes(title_text="Count", row=1, col=2)
    fig.update_xaxes(title_text="Interest Rate (%)", row=2, col=1)
    fig.update_yaxes(title_text="Count", row=2, col=1)
    fig.update_xaxes(title_text="Inflation Rate (%)", row=2, col=2)
    fig.update_yaxes(title_text="Count", row=2, col=2)
    
    # Save the plot
    filename = "parameter_distributions.html"
    fig.write_html(filename)
    print(f"    ✅ Saved: {filename}")
    
    # Show the plot
    fig.show()

def main():
    """Main function to run the focused analysis"""
    print("🏠 Focused Mortgage Parameter Analysis")
    print("=" * 50)
    
    # Load and filter data
    df = load_and_filter_data()
    
    if len(df) == 0:
        print("❌ No data found with weighted payment values")
        return
    
    print(f"\n📊 Data summary:")
    print(f"  • Total records: {len(df):,}")
    print(f"  • Weighted payment range: {df['Weighted Monthly Payment (30 years)'].min():,.0f} - {df['Weighted Monthly Payment (30 years)'].max():,.0f} NIS")
    print(f"  • Available parameters: {list(df.columns)}")
    
    # Create focused 2D plots
    create_focused_2d_plots(df)
    
    # Create fixed parameter plots
    create_fixed_parameter_plots(df)
    
    # Create focused 3D plots
    create_3d_focused_plots(df)
    
    # Create summary statistics
    create_summary_statistics(df)
    
    print("\n✅ Focused analysis complete!")
    print("📁 All plots have been saved as HTML files and displayed in browser")

if __name__ == "__main__":
    main() 