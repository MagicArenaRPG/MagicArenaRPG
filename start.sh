#!/bin/bash
set -e

echo "Updating pip and installing dependencies..."
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -r requirements.txt
echo "Installed packages:"
python3 -m pip list

echo "Starting bot..."
python3 bot.py
