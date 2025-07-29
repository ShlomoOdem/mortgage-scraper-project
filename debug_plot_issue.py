#!/usr/bin/env python3
"""
Debug script to test plot creation and identify issues
"""

import requests
import json
import pandas as pd

def test_simple_plot():
    """Test a simple plot without any fixed parameters"""
    
    test_data = {
        'x_param': 'Interest_Rate',
        'y_param': 'Weighted Monthly Payment (30 years)',
        'label_param': None,
        'fixed_params': {}
    }
    
    print("🧪 Testing simple plot (no fixed parameters)")
    print("=" * 50)
    
    try:
        response = requests.post(
            'http://localhost:5000/create_plot',
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Response received")
            print(f"   Success: {result.get('success')}")
            print(f"   Data points: {result.get('data_points', 0)}")
            print(f"   Title: {result.get('title', 'N/A')}")
            
            if result.get('success'):
                # Parse the plot JSON to check the data
                plot_data = json.loads(result['plot'])
                print(f"\n📊 Plot analysis:")
                print(f"   Number of traces: {len(plot_data['data'])}")
                
                for i, trace in enumerate(plot_data['data']):
                    print(f"   Trace {i}: {trace.get('name', 'Unknown')}")
                    print(f"     X values: {len(trace.get('x', []))}")
                    print(f"     Y values: {len(trace.get('y', []))}")
                    if trace.get('x') and trace.get('y'):
                        print(f"     X range: {min(trace['x'])} to {max(trace['x'])}")
                        print(f"     Y range: {min(trace['y']):.0f} to {max(trace['y']):.0f}")
            else:
                print(f"❌ Error: {result.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_fixed_parameter_plot():
    """Test a plot with fixed parameters"""
    
    test_data = {
        'x_param': 'Interest_Rate',
        'y_param': 'Weighted Monthly Payment (30 years)',
        'label_param': 'Inflation_Rate',
        'fixed_params': {
            'Term_Months': '360',
            'Amortization_Method': 'שפיצר'
        }
    }
    
    print("\n🧪 Testing plot with fixed parameters")
    print("=" * 50)
    
    try:
        response = requests.post(
            'http://localhost:5000/create_plot',
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Response received")
            print(f"   Success: {result.get('success')}")
            print(f"   Data points: {result.get('data_points', 0)}")
            print(f"   Title: {result.get('title', 'N/A')}")
            
            if result.get('success'):
                # Parse the plot JSON to check the data
                plot_data = json.loads(result['plot'])
                print(f"\n📊 Plot analysis:")
                print(f"   Number of traces: {len(plot_data['data'])}")
                
                for i, trace in enumerate(plot_data['data']):
                    print(f"   Trace {i}: {trace.get('name', 'Unknown')}")
                    print(f"     X values: {len(trace.get('x', []))}")
                    print(f"     Y values: {len(trace.get('y', []))}")
                    if trace.get('x') and trace.get('y'):
                        print(f"     X range: {min(trace['x'])} to {max(trace['x'])}")
                        print(f"     Y range: {min(trace['y']):.0f} to {max(trace['y']):.0f}")
            else:
                print(f"❌ Error: {result.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def check_data_source():
    """Check the data source directly"""
    
    print("\n📊 Checking data source")
    print("=" * 30)
    
    try:
        # Load the data directly
        df = pd.read_csv('data/analyzed/combined_summary_files.csv')
        
        # Check the columns
        print(f"Data shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        # Check for the specific columns we're using
        if 'Interest_Rate' in df.columns:
            print(f"\nInterest_Rate info:")
            print(f"   Unique values: {df['Interest_Rate'].nunique()}")
            print(f"   Range: {df['Interest_Rate'].min()} to {df['Interest_Rate'].max()}")
            print(f"   Sample values: {sorted(df['Interest_Rate'].unique())[:5]}")
        
        if 'Weighted Monthly Payment (30 years)' in df.columns:
            print(f"\nWeighted Monthly Payment info:")
            print(f"   Range: {df['Weighted Monthly Payment (30 years)'].min():.0f} to {df['Weighted Monthly Payment (30 years)'].max():.0f}")
            print(f"   Non-null count: {df['Weighted Monthly Payment (30 years)'].notna().sum()}")
        
        if 'Term_Months' in df.columns:
            print(f"\nTerm_Months info:")
            print(f"   Unique values: {sorted(df['Term_Months'].unique())}")
        
        if 'Amortization_Method' in df.columns:
            print(f"\nAmortization_Method info:")
            print(f"   Unique values: {df['Amortization_Method'].unique()}")
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")

if __name__ == "__main__":
    print("🔍 Debugging Plot Issues")
    print("=" * 50)
    
    check_data_source()
    test_simple_plot()
    test_fixed_parameter_plot()
    
    print("\n🎯 Next steps:")
    print("1. Open browser to: http://localhost:5000")
    print("2. Open browser developer console (F12)")
    print("3. Try creating a plot and check console output")
    print("4. Look for any error messages or warnings") 