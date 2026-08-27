#!/usr/bin/env python3
"""
Deployment Script for Housing Price Prediction System
This script helps you start both the prediction server and Streamlit app.
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = ['streamlit', 'flask', 'pandas', 'numpy', 'scikit-learn']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def check_model():
    """Check if the trained model exists."""
    model_path = Path("./mlruns/0/d1be49444ebc4c37a69488da5777f496/artifacts/model/model.pkl")
    
    if not model_path.exists():
        print("❌ Trained model not found!")
        print("Please ensure you have run the training pipeline first.")
        return False
    
    print("✅ Trained model found")
    return True

def start_server():
    """Start the Flask prediction server."""
    print("🚀 Starting prediction server...")
    
    try:
        # Start the server in the background
        process = subprocess.Popen([
            sys.executable, "simple_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for the server to start
        time.sleep(3)
        
        # Check if server is running
        try:
            import requests
            response = requests.get("http://127.0.0.1:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Prediction server is running at http://127.0.0.1:8000")
                return process
            else:
                print("❌ Server started but health check failed")
                return None
        except Exception as e:
            print(f"❌ Server health check failed: {e}")
            return None
            
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return None

def start_streamlit():
    """Start the Streamlit web app."""
    print("🌐 Starting Streamlit app...")
    
    try:
        # Start Streamlit in the background
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for the app to start
        time.sleep(5)
        
        print("✅ Streamlit app is running at http://localhost:8501")
        return process
        
    except Exception as e:
        print(f"❌ Failed to start Streamlit: {e}")
        return None

def main():
    """Main deployment function."""
    print("🏡 Housing Price Prediction System - Deployment")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check model
    if not check_model():
        sys.exit(1)
    
    print("\n📋 Starting services...")
    
    # Start prediction server
    server_process = start_server()
    if not server_process:
        print("❌ Failed to start prediction server")
        sys.exit(1)
    
    # Start Streamlit app
    streamlit_process = start_streamlit()
    if not streamlit_process:
        print("❌ Failed to start Streamlit app")
        server_process.terminate()
        sys.exit(1)
    
    print("\n🎉 Deployment successful!")
    print("=" * 50)
    print("📊 Prediction Server: http://127.0.0.1:8000")
    print("🌐 Streamlit App: http://localhost:8501")
    print("📖 API Documentation: http://127.0.0.1:8000/")
    print("\n💡 Tips:")
    print("- Keep this terminal open to monitor the services")
    print("- Use Ctrl+C to stop both services")
    print("- Check the README.md for detailed usage instructions")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        server_process.terminate()
        streamlit_process.terminate()
        print("✅ Services stopped")

if __name__ == "__main__":
    main()
