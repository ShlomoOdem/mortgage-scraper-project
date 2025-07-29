#!/usr/bin/env python3
"""
Clean script to plot parameter combinations with fixed values.
Each graph shows data points where all parameters except (x,y,label) are fixed to the same value.
Each point has a popup with all its data.
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os

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

def get_representative_values(df, param, max_values=3):
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

def create_clean_fixed_combinations(df):
    """Create clean graphs with fixed parameter combinations"""
    
    print(f"📊 Creating clean fixed parameter combinations...")
    
    # Define specific combinations to analyze
    combinations_to_analyze = [
        {
            'x_param': 'Interest_Rate',
            'y_param': 'Weighted Monthly Payment (30 years)',
            'label_param': 'Inflation_Rate',
            'fixed_params': ['Term_Months', 'Amortization_Method'],
            'title': 'Interest Rate vs Weighted Payment (labeled by Inflation Rate)'
        },
        {
            'x_param': 'Term_Months',
            'y_param': 'Weighted Monthly Payment (30 years)',
            'label_param': 'Interest_Rate',
            'fixed_params': ['Inflation_Rate', 'Amortization_Method'],
            'title': 'Term vs Weighted Payment (labeled by Interest Rate)'
        },
        {
            'x_param': 'Inflation_Rate',
            'y_param': 'Weighted Monthly Payment (30 years)',
            'label_param': 'Interest_Rate',
            'fixed_params': ['Term_Months', 'Amortization_Method'],
            'title': 'Inflation Rate vs Weighted Payment (labeled by Interest Rate)'
        }
    ]
    
    graph_count = 0
    
    for combo in combinations_to_analyze:
        x_param = combo['x_param']
        y_param = combo['y_param']
        label_param = combo['label_param']
        fixed_params = combo['fixed_params']
        title = combo['title']
        
        print(f"\n📈 {title}")
        
        # Get sample values for fixed parameters
        fixed_param_samples = {}
        for param in fixed_params:
            if param in df.columns:
                values = get_representative_values(df, param, 2)  # Use 2 values for cleaner graphs
                fixed_param_samples[param] = values
        
        # Create graphs with different fixed value combinations
        if fixed_param_samples:
            from itertools import product
            fixed_value_lists = [fixed_param_samples[param] for param in fixed_params if param in fixed_param_samples]
            fixed_combinations = list(product(*fixed_value_lists))
        else:
            fixed_combinations = [()]
        
        print(f"  📊 Creating {len(fixed_combinations)} graphs with different fixed values")
        
        for fixed_values in fixed_combinations:
            graph_count += 1
            
            # Create filter mask
            mask = pd.Series([True] * len(df))
            fixed_param_dict = {}
            
            # Handle fixed parameters
            available_fixed_params = [param for param in fixed_params if param in df.columns]
            for k, param in enumerate(available_fixed_params):
                if k < len(fixed_values):
                    fixed_value = fixed_values[k]
                    if param in ['Term_Months', 'Inflation_Rate', 'Interest_Rate']:
                        # For numeric parameters, use tolerance
                        if param == 'Term_Months':
                            tolerance = 24  # ±24 months
                        elif param == 'Inflation_Rate':
                            tolerance = 1.0  # ±1.0%
                        else:  # Interest_Rate
                            tolerance = 0.5  # ±0.5%
                        
                        param_mask = (df[param] >= fixed_value - tolerance) & (df[param] <= fixed_value + tolerance)
                    else:
                        # For categorical parameters, exact match
                        param_mask = df[param] == fixed_value
                    
                    mask = mask & param_mask
                    fixed_param_dict[param] = fixed_value
            
            # Filter data
            subset = df[mask]
            
            if len(subset) > 0:
                print(f"    📈 Graph {graph_count}: {len(subset)} data points")
                
                # Create the plot
                fig = go.Figure()
                
                # Get unique values for the label parameter
                label_values = subset[label_param].unique()
                
                # Create traces for each label value
                for label_value in label_values:
                    label_subset = subset[subset[label_param] == label_value]
                    
                    if len(label_subset) > 0:
                        # Sort by x parameter
                        label_subset = label_subset.sort_values(x_param)
                        
                        # Create hover text with all parameter values
                        hover_texts = []
                        for _, row in label_subset.iterrows():
                            hover_text = f"<b>{label_param}: {row[label_param]}</b><br>"
                            hover_text += f"{x_param}: {row[x_param]}<br>"
                            hover_text += f"Weighted Payment: {row['Weighted Monthly Payment (30 years)']:,.0f} NIS<br>"
                            
                            # Add all fixed parameters
                            for param, value in fixed_param_dict.items():
                                hover_text += f"{param}: {value}<br>"
                            
                            # Add any other available parameters
                            for col in df.columns:
                                if col not in [x_param, y_param, label_param] and col not in fixed_param_dict:
                                    hover_text += f"{col}: {row[col]}<br>"
                            
                            hover_text += "<extra></extra>"
                            hover_texts.append(hover_text)
                        
                        fig.add_trace(
                            go.Scatter(
                                x=label_subset[x_param],
                                y=label_subset['Weighted Monthly Payment (30 years)'],
                                mode='markers',
                                name=f'{label_param}={label_value}',
                                marker=dict(size=8),
                                hovertemplate='%{text}',
                                text=hover_texts
                            )
                        )
                
                # Create title with fixed parameter information
                full_title = title
                if fixed_param_dict:
                    full_title += "<br><sub>Fixed: "
                    fixed_info = []
                    for param, value in fixed_param_dict.items():
                        fixed_info.append(f"{param}={value}")
                    full_title += ", ".join(fixed_info) + "</sub>"
                
                # Update layout
                fig.update_layout(
                    title=full_title,
                    xaxis_title=x_param,
                    yaxis_title='Weighted Monthly Payment (NIS)',
                    width=800,
                    height=500,
                    showlegend=True
                )
                
                # Save the plot
                filename = f"clean_fixed_graph_{graph_count:03d}_{x_param}_vs_weighted_payment_labeled_by_{label_param}.html"
                fig.write_html(filename)
                print(f"      ✅ Saved: {filename}")
                
                # Show the plot
                fig.show()
            else:
                print(f"    ⚠️  Graph {graph_count}: No data points for this combination")

def create_example_combinations(df):
    """Create specific example combinations with clear fixed values"""
    
    print(f"\n📊 Creating specific example combinations...")
    
    # Define specific examples with clear fixed values
    examples = [
        {
            'x_param': 'Interest_Rate',
            'y_param': 'Weighted Monthly Payment (30 years)',
            'label_param': 'Inflation_Rate',
            'fixed_values': {
                'Term_Months': 360,
                'Amortization_Method': 'שפיצר'
            },
            'title': 'Example 1: Interest Rate vs Weighted Payment (360 months, שפיצר)'
        },
        {
            'x_param': 'Term_Months',
            'y_param': 'Weighted Monthly Payment (30 years)',
            'label_param': 'Interest_Rate',
            'fixed_values': {
                'Inflation_Rate': 2.0,
                'Amortization_Method': 'קרן שווה'
            },
            'title': 'Example 2: Term vs Weighted Payment (Inflation=2.0%, קרן שווה)'
        },
        {
            'x_param': 'Inflation_Rate',
            'y_param': 'Weighted Monthly Payment (30 years)',
            'label_param': 'Interest_Rate',
            'fixed_values': {
                'Term_Months': 240,
                'Amortization_Method': 'שפיצר'
            },
            'title': 'Example 3: Inflation Rate vs Weighted Payment (240 months, שפיצר)'
        }
    ]
    
    graph_count = 0
    
    for example in examples:
        x_param = example['x_param']
        y_param = example['y_param']
        label_param = example['label_param']
        fixed_values = example['fixed_values']
        title = example['title']
        
        print(f"\n📈 {title}")
        
        # Create filter mask
        mask = pd.Series([True] * len(df))
        
        for param, value in fixed_values.items():
            if param in df.columns:
                if param in ['Term_Months', 'Inflation_Rate', 'Interest_Rate']:
                    # For numeric parameters, use tolerance
                    if param == 'Term_Months':
                        tolerance = 24  # ±24 months
                    elif param == 'Inflation_Rate':
                        tolerance = 1.0  # ±1.0%
                    else:  # Interest_Rate
                        tolerance = 0.5  # ±0.5%
                    
                    param_mask = (df[param] >= value - tolerance) & (df[param] <= value + tolerance)
                else:
                    # For categorical parameters, exact match
                    param_mask = df[param] == value
                
                mask = mask & param_mask
        
        # Filter data
        subset = df[mask]
        
        if len(subset) > 0:
            graph_count += 1
            print(f"  📈 Example Graph {graph_count}: {len(subset)} data points")
            
            # Create the plot
            fig = go.Figure()
            
            # Get unique values for the label parameter
            label_values = subset[label_param].unique()
            
            # Create traces for each label value
            for label_value in label_values:
                label_subset = subset[subset[label_param] == label_value]
                
                if len(label_subset) > 0:
                    # Sort by x parameter
                    label_subset = label_subset.sort_values(x_param)
                    
                    # Create hover text with all parameter values
                    hover_texts = []
                    for _, row in label_subset.iterrows():
                        hover_text = f"<b>{label_param}: {row[label_param]}</b><br>"
                        hover_text += f"{x_param}: {row[x_param]}<br>"
                        hover_text += f"Weighted Payment: {row['Weighted Monthly Payment (30 years)']:,.0f} NIS<br>"
                        
                        # Add all fixed parameters
                        for param, value in fixed_values.items():
                            hover_text += f"{param}: {value}<br>"
                        
                        # Add any other available parameters
                        for col in df.columns:
                            if col not in [x_param, y_param, label_param] and col not in fixed_values:
                                hover_text += f"{col}: {row[col]}<br>"
                        
                        hover_text += "<extra></extra>"
                        hover_texts.append(hover_text)
                    
                    fig.add_trace(
                        go.Scatter(
                            x=label_subset[x_param],
                            y=label_subset['Weighted Monthly Payment (30 years)'],
                            mode='markers',
                            name=f'{label_param}={label_value}',
                            marker=dict(size=10),
                            hovertemplate='%{text}',
                            text=hover_texts
                        )
                    )
            
            # Create title
            full_title = title
            if fixed_values:
                full_title += "<br><sub>Fixed: "
                fixed_info = []
                for param, value in fixed_values.items():
                    fixed_info.append(f"{param}={value}")
                full_title += ", ".join(fixed_info) + "</sub>"
            
            # Update layout
            fig.update_layout(
                title=full_title,
                xaxis_title=x_param,
                yaxis_title='Weighted Monthly Payment (NIS)',
                width=800,
                height=500,
                showlegend=True
            )
            
            # Save the plot
            filename = f"example_graph_{graph_count:03d}_{x_param}_vs_weighted_payment_labeled_by_{label_param}.html"
            fig.write_html(filename)
            print(f"      ✅ Saved: {filename}")
            
            # Show the plot
            fig.show()
        else:
            print(f"  ⚠️  Example Graph {graph_count}: No data points for this combination")

def main():
    """Main function to run the clean analysis"""
    print("🏠 Clean Fixed Parameter Combination Analysis")
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
    
    # Create clean fixed combinations
    create_clean_fixed_combinations(df)
    
    # Create example combinations
    create_example_combinations(df)
    
    print("\n✅ Clean fixed parameter analysis complete!")
    print("📁 All plots have been saved as HTML files and displayed in browser")

if __name__ == "__main__":
    main() 