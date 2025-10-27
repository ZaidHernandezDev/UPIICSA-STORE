#!/bin/bash

# Build script for Vercel
echo "Building project..."

# Install dependencies
pip3 install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --noinput --clear

echo "Build completed successfully!"
