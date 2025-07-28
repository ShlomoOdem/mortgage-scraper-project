#!/bin/bash

# Comprehensive Status Monitor for Mortgage Analysis Processes
# Shows detailed progress of each running process and combination status

echo "🏠 MORTGAGE ANALYSIS STATUS MONITOR"
echo "==================================="
echo "Timestamp: $(date)"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Change to the project directory
cd "$PROJECT_DIR"

# Function to get process info
get_process_info() {
    local pid=$1
    local cmdline=$(ps -p $pid -o cmd= 2>/dev/null)
    local cpu=$(ps -p $pid -o %cpu= 2>/dev/null)
    local mem=$(ps -p $pid -o %mem= 2>/dev/null)
    local time=$(ps -p $pid -o etime= 2>/dev/null)
    
    echo "$cmdline|$cpu|$mem|$time"
}

# Function to extract combination file from command line
extract_combination_file() {
    local cmdline=$1
    echo "$cmdline" | grep -o 'combinations_[0-9]*\.json' | head -1
}

# Function to get progress from log file
get_log_progress() {
    local log_file=$1
    if [ ! -f "$log_file" ]; then
        echo "0|0|0|Log file not found"
        return
    fi
    
    # Get total lines in log
    local total_lines=$(wc -l < "$log_file" 2>/dev/null || echo "0")
    
    # Count "Processing combination" lines to get current progress
    local processed_count=$(grep -c "Processing combination" "$log_file" 2>/dev/null || echo "0")
    
    # Get the last processed combination number - look for pattern like "Processing combination 123/5000"
    local last_line=$(grep "Processing combination" "$log_file" | tail -1 2>/dev/null)
    local current_combination="0"
    local total_combinations="0"
    
    if [ ! -z "$last_line" ]; then
        # Extract numbers from "Processing combination 123/5000"
        current_combination=$(echo "$last_line" | grep -o '[0-9]*/[0-9]*' | cut -d'/' -f1 2>/dev/null || echo "0")
        total_combinations=$(echo "$last_line" | grep -o '[0-9]*/[0-9]*' | cut -d'/' -f2 2>/dev/null || echo "0")
    fi
    
    # Get last activity timestamp
    local last_activity=$(stat -c %Y "$log_file" 2>/dev/null || echo "0")
    local last_activity_str=$(date -d @$last_activity '+%H:%M:%S' 2>/dev/null || echo "Unknown")
    
    echo "$processed_count|$total_combinations|$current_combination|$last_activity_str"
}

# Function to calculate percentage
calculate_percentage() {
    local current=$1
    local total=$2
    if [ "$total" -eq 0 ]; then
        echo "0%"
    else
        local percentage=$((current * 100 / total))
        echo "${percentage}%"
    fi
}

# Function to format time
format_time() {
    local seconds=$1
    if [ "$seconds" -lt 60 ]; then
        echo "${seconds}s"
    elif [ "$seconds" -lt 3600 ]; then
        local minutes=$((seconds / 60))
        local remaining_seconds=$((seconds % 60))
        echo "${minutes}m ${remaining_seconds}s"
    else
        local hours=$((seconds / 3600))
        local minutes=$(((seconds % 3600) / 60))
        echo "${hours}h ${minutes}m"
    fi
}

# Check running processes
echo "📊 RUNNING PROCESSES:"
echo "===================="

RUNNING_PIDS=$(ps aux | grep "run_modular_workflow.py" | grep -v grep | awk '{print $2}')
TOTAL_PROCESSES=$(echo "$RUNNING_PIDS" | wc -l)

if [ -z "$RUNNING_PIDS" ]; then
    echo "❌ No processes are currently running"
    echo ""
    echo "💡 To start processing, run:"
    echo "  ./scripts/run_all_combinations_parallel_simple.sh"
    exit 0
fi

echo "✅ Found $TOTAL_PROCESSES running process(es)"
echo ""

# Process each running process
declare -A process_data
declare -A progress_data

for pid in $RUNNING_PIDS; do
    # Get process information
    process_info=$(get_process_info $pid)
    cmdline=$(echo "$process_info" | cut -d'|' -f1)
    cpu=$(echo "$process_info" | cut -d'|' -f2)
    mem=$(echo "$process_info" | cut -d'|' -f3)
    runtime=$(echo "$process_info" | cut -d'|' -f4)
    
    # Extract combination file
    combination_file=$(extract_combination_file "$cmdline")
    if [ -z "$combination_file" ]; then
        continue
    fi
    
    # Get progress from log file
    log_file="logs/${combination_file%.json}.log"
    progress_info=$(get_log_progress "$log_file")
    processed_count=$(echo "$progress_info" | cut -d'|' -f1)
    total_combinations=$(echo "$progress_info" | cut -d'|' -f2)
    current_combination=$(echo "$progress_info" | cut -d'|' -f3)
    last_activity=$(echo "$progress_info" | cut -d'|' -f4)
    
    # Store data for summary
    process_data["$pid"]="$combination_file|$cpu|$mem|$runtime"
    progress_data["$pid"]="$processed_count|$total_combinations|$current_combination|$last_activity"
done

# Display detailed process information
for pid in $RUNNING_PIDS; do
    if [ -z "${process_data[$pid]}" ]; then
        continue
    fi
    
    combination_file=$(echo "${process_data[$pid]}" | cut -d'|' -f1)
    cpu=$(echo "${process_data[$pid]}" | cut -d'|' -f2)
    mem=$(echo "${process_data[$pid]}" | cut -d'|' -f3)
    runtime=$(echo "${process_data[$pid]}" | cut -d'|' -f4)
    
    processed_count=$(echo "${progress_data[$pid]}" | cut -d'|' -f1)
    total_combinations=$(echo "${progress_data[$pid]}" | cut -d'|' -f2)
    current_combination=$(echo "${progress_data[$pid]}" | cut -d'|' -f3)
    last_activity=$(echo "${progress_data[$pid]}" | cut -d'|' -f4)
    
    # Calculate percentage
    percentage=$(calculate_percentage $processed_count $total_combinations)
    
    echo "🔄 Process $pid - $combination_file"
    echo "   📈 Progress: $processed_count/$total_combinations combinations ($percentage)"
    echo "   🎯 Current: Combination #$current_combination"
    echo "   ⏱️  Runtime: $runtime"
    echo "   💻 CPU: ${cpu}%, Memory: ${mem}%"
    echo "   🕐 Last Activity: $last_activity"
    echo ""
done

# Overall progress summary
echo "📈 OVERALL PROGRESS SUMMARY:"
echo "============================"

total_processed=0
total_combinations=0
completed_processes=0

for pid in $RUNNING_PIDS; do
    if [ -z "${progress_data[$pid]}" ]; then
        continue
    fi
    
    processed_count=$(echo "${progress_data[$pid]}" | cut -d'|' -f1)
    total_combinations=$(echo "${progress_data[$pid]}" | cut -d'|' -f2)
    
    # Convert to integers, defaulting to 0 if empty or invalid
    processed_count=$(echo "$processed_count" | tr -d ' ' | grep -E '^[0-9]+$' || echo "0")
    total_combinations=$(echo "$total_combinations" | tr -d ' ' | grep -E '^[0-9]+$' || echo "0")
    
    total_processed=$((total_processed + processed_count))
    total_combinations=$((total_combinations + total_combinations))
    
    if [ "$processed_count" -eq "$total_combinations" ] && [ "$total_combinations" -gt 0 ]; then
        completed_processes=$((completed_processes + 1))
    fi
done

if [ "$total_combinations" -gt 0 ]; then
    overall_percentage=$(calculate_percentage $total_processed $total_combinations)
    echo "✅ Completed Processes: $completed_processes/$TOTAL_PROCESSES"
    echo "📊 Total Progress: $total_processed/$total_combinations combinations ($overall_percentage)"
else
    echo "⏳ Calculating progress..."
fi

echo ""

# System resource usage
echo "💻 SYSTEM RESOURCES:"
echo "==================="

# Get overall CPU and memory usage
total_cpu=$(ps aux | grep "run_modular_workflow.py" | grep -v grep | awk '{sum += $3} END {print sum}')
total_mem=$(ps aux | grep "run_modular_workflow.py" | grep -v grep | awk '{sum += $4} END {print sum}')

echo "🖥️  Total CPU Usage: ${total_cpu}%"
echo "🧠 Total Memory Usage: ${total_mem}%"
echo ""

# Recent log activity
echo "📝 RECENT ACTIVITY:"
echo "=================="

# Show last few lines from each log file
for pid in $RUNNING_PIDS; do
    if [ -z "${process_data[$pid]}" ]; then
        continue
    fi
    
    combination_file=$(echo "${process_data[$pid]}" | cut -d'|' -f1)
    log_file="logs/${combination_file%.json}.log"
    
    if [ -f "$log_file" ]; then
        echo "📄 $combination_file:"
        last_line=$(tail -1 "$log_file" 2>/dev/null | cut -c1-100)
        if [ ! -z "$last_line" ]; then
            echo "   $last_line..."
        else
            echo "   No recent activity"
        fi
        echo ""
    fi
done

# Quick commands
echo "🔧 QUICK COMMANDS:"
echo "=================="
echo "  📊 View this status again: ./scripts/status_monitor.sh"
echo "  📈 View specific log: tail -f logs/combinations_001.log"
echo "  📋 View all logs: tail -f logs/*.log"
echo "  ⏹️  Stop all processes: pkill -f run_modular_workflow"
echo "  🔍 Check verification status: python3 run_modular_workflow.py --combination-file data/combinations_index.json --status"
echo ""

# Estimated completion time (if we have enough data)
if [ "$total_processed" -gt 0 ] && [ "$total_combinations" -gt 0 ]; then
    # Get the average runtime of processes
    avg_runtime_seconds=0
    process_count=0
    
    for pid in $RUNNING_PIDS; do
        if [ -z "${process_data[$pid]}" ]; then
            continue
        fi
        
        runtime=$(echo "${process_data[$pid]}" | cut -d'|' -f4)
        # Convert runtime to seconds (simple estimation)
        if [[ "$runtime" =~ ([0-9]+)h ]]; then
            hours=${BASH_REMATCH[1]}
            avg_runtime_seconds=$((avg_runtime_seconds + hours * 3600))
        elif [[ "$runtime" =~ ([0-9]+)m ]]; then
            minutes=${BASH_REMATCH[1]}
            avg_runtime_seconds=$((avg_runtime_seconds + minutes * 60))
        fi
        process_count=$((process_count + 1))
    done
    
    if [ "$process_count" -gt 0 ]; then
        avg_runtime_seconds=$((avg_runtime_seconds / process_count))
        remaining_combinations=$((total_combinations - total_processed))
        estimated_remaining_time=$((remaining_combinations * avg_runtime_seconds / total_processed))
        
        echo "⏰ ESTIMATED COMPLETION:"
        echo "======================="
        echo "   🕐 Estimated remaining time: $(format_time $estimated_remaining_time)"
        echo "   📅 Estimated completion: $(date -d "+$estimated_remaining_time seconds" '+%Y-%m-%d %H:%M:%S')"
        echo ""
    fi
fi

echo "🔄 Auto-refresh: Run this script again to see updated progress" 