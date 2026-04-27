#!/bin/bash
echo "Starting Emby Missing Monitor..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py