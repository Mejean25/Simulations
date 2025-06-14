#!/bin/bash
cd /Users/leapcube/mc-simulations || exit

# Save uncommitted work
git add .
timestamp=$(date "+%Y-%m-%d %H:%M:%S")
git commit -m "Auto-commit local changes at $timestamp" || echo "Nothing to commit"

# Pull from GitHub, merge any remote updates
git pull origin main --no-edit

# Push merged result back to GitHub
git push origin main

