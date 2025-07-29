#!/bin/bash

# Interactive Mortgage Plot UI Launcher
echo "🏠 Interactive Mortgage Plot UI"
echo "=============================="

# Check if required files exist
if [ ! -f "data/analyzed/combined_summary_files.csv" ]; then
    echo "❌ Error: Data file not found!"
    echo "Please run the analysis first:"
    echo "  python3 scripts/plot_clean_fixed_combinations.py"
    exit 1
fi

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 Installing required dependencies..."
    pip3 install -r requirements_ui.txt
fi

echo "🚀 Starting Interactive Plot UI..."
echo "📊 Loading mortgage data..."
echo "🌐 Opening browser..."

# Start the server
python3 scripts/interactive_plot_ui.py &

# Wait a moment for the server to start
sleep 3

# Try to open the browser
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:5000
elif command -v open &> /dev/null; then
    open http://localhost:5000
else
    echo "🌐 Please open your browser and go to: http://localhost:5000"
fi

echo ""
echo "✅ Interactive UI is running!"
echo "📊 You can now:"
echo "   • Choose X-axis parameter (Interest_Rate, Term_Months, etc.)"
echo "   • Choose Y-axis parameter (default: Weighted Monthly Payment)"
echo "   • Choose Label parameter (optional, for different colors)"
echo "   • Add Fixed Parameters (to filter data)"
echo "   • Click 'Create Plot' to generate interactive visualizations"
echo ""
echo "🛑 To stop the server, press Ctrl+C"

# Wait for user to stop
wait 