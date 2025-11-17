#!/bin/bash

# Build script for Vercel deployment
echo "Building the project..."

# Install dependencies
pip install -r requirements.txt

# Collect static files
python Blog/manage.py collectstatic --noinput --clear

echo "Build completed!"
