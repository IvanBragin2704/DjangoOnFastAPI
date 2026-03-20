#!/bin/bash
echo "starting app..."
echo "venv activating..."
source venv/Scripts/activate
echo "go to directory fastapi_app..."
cd fastapi_app/
echo "staring now..."
python main.py
