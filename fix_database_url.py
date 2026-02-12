#!/usr/bin/env python3
"""
Quick fix for DATABASE_URL port issue
This script helps identify and fix the port problem
"""

import os
import re

def fix_database_url(url):
    """
    Fix common DATABASE_URL issues
    """
    if not url:
        return None, "DATABASE_URL is empty"
    
    # Fix 1: Replace literal 'port' with '5432'
    if ':port/' in url:
        url = url.replace(':port/', ':5432/')
        print("✅ Fixed: Replaced literal 'port' with '5432'")
    
    # Fix 2: Ensure postgresql:// scheme
    if url.startswith('postgres://'):
        url = url.replace('postgres://', 'postgresql://')
        print("✅ Fixed: Changed 'postgres://' to 'postgresql://'")
    
    # Fix 3: Add database name if missing
    if url.endswith(':5432/') or url.endswith(':5432'):
        url = url.rstrip('/') + '/render_db'
        print("✅ Fixed: Added database name 'render_db'")
    
    # Validate the fixed URL
    if re.match(r'^postgresql://[^:]+:[^@]+@[^:]+:5432/[^/]+$', url):
        return url, "DATABASE_URL is now valid"
    else:
        return url, "DATABASE_URL format may still have issues"

def main():
    """
    Main fix function
    """
    print("🔧 DATABASE_URL QUICK FIX")
    print("=" * 30)
    
    # Get current DATABASE_URL
    current_url = os.environ.get('DATABASE_URL', '')
    
    print(f"Current DATABASE_URL: {current_url}")
    print()
    
    if not current_url:
        print("❌ No DATABASE_URL found in environment")
        print("\n🔧 TO FIX:")
        print("1. Go to Render dashboard")
        print("2. Your Web Service → Environment")
        print("3. Add DATABASE_URL with correct format")
        print("4. Use: postgresql://user:pass@host:5432/dbname")
        return
    
    # Try to fix the URL
    fixed_url, message = fix_database_url(current_url)
    
    print(f"\nFixed DATABASE_URL: {fixed_url}")
    print(f"Status: {message}")
    
    if fixed_url != current_url:
        print("\n🔧 STEPS TO APPLY FIX:")
        print("1. Copy the fixed DATABASE_URL above")
        print("2. Go to Render dashboard")
        print("3. Your Web Service → Environment")
        print("4. Update DATABASE_URL with the fixed value")
        print("5. Save changes")
        print("6. Trigger manual deploy")
    
    print("\n📋 CORRECT FORMAT EXAMPLES:")
    print("postgresql://myuser:mypassword@mydb.abc123.r2-db.com:5432/mydatabase")
    print("postgresql://user:pass@host:5432/dbname")

if __name__ == "__main__":
    main()
