#!/bin/bash
set -e

sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv redis-server

# Start redis
sudo service redis-server start

# Create venv and install dependencies
cd /mnt/c/Users/bhush/CareerLink/backend
python3 -m venv wsl_venv
source wsl_venv/bin/activate
pip install flask flask-sqlalchemy flask-security-too flask-restful celery redis weasyprint jinja2 flask-cors

echo "WSL Setup Complete"
