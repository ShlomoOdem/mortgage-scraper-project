#!/usr/bin/env python3
"""
Interactive Plot UI
A web-based interface for creating custom mortgage parameter plots
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from flask import Flask, render_template, request, jsonify
import numpy as np
import os
import json
from datetime import datetime

# Set the template folder to the project's templates directory
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)

# Global variable to store the data
df = None

def load_data():
    """Load and prepare the mortgage data"""
    global df
    
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
    df = df[available_columns].copy()
    
    print(f"📊 Filtered data: {len(df):,} rows with {len(available_columns)} parameters")
    
    # Convert numeric columns
    numeric_columns = ['Weighted Monthly Payment (30 years)', 'Term_Months', 'Inflation_Rate', 'Interest_Rate']
    for col in numeric_columns:
        if col in df.columns:
            if col == 'Weighted Monthly Payment (30 years)':
                # Handle comma-separated numbers and convert to float
                df[col] = df[col].astype(str).str.replace(',', '').str.replace('NIS', '').str.strip()
                df[col] = pd.to_numeric(df[col], errors='coerce')
            else:
                df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Remove rows with missing weighted payment data
    original_count = len(df)
    df = df[df['Weighted Monthly Payment (30 years)'].notna()]
    print(f"📊 After removing missing weighted payment data: {len(df):,} rows")
    
    # Additional filtering for better data quality
    q1 = df['Weighted Monthly Payment (30 years)'].quantile(0.01)
    q3 = df['Weighted Monthly Payment (30 years)'].quantile(0.99)
    df = df[
        (df['Weighted Monthly Payment (30 years)'] >= q1) &
        (df['Weighted Monthly Payment (30 years)'] <= q3)
    ]
    print(f"📊 After removing outliers: {len(df):,} rows")
    
    # Reset index to avoid alignment issues
    df = df.reset_index(drop=True)
    
    return df

def get_parameter_info(df):
    """Get information about available parameters"""
    param_info = {}
    
    for col in df.columns:
        if col in ['Term_Months', 'Inflation_Rate', 'Interest_Rate']:
            # Numeric parameters
            values = sorted(df[col].unique())
            # Convert numpy types to Python native types
            values = [float(v) if isinstance(v, (np.integer, np.floating)) else v for v in values]
            param_info[col] = {
                'type': 'numeric',
                'values': values,
                'min': float(min(values)),
                'max': float(max(values)),
                'sample_values': [float(v) if isinstance(v, (np.integer, np.floating)) else v for v in values[:5]] if len(values) > 5 else [float(v) if isinstance(v, (np.integer, np.floating)) else v for v in values]
            }
        else:
            # Categorical parameters
            values = df[col].unique().tolist()
            param_info[col] = {
                'type': 'categorical',
                'values': values,
                'sample_values': values[:5] if len(values) > 5 else values
            }
    
    return param_info

@app.route('/')
def index():
    """Main page with the interactive UI"""
    global df
    
    if df is None:
        df = load_data()
    
    param_info = get_parameter_info(df)
    
    return render_template('interactive_plot_ui.html', 
                         param_info=param_info,
                         data_summary={
                             'total_records': len(df),
                             'weighted_payment_range': f"{df['Weighted Monthly Payment (30 years)'].min():,.0f} - {df['Weighted Monthly Payment (30 years)'].max():,.0f} NIS"
                         })

@app.route('/get_parameter_values')
def get_parameter_values():
    """API endpoint to get values for a specific parameter"""
    global df
    
    param = request.args.get('parameter')
    if param and param in df.columns:
        values = df[param].unique()
        if param in ['Term_Months', 'Inflation_Rate', 'Interest_Rate']:
            values = sorted(values)
            # Convert numpy types to Python native types
            values = [float(v) if isinstance(v, (np.integer, np.floating)) else v for v in values]
        else:
            # For categorical parameters, convert to list
            values = values.tolist()
        
        return jsonify({
            'parameter': param,
            'values': values,
            'type': 'numeric' if param in ['Term_Months', 'Inflation_Rate', 'Interest_Rate'] else 'categorical'
        })
    
    return jsonify({'error': 'Parameter not found'})

@app.route('/create_plot', methods=['POST'])
def create_plot():
    """API endpoint to create a plot based on user selections"""
    global df
    
    try:
        data = request.get_json()
        
        x_param = data.get('x_param')
        y_param = data.get('y_param', 'Weighted Monthly Payment (30 years)')
        label_param = data.get('label_param')
        fixed_params = data.get('fixed_params', {})
        
        print(f"🔍 Creating plot with parameters:")
        print(f"   X: {x_param}")
        print(f"   Y: {y_param}")
        print(f"   Label: {label_param}")
        print(f"   Fixed: {fixed_params}")
        
        # Validate parameters
        if not x_param or x_param not in df.columns:
            return jsonify({'error': 'Invalid x parameter'})
        
        if y_param not in df.columns:
            return jsonify({'error': 'Invalid y parameter'})
        
        if label_param and label_param not in df.columns:
            return jsonify({'error': 'Invalid label parameter'})
        
        # Create filter mask
        mask = pd.Series([True] * len(df), index=df.index)
        fixed_param_dict = {}
        
        for param, value in fixed_params.items():
            if param in df.columns:
                # Convert value to appropriate type
                if param in ['Term_Months', 'Inflation_Rate', 'Interest_Rate']:
                    try:
                        value = float(value)
                    except (ValueError, TypeError):
                        return jsonify({'error': f'Invalid numeric value for {param}: {value}'})
                    
                    # For numeric parameters, use tolerance
                    if param == 'Term_Months':
                        tolerance = 24  # ±24 months
                    elif param == 'Inflation_Rate':
                        tolerance = 1.0  # ±1.0%
                    else:  # Interest_Rate
                        tolerance = 0.5  # ±0.5%
                    
                    param_mask = (df[param] >= value - tolerance) & (df[param] <= value + tolerance)
                    print(f"   Filtering {param}: {value} ± {tolerance} -> {param_mask.sum()} matches")
                else:
                    # For categorical parameters, exact match
                    param_mask = df[param] == value
                    print(f"   Filtering {param}: {value} -> {param_mask.sum()} matches")
                
                mask = mask & param_mask
                fixed_param_dict[param] = value
        
        # Filter data
        subset = df[mask].copy()  # Use .copy() to avoid the warning
        
        print(f"📊 Final data subset: {len(subset)} points")
        
        if len(subset) == 0:
            return jsonify({'error': 'No data points found for the selected parameters'})
        
        # Check for valid data in x and y columns
        subset = subset.dropna(subset=[x_param, y_param])
        print(f"📊 After removing NaN values: {len(subset)} points")
        
        if len(subset) == 0:
            return jsonify({'error': 'No valid data points after removing NaN values'})
        
        # Create the plot
        fig = go.Figure()
        
        if label_param:
            # Create traces for each label value
            label_values = subset[label_param].unique()
            print(f"📊 Label values: {label_values}")
            
            for label_value in label_values:
                label_subset = subset[subset[label_param] == label_value]
                
                if len(label_subset) > 0:
                    # Sort by x parameter for better visualization
                    label_subset = label_subset.sort_values(x_param)
                    
                    print(f"📊 Creating trace for {label_param}={label_value}: {len(label_subset)} points")
                    print(f"   X range: {label_subset[x_param].min()} to {label_subset[x_param].max()}")
                    print(f"   Y range: {label_subset[y_param].min():.0f} to {label_subset[y_param].max():.0f}")
                    
                    # Create hover text with all parameter values
                    hover_texts = []
                    for _, row in label_subset.iterrows():
                        hover_text = f"<b>{label_param}: {row[label_param]}</b><br>"
                        hover_text += f"{x_param}: {row[x_param]}<br>"
                        hover_text += f"{y_param}: {row[y_param]:,.0f} NIS<br>"
                        
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
                            y=label_subset[y_param],
                            mode='markers',
                            name=f'{label_param}={label_value}',
                            marker=dict(size=8),
                            hovertemplate='%{text}',
                            text=hover_texts
                        )
                    )
        else:
            # No label parameter, create single trace
            subset = subset.sort_values(x_param)
            
            print(f"📊 Creating single trace: {len(subset)} points")
            print(f"   X range: {subset[x_param].min()} to {subset[x_param].max()}")
            print(f"   Y range: {subset[y_param].min():.0f} to {subset[y_param].max():.0f}")
            
            # Create hover text
            hover_texts = []
            for _, row in subset.iterrows():
                hover_text = f"{x_param}: {row[x_param]}<br>"
                hover_text += f"{y_param}: {row[y_param]:,.0f} NIS<br>"
                
                # Add all fixed parameters
                for param, value in fixed_param_dict.items():
                    hover_text += f"{param}: {value}<br>"
                
                # Add any other available parameters
                for col in df.columns:
                    if col not in [x_param, y_param] and col not in fixed_param_dict:
                        hover_text += f"{col}: {row[col]}<br>"
                
                hover_text += "<extra></extra>"
                hover_texts.append(hover_text)
            
            fig.add_trace(
                go.Scatter(
                    x=subset[x_param],
                    y=subset[y_param],
                    mode='markers',
                    name='Data Points',
                    marker=dict(size=8),
                    hovertemplate='%{text}',
                    text=hover_texts
                )
            )
        
        # Create title
        title = f"{x_param} vs {y_param}"
        if label_param:
            title += f" (labeled by {label_param})"
        
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
            yaxis_title=y_param,
            width=800,
            height=500,
            showlegend=True
        )
        
        # Convert to JSON for frontend
        plot_json = fig.to_json()
        
        print(f"✅ Plot created successfully with {len(subset)} data points")
        
        return jsonify({
            'success': True,
            'plot': plot_json,
            'data_points': len(subset),
            'title': title
        })
        
    except Exception as e:
        print(f"❌ Error creating plot: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Error creating plot: {str(e)}'})

@app.route('/get_data_summary')
def get_data_summary():
    """API endpoint to get data summary"""
    global df
    
    if df is None:
        df = load_data()
    
    param_info = get_parameter_info(df)
    
    return jsonify({
        'total_records': len(df),
        'parameters': list(df.columns),
        'param_info': param_info,
        'weighted_payment_range': {
            'min': float(df['Weighted Monthly Payment (30 years)'].min()),
            'max': float(df['Weighted Monthly Payment (30 years)'].max())
        }
    })

if __name__ == '__main__':
    # Load data on startup
    df = load_data()
    
    print("🚀 Starting Interactive Plot UI...")
    print("📊 Data loaded successfully!")
    print("🌐 Open your browser and go to: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 