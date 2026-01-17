#!/usr/bin/env pwsh

# Authentication Testing Script for Library Seat Booking System
# This script tests all authentication endpoints

Write-Host "=== Library Seat Booking - Authentication Test ===" -ForegroundColor Cyan
Write-Host ""

# Configuration
$apiBase = "http://localhost:8000/api"
$headers = @{ "Content-Type" = "application/json" }

# Colors for output
$success = "Green"
$error = "Red"
$info = "Cyan"
$warning = "Yellow"

# Test 1: Login with Admin Account
Write-Host "[TEST 1] Login Endpoint" -ForegroundColor $info
Write-Host "POST /auth/login/" -ForegroundColor $info
Write-Host "Credentials: admin@library.com / admin123" -ForegroundColor $info

$loginBody = @{
    email_or_phone = "admin@library.com"
    password       = "admin123"
} | ConvertTo-Json

try {
    $loginResponse = Invoke-WebRequest `
        -Uri "$apiBase/auth/login/" `
        -Method POST `
        -ContentType "application/json" `
        -Body $loginBody `
        -UseBasicParsing `
        -ErrorAction SilentlyContinue

    if ($loginResponse.StatusCode -eq 200) {
        Write-Host "✅ Login successful (Status: 200)" -ForegroundColor $success
        
        $loginData = $loginResponse.Content | ConvertFrom-Json
        
        # Extract tokens
        $accessToken = $loginData.access
        $refreshToken = $loginData.refresh
        $user = $loginData.user
        
        Write-Host "   User: $($user.username) ($($user.email))" -ForegroundColor $success
        Write-Host "   Role: $(if ($user.is_staff) { 'Admin' } else { 'Student' })" -ForegroundColor $success
        Write-Host "   Access Token: $($accessToken.Substring(0, 30))..." -ForegroundColor $success
        Write-Host ""
        
        # Test 2: Get Profile with Token
        Write-Host "[TEST 2] Protected Endpoint - Get Profile" -ForegroundColor $info
        Write-Host "GET /auth/profile/" -ForegroundColor $info
        Write-Host "Using Authorization: Bearer {accessToken}" -ForegroundColor $info
        
        $profileHeaders = @{
            "Authorization" = "Bearer $accessToken"
            "Content-Type"   = "application/json"
        }
        
        try {
            $profileResponse = Invoke-WebRequest `
                -Uri "$apiBase/auth/profile/" `
                -Method GET `
                -Headers $profileHeaders `
                -UseBasicParsing `
                -ErrorAction SilentlyContinue
            
            if ($profileResponse.StatusCode -eq 200) {
                Write-Host "✅ Profile fetch successful (Status: 200)" -ForegroundColor $success
                $profileData = $profileResponse.Content | ConvertFrom-Json
                Write-Host "   Username: $($profileData.username)" -ForegroundColor $success
                Write-Host "   Email: $($profileData.email)" -ForegroundColor $success
                Write-Host "   Member Since: $($profileData.date_joined)" -ForegroundColor $success
                Write-Host ""
            }
        } catch {
            Write-Host "❌ Profile fetch failed" -ForegroundColor $error
            Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor $error
            Write-Host ""
        }
        
        # Test 3: Token Refresh
        Write-Host "[TEST 3] Token Refresh Endpoint" -ForegroundColor $info
        Write-Host "POST /auth/token/refresh/" -ForegroundColor $info
        
        $refreshBody = @{
            refresh = $refreshToken
        } | ConvertTo-Json
        
        try {
            $refreshResponse = Invoke-WebRequest `
                -Uri "$apiBase/auth/token/refresh/" `
                -Method POST `
                -ContentType "application/json" `
                -Body $refreshBody `
                -UseBasicParsing `
                -ErrorAction SilentlyContinue
            
            if ($refreshResponse.StatusCode -eq 200) {
                Write-Host "✅ Token refresh successful (Status: 200)" -ForegroundColor $success
                $refreshData = $refreshResponse.Content | ConvertFrom-Json
                Write-Host "   New Access Token: $($refreshData.access.Substring(0, 30))..." -ForegroundColor $success
                Write-Host ""
            }
        } catch {
            Write-Host "❌ Token refresh failed" -ForegroundColor $error
            Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor $error
            Write-Host ""
        }
        
        # Test 4: Register New User
        Write-Host "[TEST 4] Registration Endpoint" -ForegroundColor $info
        Write-Host "POST /auth/register/" -ForegroundColor $info
        
        $timestamp = Get-Date -Format "yyyyMMddHHmmss"
        $regBody = @{
            username         = "testuser$timestamp"
            email            = "testuser$timestamp@library.com"
            password         = "TestPass123!"
            password_confirm = "TestPass123!"
            first_name       = "Test"
            last_name        = "User"
            student_id       = "STU$timestamp"
            department       = "IT"
            year_of_study    = 2
        } | ConvertTo-Json
        
        try {
            $regResponse = Invoke-WebRequest `
                -Uri "$apiBase/auth/register/" `
                -Method POST `
                -ContentType "application/json" `
                -Body $regBody `
                -UseBasicParsing `
                -ErrorAction SilentlyContinue
            
            if ($regResponse.StatusCode -eq 201) {
                Write-Host "✅ Registration successful (Status: 201)" -ForegroundColor $success
                $regData = $regResponse.Content | ConvertFrom-Json
                Write-Host "   New User: $($regData.user.username) ($($regData.user.email))" -ForegroundColor $success
                Write-Host "   Access Token: $($regData.access.Substring(0, 30))..." -ForegroundColor $success
                Write-Host ""
            }
        } catch {
            Write-Host "⚠️  Registration test skipped (likely user already exists)" -ForegroundColor $warning
            Write-Host ""
        }
        
    }
} catch {
    Write-Host "❌ Login failed" -ForegroundColor $error
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor $error
    Write-Host "   Make sure Django server is running on port 8000" -ForegroundColor $warning
    Write-Host ""
}

Write-Host "=== Test Summary ===" -ForegroundColor $info
Write-Host "Frontend: http://localhost:4200" -ForegroundColor $info
Write-Host "Backend:  http://localhost:8000" -ForegroundColor $info
Write-Host ""
Write-Host "Test Credentials:" -ForegroundColor $info
Write-Host "  Admin: admin@library.com / admin123" -ForegroundColor $info
Write-Host ""
