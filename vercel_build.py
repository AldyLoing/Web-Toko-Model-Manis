#!/usr/bin/env python
"""
Vercel build script
"""
import os
import subprocess
import sys

def main():
    print("Starting Vercel build process...")
    
    # Change to Blog directory
    blog_dir = os.path.join(os.path.dirname(__file__), 'Blog')
    os.chdir(blog_dir)
    
    print(f"Current directory: {os.getcwd()}")
    
    # Run collectstatic
    print("Collecting static files...")
    result = subprocess.run(
        [sys.executable, 'manage.py', 'collectstatic', '--noinput', '--clear'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✓ Static files collected successfully")
        print(result.stdout)
    else:
        print("✗ Error collecting static files:")
        print(result.stderr)
        sys.exit(1)
    
    print("Build completed successfully!")

if __name__ == '__main__':
    main()
