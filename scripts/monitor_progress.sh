#!/bin/bash

# Script to monitor the progress of all running mortgage analysis processes

echo "Monitoring Mortgage Analysis Progress"
echo "===================================="
echo ""

# Check running processes
echo "📊 RUNNING PROCESSES:"
echo "===================="
RUNNING_PROCESSES=$(ps aux | grep "run_modular_workflow.py" | grep -v grep)
if [ -z "$RUNNING_PROCESSES" ]; then
    echo "❌ No processes are currently running"
else
    echo "$RUNNING_PROCESSES" | while read line; do
        echo "✅ $line"
    done
fi

echo ""
echo "📈 LOG FILES STATUS:"
echo "==================="

# Check log files
if [ -d "logs" ]; then
    for log_file in logs/combinations_*.log; do
        if [ -f "$log_file" ]; then
            filename=$(basename "$log_file")
            size=$(du -h "$log_file" | cut -f1)
            lines=$(wc -l < "$log_file")
            last_line=$(tail -1 "$log_file" 2>/dev/null | cut -c1-80)
            
            echo "📄 $filename:"
            echo "   Size: $size, Lines: $lines"
            if [ ! -z "$last_line" ]; then
                echo "   Last: $last_line..."
            fi
            echo ""
        fi
    done
else
    echo "❌ No logs directory found"
fi

echo "🔍 QUICK COMMANDS:"
echo "=================="
echo "  - View all logs: tail -f logs/*.log"
echo "  - View specific log: tail -f logs/combinations_001.log"
echo "  - Check processes: ps aux | grep run_modular_workflow"
echo "  - Kill all processes: pkill -f run_modular_workflow"
echo "  - Check status: python3 run_modular_workflow.py --combination-file data/combinations_index.json --status"
echo "" 