#!/usr/bin/env python3
"""
Script to plot parameter combinations where each graph shows data points with fixed values for all other parameters.
Each point represents exactly one combination of (x,y,label) with all remaining parameters held constant.
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

def get_unique_values(df, param):
    """Get unique values for a parameter"""
    if param in df.columns:
        values = df[param].unique()
        return sorted(values) if param in ['Term_Months', 'Inflation_Rate', 'Interest_Rate'] else values
    return []

def create_fixed_parameter_graphs(df):
    """Create graphs where each point has fixed values for all other parameters"""
    
    # Define parameters
    params = ['Term_Months', 'Inflation_Rate', 'Interest_Rate', 'loan_type', 'Amortization_Method']
    available_params = [param for param in params if param in df.columns]
    
    print(f"📊 Available parameters: {available_params}")
    
    # Get unique values for each parameter
    param_values = {}
    for param in available_params:
        param_values[param] = get_unique_values(df, param)
        print(f"  • {param}: {len(param_values[param])} unique values")
    
    # Create all possible combinations of 3 parameters (x, y, label)
    param_combinations = list(combinations(available_params, 3))
    
    print(f"\n📊 Creating {len(param_combinations)} parameter combination graphs...")
    
    graph_count = 0
    
    for i, (x_param, y_param, label_param) in enumerate(param_combinations):
        print(f"\n📈 Graph {i+1}: {x_param} vs {y_param} (labeled by {label_param})")
        
        # Get sample values for fixed parameters (the remaining parameters)
        fixed_params = [p for p in available_params if p not in [x_param, y_param, label_param]]
        
        # Get sample values for each fixed parameter
        fixed_param_samples = {}
        for param in fixed_params:
            values = param_values[param]
            if len(values) > 3:
                # Take evenly spaced samples
                indices = np.linspace(0, len(values)-1, 3, dtype=int)
                fixed_param_samples[param] = [values[i] for i in indices]
            else:
                fixed_param_samples[param] = values
        
        # Create multiple graphs with different fixed value combinations
        fixed_combinations = []
        if fixed_params:
            # Generate combinations of fixed values
            from itertools import product
            fixed_value_lists = [fixed_param_samples[param] for param in fixed_params]
            fixed_combinations = list(product(*fixed_value_lists))
        else:
            # No fixed parameters, just one graph
            fixed_combinations = [()]
        
        print(f"  📊 Creating {len(fixed_combinations)} graphs with different fixed values")
        
        for j, fixed_values in enumerate(fixed_combinations):
            graph_count += 1
            
            # Create filter mask for this combination
            mask = pd.Series([True] * len(df))
            fixed_param_dict = {}
            
            for k, param in enumerate(fixed_params):
                fixed_value = fixed_values[k]
                if param in ['Term_Months', 'Inflation_Rate', 'Interest_Rate']:
                    # For numeric parameters, use a small tolerance
                    if param == 'Term_Months':
                        tolerance = 12  # ±12 months
                    elif param == 'Inflation_Rate':
                        tolerance = 0.5  # ±0.5%
                    else:  # Interest_Rate
                        tolerance = 0.25  # ±0.25%
                    
                    param_mask = (df[param] >= fixed_value - tolerance) & (df[param] <= fixed_value + tolerance)
                else:
                    # For categorical parameters, exact match
                    param_mask = df[param] == fixed_value
                
                mask = mask & param_mask
                fixed_param_dict[param] = fixed_value
            
            # Filter data for this combination
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
                        # Sort by x parameter for better visualization
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
                title = f"{x_param} vs Weighted Monthly Payment (labeled by {label_param})"
                if fixed_param_dict:
                    title += "<br><sub>Fixed: "
                    fixed_info = []
                    for param, value in fixed_param_dict.items():
                        fixed_info.append(f"{param}={value}")
                    title += ", ".join(fixed_info) + "</sub>"
                
                # Update layout
                fig.update_layout(
                    title=title,
                    xaxis_title=x_param,
                    yaxis_title='Weighted Monthly Payment (NIS)',
                    width=800,
                    height=500,
                    showlegend=True
                )
                
                # Save the plot
                filename = f"fixed_param_graph_{graph_count:03d}_{x_param}_vs_weighted_payment_labeled_by_{label_param}.html"
                fig.write_html(filename)
                print(f"      ✅ Saved: {filename}")
                
                # Show the plot
                fig.show()
            else:
                print(f"    ⚠️  Graph {graph_count}: No data points for this combination")

def create_specialized_combinations(df):
    """Create specialized combinations focusing on specific parameter relationships"""
    
    print(f"\n📊 Creating specialized parameter combinations...")
    
    # Define specific combinations to focus on
    combinations_to_analyze = [
        # Interest Rate vs Weighted Payment (labeled by Inflation Rate)
        {
            'x_param': 'Interest_Rate',
            'y_param': 'Weighted Monthly Payment (30 years)',
            'label_param': 'Inflation_Rate',
            'fixed_params': ['Term_Months', 'loan_type', 'Amortization_Method']
        },
        # Term vs Weighted Payment (labeled by Interest Rate)
        {
            'x_param': 'Term_Months',
            'y_param': 'Weighted Monthly Payment (30 years)',
            'label_param': 'Interest_Rate',
            'fixed_params': ['Inflation_Rate', 'loan_type', 'Amortization_Method']
        },
        # Inflation Rate vs Weighted Payment (labeled by Interest Rate)
        {
            'x_param': 'Inflation_Rate',
            'y_param': 'Weighted Monthly Payment (30 years)',
            'label_param': 'Interest_Rate',
            'fixed_params': ['Term_Months', 'loan_type', 'Amortization_Method']
        }
    ]
    
    graph_count = 0
    
    for combo in combinations_to_analyze:
        x_param = combo['x_param']
        y_param = combo['y_param']
        label_param = combo['label_param']
        fixed_params = combo['fixed_params']
        
        print(f"\n📈 Specialized Graph: {x_param} vs {y_param} (labeled by {label_param})")
        
        # Get sample values for fixed parameters
        fixed_param_samples = {}
        for param in fixed_params:
            if param in df.columns:
                values = get_unique_values(df, param)
                if len(values) > 2:
                    # Take 2 sample values
                    indices = [0, len(values)-1]  # First and last values
                    fixed_param_samples[param] = [values[i] for i in indices]
                else:
                    fixed_param_samples[param] = values
        
        # Create graphs with different fixed value combinations
        if fixed_param_samples:
            from itertools import product
            fixed_value_lists = [fixed_param_samples[param] for param in fixed_params if param in fixed_param_samples]
            fixed_combinations = list(product(*fixed_value_lists))
        else:
            fixed_combinations = [()]
        
        print(f"  📊 Creating {len(fixed_combinations)} specialized graphs")
        
        for fixed_values in fixed_combinations:
            graph_count += 1
            
            # Create filter mask
            mask = pd.Series([True] * len(df))
            fixed_param_dict = {}
            
            # Handle fixed parameters properly
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
                print(f"    📈 Specialized Graph {graph_count}: {len(subset)} data points")
                
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
                title = f"Specialized: {x_param} vs Weighted Monthly Payment (labeled by {label_param})"
                if fixed_param_dict:
                    title += "<br><sub>Fixed: "
                    fixed_info = []
                    for param, value in fixed_param_dict.items():
                        fixed_info.append(f"{param}={value}")
                    title += ", ".join(fixed_info) + "</sub>"
                
                # Update layout
                fig.update_layout(
                    title=title,
                    xaxis_title=x_param,
                    yaxis_title='Weighted Monthly Payment (NIS)',
                    width=800,
                    height=500,
                    showlegend=True
                )
                
                # Save the plot
                filename = f"specialized_graph_{graph_count:03d}_{x_param}_vs_weighted_payment_labeled_by_{label_param}.html"
                fig.write_html(filename)
                print(f"      ✅ Saved: {filename}")
                
                # Show the plot
                fig.show()
            else:
                print(f"    ⚠️  Specialized Graph {graph_count}: No data points for this combination")

def main():
    """Main function to run the analysis"""
    print("🏠 Fixed Parameter Combination Analysis")
    print("=" * 50)
    
    # Load and filter data
    df = load_and_filter_data()
    
    if len(df) == 0:
        print("❌ No data found with weighted payment values")
        return
    
    print(f"\n📊 Data summary:")
    print(f"  • Total records: {len(df):,}")
    print(f"  • Available parameters: {list(df.columns)}")
    
    # Create fixed parameter graphs
    create_fixed_parameter_graphs(df)
    
    # Create specialized combinations
    create_specialized_combinations(df)
    
    print("\n✅ Fixed parameter analysis complete!")
    print("📁 All plots have been saved as HTML files and displayed in browser")

if __name__ == "__main__":
    main() 