#!/bin/bash

# Mortgage Data Graph Generator UI Launcher

echo "Starting Mortgage Data Graph Generator UI..."
echo "=========================================="

# Check if the data file exists
if [ ! -f "data/analyzed/combined_summary_files.csv" ]; then
    echo "Error: Combined summary file not found!"
    echo "Please run 'python3 scripts/combine_summary_files.py' first to create the data file."
    exit 1
fi

# Check if required packages are installed
echo "Checking dependencies..."
python3 -c "import flask, pandas, plotly" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required packages..."
    pip install flask pandas plotly numpy
fi

# Check if port 5000 is already in use
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null ; then
    echo "Warning: Port 5000 is already in use. Stopping existing processes..."
    pkill -f "python3 scripts/graph_ui.py"
    sleep 2
fi

# Start the web server
echo "Starting web server..."
echo "Open http://localhost:5000 in your browser"
echo "Press Ctrl+C to stop the server"
echo ""

python3 scripts/graph_ui.py 