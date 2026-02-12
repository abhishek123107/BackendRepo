#!/usr/bin/env python3
"""
DATABASE_URL validation script for Render PostgreSQL
Run this script to validate your DATABASE_URL format
"""

import os
import re
from urllib.parse import urlparse

def validate_database_url(url):
    """
    Validate DATABASE_URL format for PostgreSQL
    """
    if not url:
        return False, "DATABASE_URL is empty"
    
    try:
        parsed = urlparse(url)
        
        # Check scheme
        if parsed.scheme not in ['postgresql', 'postgres']:
            return False, f"Invalid scheme: {parsed.scheme}. Expected 'postgresql' or 'postgres'"
        
        # Check hostname
        if not parsed.hostname:
            return False, "Missing hostname in DATABASE_URL"
        
        # Check port
        if parsed.port:
            if not isinstance(parsed.port, int) or parsed.port <= 0 or parsed.port > 65535:
                return False, f"Invalid port: {parsed.port}. Must be between 1-65535"
        
        # Check database name
        if not parsed.path or parsed.path == '/':
            return False, "Missing database name in DATABASE_URL"
        
        database_name = parsed.path.lstrip('/')
        if not database_name:
            return False, "Database name cannot be empty"
        
        return True, "DATABASE_URL format is valid"
        
    except Exception as e:
        return False, f"Error parsing DATABASE_URL: {str(e)}"

def get_render_database_url_format():
    """
    Show correct DATABASE_URL format for Render
    """
    print("🔧 CORRECT DATABASE_URL FORMAT FOR RENDER:")
    print("=" * 50)
    print("postgresql://username:password@host:5432/database_name")
    print()
    print("📝 EXAMPLE:")
    print("postgresql://myuser:mypassword@mydb.abc123.rds.amazonaws.com:5432/mydatabase")
    print()
    print("🔍 WHERE TO FIND THESE VALUES:")
    print("1. Go to Render Dashboard")
    print("2. Click on your PostgreSQL database")
    print("3. Go to 'Connections' tab")
    print("4. Copy the 'External Database URL'")
    print()

def main():
    """
    Main validation function
    """
    print("🔍 DATABASE_URL VALIDATION TOOL")
    print("=" * 40)
    
    # Show correct format
    get_render_database_url_format()
    
    # Test current DATABASE_URL
    database_url = os.environ.get('DATABASE_URL', '')
    
    if database_url:
        print(f"🔍 TESTING CURRENT DATABASE_URL:")
        print(f"URL: {database_url[:30]}..." if len(database_url) > 30 else f"URL: {database_url}")
        print()
        
        is_valid, message = validate_database_url(database_url)
        
        if is_valid:
            print("✅ VALIDATION PASSED")
            print(f"✅ {message}")
            
            # Parse and show components
            parsed = urlparse(database_url)
            print("\n📋 URL COMPONENTS:")
            print(f"   Scheme: {parsed.scheme}")
            print(f"   Username: {parsed.username}")
            print(f"   Password: {'*' * len(parsed.password) if parsed.password else 'None'}")
            print(f"   Host: {parsed.hostname}")
            print(f"   Port: {parsed.port}")
            print(f"   Database: {parsed.path.lstrip('/')}")
            
        else:
            print("❌ VALIDATION FAILED")
            print(f"❌ {message}")
            print("\n🔧 FIX STEPS:")
            print("1. Check that port is a number (usually 5432)")
            print("2. Ensure URL follows the correct format")
            print("3. Get the correct URL from Render dashboard")
    else:
        print("⚠️  NO DATABASE_URL FOUND")
        print("Please set DATABASE_URL environment variable")
    
    print("\n🚀 COMMON ISSUES AND FIXES:")
    print("-" * 30)
    print("Issue: 'port' instead of actual port number")
    print("Fix: Replace 'port' with '5432'")
    print()
    print("Issue: Missing database name")
    print("Fix: Add database name after the last slash")
    print()
    print("Issue: Wrong scheme")
    print("Fix: Use 'postgresql://' not 'http://'")

if __name__ == "__main__":
    main()
