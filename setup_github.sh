#!/bin/bash
# GitHub Repository Setup Script for BackendPanel
# Username: abhishek123107

echo "🚀 Setting up GitHub Repository for BackendPanel..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git is not initialized. Please run 'git init' first."
    exit 1
fi

# Add remote repository (replace with your actual repo URL)
echo "📝 Adding remote repository..."
git remote add origin https://github.com/abhishek123107/BackendPanel.git

# Check if remote already exists
if git remote get-url origin > /dev/null 2>&1; then
    echo "✅ Remote repository already configured"
else
    echo "⚠️  Please create a repository on GitHub first:"
    echo "   1. Go to https://github.com/abhishek123107"
    echo "   2. Click 'New repository'"
    echo "   3. Name: BackendPanel"
    echo "   4. Description: Library Seat Booking Backend Panel"
    echo "   5. Make it Public"
    echo "   6. Click 'Create repository'"
    echo "   7. Run this script again"
    exit 1
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push -u origin main

echo "🎉 Repository setup complete!"
echo "📋 Next steps:"
echo "   1. Go to: https://github.com/abhishek123107/BackendPanel"
echo "   2. Verify all files are pushed"
echo "   3. Connect to Vercel for deployment"
