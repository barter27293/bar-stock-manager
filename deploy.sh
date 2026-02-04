#!/bin/bash
set -e

cd /home/ploi/bar-stock-manager

# Pull latest code
git pull origin main

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Restart the app
sudo supervisorctl restart bar-stock-manager

echo "Deployed successfully!"
