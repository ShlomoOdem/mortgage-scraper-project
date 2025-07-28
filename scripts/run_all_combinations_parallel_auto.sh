#!/bin/bash

# Automatic script to run all combination files in parallel, each in its own terminal window
# This script will find all combinations_*.json files and run them in parallel without confirmation

# Cleanup function to remove temporary scripts
cleanup() {
    echo "🧹 Cleaning up temporary scripts..."
    rm -f /tmp/mortgage_analysis_*.sh
}

# Set trap to cleanup on exit
trap cleanup EXIT

echo "Starting automatic parallel execution of all combination files..."
echo "=============================================================="

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

echo "🚀 Starting automatic parallel execution..."
echo "Each file will run in its own terminal window."
echo ""

# Function to run a single combination file
run_combination_file() {
    local file="$1"
    local filename=$(basename "$file")
    
    echo "Starting: $filename"
    
    # Create a temporary script for this combination
    local temp_script="/tmp/mortgage_analysis_${filename%.json}.sh"
    cat > "$temp_script" << EOF
#!/bin/bash
cd "$PROJECT_DIR"
echo "=========================================="
echo "🏠 MORTGAGE ANALYSIS: $filename"
echo "=========================================="
echo "Starting at: \$(date)"
echo "Working directory: \$(pwd)"
echo "Command: python3 run_modular_workflow.py --full --combination-file '$file' --combinations 0"
echo "=========================================="
echo ""

# Run the command and capture exit code
python3 run_modular_workflow.py --full --combination-file "$file" --combinations 0
exit_code=\$?

echo ""
echo "=========================================="
echo "🏁 ANALYSIS COMPLETED: $filename"
echo "Exit code: \$exit_code"
echo "Completed at: \$(date)"
echo "=========================================="

if [ \$exit_code -eq 0 ]; then
    echo "✅ SUCCESS: Analysis completed successfully!"
else
    echo "❌ ERROR: Analysis failed with exit code \$exit_code"
fi

echo ""
echo "Press Enter to close this terminal..."
read
EOF
    
    chmod +x "$temp_script"
    
    # Use tilix for Ubuntu/Debian systems
    if command -v tilix &> /dev/null; then
        tilix -t "Mortgage Analysis: $filename" \
              -w "$PROJECT_DIR" \
              -e "bash '$temp_script'" &
    
    # Use gnome-terminal for Ubuntu/Debian systems
    elif command -v gnome-terminal &> /dev/null; then
        gnome-terminal --title="Mortgage Analysis: $filename" \
                      -- bash -c "bash '$temp_script'" &
    
    # Use xterm for other systems
    elif command -v xterm &> /dev/null; then
        xterm -title "Mortgage Analysis: $filename" \
              -e "bash '$temp_script'" &
    
    # Use konsole for KDE systems
    elif command -v konsole &> /dev/null; then
        konsole --title "Mortgage Analysis: $filename" \
                -e bash -c "bash '$temp_script'" &
    
    # Use terminator
    elif command -v terminator &> /dev/null; then
        terminator --title="Mortgage Analysis: $filename" \
                   -e "bash '$temp_script'" &
    
    # Use alacritty
    elif command -v alacritty &> /dev/null; then
        alacritty --title "Mortgage Analysis: $filename" \
                  -e bash -c "bash '$temp_script'" &
    
    # Fallback to default terminal
    else
        echo "❌ No suitable terminal emulator found (tilix, gnome-terminal, xterm, konsole, terminator, or alacritty)"
        echo "Please install one of these terminal emulators or run manually:"
        echo "  python3 run_modular_workflow.py --full --combination-file '$file' --combinations 0"
        rm -f "$temp_script"
        return 1
    fi
    
    echo "✅ Started: $filename (script: $temp_script)"
}

# Run each file in parallel
for file in $COMBINATION_FILES; do
    run_combination_file "$file"
    # Small delay to prevent overwhelming the system
    sleep 60
done

echo ""
echo "🎉 All combination files have been started automatically!"
echo ""
echo "📊 Summary:"
echo "  - Total files: $FILE_COUNT"
echo "  - Each running in its own terminal window"
echo "  - Command: python3 run_modular_workflow.py --full --combination-file <file> --combinations 0"
echo ""
echo "💡 Tips:"
echo "  - Each terminal will show the progress for its specific file"
echo "  - You can monitor multiple terminals simultaneously"
echo "  - Files will be saved to data/raw/ and data/analyzed/ directories"
echo "  - The process will continue even if you close this script"
echo ""
echo "🔍 To check progress later, you can run:"
echo "  python3 run_modular_workflow.py --combination-file data/combinations_index.json --status" 