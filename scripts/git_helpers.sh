#!/bin/bash

# Git helper script for mortgage scraper project

echo "=== Mortgage Scraper Git Helper ==="
echo "1. Check status"
echo "2. Add all changes"
echo "3. Commit changes"
echo "4. View log"
echo "5. Create new branch"
echo "6. Switch branch"
echo "7. Merge branch"
echo "8. Exit"

read -p "Choose an option (1-8): " choice

case $choice in
    1)
        echo "=== Git Status ==="
        git status
        ;;
    2)
        echo "=== Adding Changes ==="
        git add .
        echo "Changes added successfully!"
        ;;
    3)
        read -p "Enter commit message: " message
        git commit -m "$message"
        ;;
    4)
        echo "=== Git Log ==="
        git log --oneline -10
        ;;
    5)
        read -p "Enter new branch name: " branch_name
        git checkout -b "$branch_name"
        ;;
    6)
        echo "Available branches:"
        git branch
        read -p "Enter branch name to switch to: " branch_name
        git checkout "$branch_name"
        ;;
    7)
        echo "Available branches:"
        git branch
        read -p "Enter branch name to merge: " branch_name
        git merge "$branch_name"
        ;;
    8)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid option. Please choose 1-8."
        ;;
esac 