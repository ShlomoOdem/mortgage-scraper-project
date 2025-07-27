#!/bin/bash

# Automated CP Programs Extractor Runner
# This script makes it easy to run the automated extraction

echo "Automated CP Programs Extractor"
echo "==============================="
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTION] [--no-headless]"
    echo ""
    echo "Options:"
    echo "  single     - Run single scenario with default values"
    echo "  batch      - Run predefined batch scenarios"
    echo "  config     - Run scenarios from scenarios_config.json"
    echo "  custom     - Run with custom configuration file"
    echo "  help       - Show this help message"
    echo ""
    echo "Flags:"
    echo "  --no-headless  - Run in visible mode (show browser)"
    echo ""
    echo "Examples:"
    echo "  $0 single"
    echo "  $0 single --no-headless"
    echo "  $0 batch"
    echo "  $0 batch --no-headless"
    echo "  $0 config"
    echo "  $0 custom my_scenarios.json"
    echo ""
}

# Function to run single scenario
run_single() {
    local headless_flag=""
    if [ "$1" = "--no-headless" ]; then
        headless_flag="--no-headless"
    fi
    
    echo "Running single scenario extraction..."
    echo ""
    python3 automated_cp_programs_extractor.py $headless_flag
}

# Function to run batch scenarios
run_batch() {
    local headless_flag=""
    if [ "$1" = "--no-headless" ]; then
        headless_flag="--no-headless"
    fi
    
    echo "Running batch scenarios..."
    echo ""
    python3 batch_cp_programs_extractor.py $headless_flag
}

# Function to run configurable scenarios
run_config() {
    local headless_flag=""
    if [ "$1" = "--no-headless" ]; then
        headless_flag="--no-headless"
    fi
    
    echo "Running configurable scenarios..."
    echo ""
    python3 configurable_batch_extractor.py $headless_flag
}

# Function to run custom configuration
run_custom() {
    local config_file=""
    local headless_flag=""
    
    # Parse arguments
    for arg in "$@"; do
        if [ "$arg" = "--no-headless" ]; then
            headless_flag="--no-headless"
        elif [ -z "$config_file" ]; then
            config_file="$arg"
        fi
    done
    
    if [ -z "$config_file" ]; then
        echo "Error: Please specify a configuration file"
        echo "Usage: $0 custom <config_file.json> [--no-headless]"
        exit 1
    fi
    
    if [ ! -f "$config_file" ]; then
        echo "Error: Configuration file '$config_file' not found"
        exit 1
    fi
    
    echo "Running custom scenarios from $config_file..."
    echo ""
    python3 configurable_batch_extractor.py $headless_flag "$config_file"
}

# Main script logic
case "$1" in
    "single")
        run_single "$2"
        ;;
    "batch")
        run_batch "$2"
        ;;
    "config")
        run_config "$2"
        ;;
    "custom")
        shift  # Remove the first argument (custom)
        run_custom "$@"
        ;;
    "help"|"-h"|"--help"|"")
        show_usage
        ;;
    *)
        echo "Error: Unknown option '$1'"
        echo ""
        show_usage
        exit 1
        ;;
esac

echo ""
echo "Script completed!" 