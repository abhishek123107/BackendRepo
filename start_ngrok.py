#!/usr/bin/env python3
"""
Ngrok script to expose Django backend to the internet
"""
from pyngrok import ngrok
import os
import time

def start_ngrok():
    # Start ngrok tunnel
    public_url = ngrok.connect(8000)
    print(f"🚀 Public URL: {public_url}")
    print(f"📱 Frontend can now connect to: {public_url}/api/")
    print(f"🔗 Add this URL to CORS_ALLOWED_ORIGINS in settings.py")
    print(f"⚠️  Keep this terminal open to maintain the tunnel")
    
    # Keep the tunnel alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping ngrok tunnel...")
        ngrok.disconnect(public_url)

if __name__ == "__main__":
    start_ngrok()
