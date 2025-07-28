#!/bin/bash

# Simple script to run all combination files in parallel in the background
# This script will find all combinations_*.json files and run them in parallel

echo "Starting parallel execution of all combination files in background..."
echo "=================================================================="

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Change to the project directory
cd "$PROJECT_DIR"

echo "Project directory: $PROJECT_DIR"
echo ""

# Find all combination files (excluding the index file)
COMBINATION_FILES=$(ls data/combinations_*.json 2>/dev/null | grep -v "index" | sort)

if [ -z "$COMBINATION_FILES" ]; then
    echo "❌ No combination files found in data/ directory!"
    echo "Please run the combination generator first:"
    echo "  python3 scripts/generate_combinations.py"
    exit 1
fi

# Count the files
FILE_COUNT=$(echo "$COMBINATION_FILES" | wc -l)
echo "Found $FILE_COUNT combination file(s):"
echo "$COMBINATION_FILES" | sed 's/^/  /'
echo ""

echo "🚀 Starting parallel execution in background..."
echo "Each file will run in the background."
echo "You can monitor progress with: ps aux | grep run_modular_workflow"
echo ""

# Function to run a single combination file
run_combination_file() {
    local file="$1"
    local filename=$(basename "$file")
    local log_file="logs/${filename%.json}.log"
    
    # Create logs directory if it doesn't exist
    mkdir -p logs
    
    echo "Starting: $filename (log: $log_file)"
    
    # Run the command in background and redirect output to log file
    python3 run_modular_workflow.py --full --combination-file "$file" --combinations 0 > "$log_file" 2>&1 &
    
    local pid=$!
    echo "✅ Started: $filename (PID: $pid)"
    
    # Save PID to a file for later reference
    echo "$pid" > "logs/${filename%.json}.pid"
}

# Run each file in parallel
for file in $COMBINATION_FILES; do
    run_combination_file "$file"
    # Small delay to prevent overwhelming the system
    sleep 2
done

echo ""
echo "🎉 All combination files have been started in background!"
echo ""
echo "📊 Summary:"
echo "  - Total files: $FILE_COUNT"
echo "  - Each running in background"
echo "  - Log files saved to: logs/"
echo "  - PID files saved to: logs/"
echo ""
echo "💡 Monitoring Commands:"
echo "  - Check running processes: ps aux | grep run_modular_workflow"
echo "  - Check logs: tail -f logs/combinations_001.log"
echo "  - Check all logs: tail -f logs/*.log"
echo "  - Kill all processes: pkill -f run_modular_workflow"
echo ""
echo "🔍 To check progress later, you can run:"
echo "  python3 run_modular_workflow.py --combination-file data/combinations_index.json --status" 