#!/bin/bash

# Build script for Vercel deployment
echo "Building the project..."

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create staticfiles directory
echo "Creating staticfiles directory..."
mkdir -p Blog/staticfiles_build/static

# Collect static files
echo "Collecting static files..."
cd Blog
python manage.py collectstatic --noinput --clear || echo "Warning: collectstatic failed, continuing anyway"
cd ..

echo "Build completed!"
