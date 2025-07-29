#!/usr/bin/env python3
"""
Script to plot weighted monthly payment vs interest rate for 360-month loans with שפיצר amortization.
Each loan type will be plotted as a separate line on the same figure.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import os

def load_and_filter_data():
    """Load the combined data and filter for 360-month loans with שפיצר amortization"""
    print("📂 Loading mortgage data...")
    
    # Load the combined data
    df = pd.read_csv('data/analyzed/combined_summary_files.csv')
    print(f"✅ Data loaded: {len(df):,} total rows")
    
    # Show data availability
    print("\n📊 Data Availability:")
    print(f"  • Records with שפיצר amortization: {len(df[df['Amortization_Method'] == 'שפיצר']):,}")
    print(f"  • Records with 360-month term: {len(df[df['Term_Months'] == 360]):,}")
    print(f"  • Records with both 360-month and שפיצר: {len(df[(df['Term_Months'] == 360) & (df['Amortization_Method'] == 'שפיצר')]):,}")
    
    # Filter for 360-month loans with שפיצר amortization
    filtered_df = df[
        (df['Term_Months'] == 360) & 
        (df['Amortization_Method'] == 'שפיצר')
    ].copy()
    
    print(f"\n📊 Filtered data: {len(filtered_df):,} rows (360-month, שפיצר amortization)")
    
    # Convert numeric columns
    numeric_columns = ['Interest_Rate', 'Inflation_Rate']
    for col in numeric_columns:
        if col in filtered_df.columns:
            filtered_df[col] = pd.to_numeric(filtered_df[col], errors='coerce')
    
    # Handle weighted payment column separately (it has commas)
    if 'Weighted Monthly Payment (30 years)' in filtered_df.columns:
        # Remove commas and convert to numeric
        filtered_df['Weighted Monthly Payment (30 years)'] = filtered_df['Weighted Monthly Payment (30 years)'].str.replace(',', '').astype(float)
    
    # Remove rows with missing weighted payment data
    original_count = len(filtered_df)
    filtered_df = filtered_df[filtered_df['Weighted Monthly Payment (30 years)'].notna()]
    print(f"📊 After removing missing weighted payment data: {len(filtered_df):,} rows (removed {original_count - len(filtered_df):,} rows)")
    
    return filtered_df

def create_weighted_payment_plot(df):
    """Create a plot of weighted monthly payment vs interest rate by loan type"""
    
    # Get unique loan types (channels)
    loan_types = df['Channel'].unique()
    print(f"🏦 Loan types found: {list(loan_types)}")
    
    # Create the plot
    fig = go.Figure()
    
    # Colors for different loan types
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    for i, loan_type in enumerate(loan_types):
        # Filter data for this loan type
        loan_data = df[df['Channel'] == loan_type].copy()
        
        if len(loan_data) > 0:
            # Sort by interest rate for better line visualization
            loan_data = loan_data.sort_values('Interest_Rate')
            
            # Add line for this loan type
            fig.add_trace(
                go.Scatter(
                    x=loan_data['Interest_Rate'],
                    y=loan_data['Weighted Monthly Payment (30 years)'],
                    mode='lines+markers',
                    name=loan_type,
                    line=dict(color=colors[i % len(colors)], width=3),
                    marker=dict(size=8),
                    hovertemplate=f'<b>{loan_type}</b><br>' +
                                'Interest Rate: %{x:.2f}%<br>' +
                                'Weighted Payment: %{y:,.0f} NIS<br>' +
                                'Term: 360 months<br>' +
                                '<extra></extra>'
                )
            )
            
            print(f"  📈 {loan_type}: {len(loan_data)} data points")
    
    # Update layout
    fig.update_layout(
        title={
            'text': 'Weighted Monthly Payment vs Interest Rate<br><sub>360-Month Loans with שפיצר Amortization</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        xaxis_title='Interest Rate (%)',
        yaxis_title='Weighted Monthly Payment (NIS)',
        xaxis=dict(
            gridcolor='lightgray',
            zeroline=False,
            showgrid=True
        ),
        yaxis=dict(
            gridcolor='lightgray',
            zeroline=False,
            showgrid=True
        ),
        plot_bgcolor='white',
        width=1000,
        height=600,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode='closest'
    )
    
    return fig

def create_additional_analysis(df):
    """Create additional analysis plots"""
    
    # Create subplots for additional analysis
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Weighted Payment Distribution by Loan Type',
            'Interest Rate Distribution by Loan Type', 
            'Weighted Payment vs Inflation Rate',
            'Investment Profit vs Interest Rate'
        ),
        specs=[[{"type": "box"}, {"type": "box"}],
               [{"type": "scatter"}, {"type": "scatter"}]]
    )
    
    # 1. Weighted Payment Distribution by Loan Type
    for loan_type in df['Channel'].unique():
        loan_data = df[df['Channel'] == loan_type]['Weighted Monthly Payment (30 years)']
        fig.add_trace(
            go.Box(y=loan_data, name=loan_type, showlegend=False),
            row=1, col=1
        )
    
    # 2. Interest Rate Distribution by Loan Type
    for loan_type in df['Channel'].unique():
        loan_data = df[df['Channel'] == loan_type]['Interest_Rate']
        fig.add_trace(
            go.Box(y=loan_data, name=loan_type, showlegend=False),
            row=1, col=2
        )
    
    # 3. Weighted Payment vs Inflation Rate
    fig.add_trace(
        go.Scatter(
            x=df['Inflation_Rate'],
            y=df['Weighted Monthly Payment (30 years)'],
            mode='markers',
            marker=dict(
                color=df['Interest_Rate'],
                colorscale='Viridis',
                size=8,
                colorbar=dict(title="Interest Rate (%)")
            ),
            text=df['Channel'],
            hovertemplate='<b>%{text}</b><br>' +
                        'Inflation: %{x:.1f}%<br>' +
                        'Weighted Payment: %{y:,.0f} NIS<br>' +
                        'Interest Rate: %{marker.color:.2f}%<br>' +
                        '<extra></extra>',
            name='Weighted Payment vs Inflation',
            showlegend=False
        ),
        row=2, col=1
    )
    
    # 4. Investment Profit vs Interest Rate
    if 'Total Investment Profit After Tax' in df.columns:
        # Handle investment profit column (it might have commas)
        if df['Total Investment Profit After Tax'].dtype == 'object':
            df['Total Investment Profit After Tax'] = df['Total Investment Profit After Tax'].str.replace(',', '').astype(float)
        
        fig.add_trace(
            go.Scatter(
                x=df['Interest_Rate'],
                y=df['Total Investment Profit After Tax'],
                mode='markers',
                marker=dict(
                    color=df['Inflation_Rate'],
                    colorscale='Plasma',
                    size=8,
                    colorbar=dict(title="Inflation Rate (%)")
                ),
                text=df['Channel'],
                hovertemplate='<b>%{text}</b><br>' +
                            'Interest Rate: %{x:.2f}%<br>' +
                            'Investment Profit: %{y:,.0f} NIS<br>' +
                            'Inflation Rate: %{marker.color:.1f}%<br>' +
                            '<extra></extra>',
                name='Investment Profit vs Interest Rate',
                showlegend=False
            ),
            row=2, col=2
        )
    
    # Update layout
    fig.update_layout(
        title={
            'text': 'Additional Analysis: 360-Month Loans with שפיצר Amortization',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        height=800,
        showlegend=False
    )
    
    # Update axes labels
    fig.update_xaxes(title_text="Loan Type", row=1, col=1)
    fig.update_yaxes(title_text="Weighted Monthly Payment (NIS)", row=1, col=1)
    fig.update_xaxes(title_text="Loan Type", row=1, col=2)
    fig.update_yaxes(title_text="Interest Rate (%)", row=1, col=2)
    fig.update_xaxes(title_text="Inflation Rate (%)", row=2, col=1)
    fig.update_yaxes(title_text="Weighted Monthly Payment (NIS)", row=2, col=1)
    fig.update_xaxes(title_text="Interest Rate (%)", row=2, col=2)
    fig.update_yaxes(title_text="Investment Profit After Tax (NIS)", row=2, col=2)
    
    return fig

def print_statistics(df):
    """Print key statistics for the filtered data"""
    print("\n📊 Key Statistics:")
    print("=" * 50)
    
    print(f"Total filtered records: {len(df):,}")
    print(f"Loan types: {len(df['Channel'].unique())}")
    print(f"Interest rate range: {df['Interest_Rate'].min():.2f}% - {df['Interest_Rate'].max():.2f}%")
    print(f"Weighted payment range: {df['Weighted Monthly Payment (30 years)'].min():,.0f} - {df['Weighted Monthly Payment (30 years)'].max():,.0f} NIS")
    print(f"All loans are 360-month terms")
    
    print("\n📈 By Loan Type:")
    for loan_type in df['Channel'].unique():
        loan_data = df[df['Channel'] == loan_type]
        print(f"  {loan_type}:")
        print(f"    Count: {len(loan_data):,}")
        print(f"    Avg Interest Rate: {loan_data['Interest_Rate'].mean():.2f}%")
        print(f"    Avg Weighted Payment: {loan_data['Weighted Monthly Payment (30 years)'].mean():,.0f} NIS")
        print(f"    Min Weighted Payment: {loan_data['Weighted Monthly Payment (30 years)'].min():,.0f} NIS")
        print(f"    Max Weighted Payment: {loan_data['Weighted Monthly Payment (30 years)'].max():,.0f} NIS")
        print()

def main():
    """Main function to run the analysis"""
    print("🏠 360-Month Mortgage Weighted Payment Analysis")
    print("=" * 60)
    
    # Load and filter data
    df = load_and_filter_data()
    
    if len(df) == 0:
        print("❌ No data found matching the criteria (360-month, שפיצר amortization)")
        print("💡 Try running the general analysis script instead:")
        print("   python3 scripts/plot_weighted_payment_analysis.py")
        return
    
    # Print statistics
    print_statistics(df)
    
    # Create main plot
    print("\n📊 Creating weighted payment vs interest rate plot...")
    main_fig = create_weighted_payment_plot(df)
    
    # Save the plot
    output_file = "360_month_weighted_payment_analysis.html"
    main_fig.write_html(output_file)
    print(f"✅ Main plot saved to: {output_file}")
    
    # Create additional analysis
    print("\n📊 Creating additional analysis plots...")
    analysis_fig = create_additional_analysis(df)
    
    # Save additional analysis
    analysis_file = "360_month_additional_analysis.html"
    analysis_fig.write_html(analysis_file)
    print(f"✅ Additional analysis saved to: {analysis_file}")
    
    # Show the plots
    print("\n🎯 Displaying plots...")
    main_fig.show()
    analysis_fig.show()
    
    print("\n✅ Analysis complete!")
    print(f"📁 Files created:")
    print(f"  • {output_file} - Main 360-month weighted payment analysis")
    print(f"  • {analysis_file} - Additional 360-month analysis plots")

if __name__ == "__main__":
    main() 