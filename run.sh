#!/bin/bash
# Script to run the application

# Ensure virtualenv is active
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
if [ -d "venv/bin" ]; then
    # Unix
    source venv/bin/activate
elif [ -d "venv/Scripts" ]; then
    # Windows
    source venv/Scripts/activate
else
    echo "Virtual environment not found!"
    exit 1
fi

# Install requirements
pip install -r requirements.txt

# Run the application directly
python main.py
