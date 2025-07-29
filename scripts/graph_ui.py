#!/usr/bin/env python3
"""
Web-based UI for creating graphs from the combined summary data
Uses Flask and Plotly for interactive visualization
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from flask import Flask, render_template, request, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__, template_folder='../templates')

# Global variable to store the dataframe
df = None

def load_data():
    """Load the combined summary data"""
    global df
    try:
        file_path = "data/analyzed/combined_summary_files.csv"
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return False
        
        print("Loading data...")
        df = pd.read_csv(file_path)
        
        # Clean up numeric columns
        numeric_columns = ['Interest_Rate', 'Term_Months', 'Inflation_Rate', 'Loan Amount', 
                          'Total Monthly Payments', 'Total Mortgage Interest', 'Weighted Cost (should be ~0)']
        
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Clean up currency columns
        currency_columns = ['Monthly Income', 'Total Investment Amount', 'Total Investment Final Value',
                          'Total Investment Profit After Tax', 'Weighted Monthly Payment (30 years)',
                          'Weighted Investment Profit']
        
        for col in currency_columns:
            if col in df.columns:
                # Remove currency symbols and commas, convert to numeric
                df[col] = df[col].astype(str).str.replace('$', '').str.replace(',', '')
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Clean up percentage columns
        percentage_columns = ['Effective Annual Return After Tax']
        for col in percentage_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace('%', '')
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        print(f"Data loaded successfully: {len(df)} rows, {len(df.columns)} columns")
        return True
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return False

def get_column_info():
    """Get information about columns for the UI"""
    if df is None:
        return {}
    
    column_info = {}
    
    for col in df.columns:
        dtype = str(df[col].dtype)
        
        if dtype in ['int64', 'float64']:
            # Numeric column
            min_val = float(df[col].min()) if not df[col].isna().all() else 0
            max_val = float(df[col].max()) if not df[col].isna().all() else 100
            unique_count = df[col].nunique()
            
            column_info[col] = {
                'type': 'numeric',
                'min': min_val,
                'max': max_val,
                'unique_count': unique_count,
                'dtype': dtype
            }
        else:
            # String/categorical column
            unique_values = df[col].dropna().unique().tolist()
            column_info[col] = {
                'type': 'categorical',
                'unique_values': unique_values,
                'unique_count': len(unique_values),
                'dtype': dtype
            }
    
    return column_info

def create_filtered_dataframe(filters):
    """Create a filtered dataframe based on user selections"""
    if df is None:
        return None
    
    filtered_df = df.copy()
    
    for column, filter_config in filters.items():
        if column not in df.columns:
            continue
            
        if filter_config['type'] == 'range':
            min_val = filter_config.get('min')
            max_val = filter_config.get('max')
            
            if min_val is not None and max_val is not None:
                filtered_df = filtered_df[
                    (filtered_df[column] >= min_val) & 
                    (filtered_df[column] <= max_val)
                ]
        
        elif filter_config['type'] == 'values':
            selected_values = filter_config.get('values', [])
            if selected_values:
                filtered_df = filtered_df[filtered_df[column].isin(selected_values)]
    
    return filtered_df

def create_graph(x_col, y_col, color_col=None, size_col=None, graph_type='scatter', 
                filters=None, title=None):
    """Create a graph based on user selections"""
    
    filtered_df = create_filtered_dataframe(filters) if filters else df
    
    if filtered_df is None or filtered_df.empty:
        return None
    
    # Remove rows with NaN values in the selected columns
    columns_to_check = [x_col, y_col]
    if color_col:
        columns_to_check.append(color_col)
    if size_col:
        columns_to_check.append(size_col)
    
    filtered_df = filtered_df.dropna(subset=columns_to_check)
    
    if filtered_df.empty:
        return None
    
    # Create the graph based on type
    if graph_type == 'scatter':
        fig = px.scatter(
            filtered_df, 
            x=x_col, 
            y=y_col, 
            color=color_col,
            size=size_col,
            title=title or f"{y_col} vs {x_col}",
            hover_data=[x_col, y_col, color_col, size_col] if color_col and size_col else [x_col, y_col, color_col] if color_col else [x_col, y_col, size_col] if size_col else [x_col, y_col]
        )
    
    elif graph_type == 'line':
        # For line plots, we need to sort by x-axis
        filtered_df = filtered_df.sort_values(x_col)
        fig = px.line(
            filtered_df, 
            x=x_col, 
            y=y_col, 
            color=color_col,
            title=title or f"{y_col} vs {x_col}",
            hover_data=[x_col, y_col, color_col] if color_col else [x_col, y_col]
        )
    
    elif graph_type == 'bar':
        # For bar plots, we might want to aggregate data
        if color_col:
            # Group by x_col and color_col, aggregate y_col
            agg_df = filtered_df.groupby([x_col, color_col])[y_col].mean().reset_index()
            fig = px.bar(
                agg_df, 
                x=x_col, 
                y=y_col, 
                color=color_col,
                title=title or f"Average {y_col} by {x_col}",
                barmode='group'
            )
        else:
            # Group by x_col, aggregate y_col
            agg_df = filtered_df.groupby(x_col)[y_col].mean().reset_index()
            fig = px.bar(
                agg_df, 
                x=x_col, 
                y=y_col,
                title=title or f"Average {y_col} by {x_col}"
            )
    
    elif graph_type == 'histogram':
        fig = px.histogram(
            filtered_df, 
            x=x_col, 
            color=color_col,
            title=title or f"Distribution of {x_col}",
            nbins=30
        )
    
    elif graph_type == 'box':
        fig = px.box(
            filtered_df, 
            x=x_col, 
            y=y_col, 
            color=color_col,
            title=title or f"Box plot of {y_col} by {x_col}"
        )
    
    else:
        # Default to scatter
        fig = px.scatter(
            filtered_df, 
            x=x_col, 
            y=y_col, 
            color=color_col,
            title=title or f"{y_col} vs {x_col}"
        )
    
    # Update layout
    fig.update_layout(
        height=600,
        margin=dict(l=50, r=50, t=80, b=50),
        showlegend=True
    )
    
    return fig

@app.route('/')
def index():
    """Main page"""
    if df is None:
        if not load_data():
            return "Error: Could not load data file"
    
    column_info = get_column_info()
    
    return render_template('graph_ui.html', 
                         column_info=column_info,
                         total_rows=len(df) if df is not None else 0)

@app.route('/api/columns')
def get_columns():
    """API endpoint to get column information"""
    if df is None:
        return jsonify({'error': 'Data not loaded'})
    
    column_info = get_column_info()
    return jsonify(column_info)

@app.route('/api/graph', methods=['POST'])
def generate_graph():
    """API endpoint to generate graph"""
    try:
        data = request.get_json()
        
        x_col = data.get('x_column')
        y_col = data.get('y_column')
        color_col = data.get('color_column')
        size_col = data.get('size_column')
        graph_type = data.get('graph_type', 'scatter')
        filters = data.get('filters', {})
        title = data.get('title', '')
        
        if not x_col or not y_col:
            return jsonify({'error': 'X and Y columns are required'})
        
        fig = create_graph(x_col, y_col, color_col, size_col, graph_type, filters, title)
        
        if fig is None:
            return jsonify({'error': 'Could not create graph with selected data'})
        
        # Convert to JSON for frontend
        graph_json = fig.to_json()
        
        return jsonify({
            'success': True,
            'graph': graph_json,
            'data_points': len(fig.data[0].x) if fig.data else 0
        })
        
    except Exception as e:
        return jsonify({'error': f'Error generating graph: {str(e)}'})

@app.route('/api/sample_data')
def get_sample_data():
    """API endpoint to get sample data for preview"""
    if df is None:
        return jsonify({'error': 'Data not loaded'})
    
    sample_data = df.head(10).to_dict('records')
    return jsonify({'data': sample_data})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Load data on startup
    if load_data():
        print("Starting web server...")
        print("Open http://localhost:5000 in your browser")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("Failed to load data. Please check the file path.") 