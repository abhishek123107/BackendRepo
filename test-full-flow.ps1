# Full Flow Integration Test: Signup → Login → Profile → Dashboard

$baseUrl = "http://localhost:8000"
$apiUrl = "$baseUrl/api/auth"

# Colors for output
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Error { Write-Host $args -ForegroundColor Red }
function Write-Info { Write-Host $args -ForegroundColor Cyan }

Write-Info "=== Starting Full Flow Integration Test ==="

# Test 1: Signup
Write-Info "`n[1] Testing SIGNUP..."
$random = Get-Random
$signupData = @{
    username = "testuser_$random"
    email = "testuser_$random@example.com"
    password = "TestPassword@123"
    password_confirm = "TestPassword@123"
    first_name = "Test"
    last_name = "User"
    phone = "988$random"
    student_id = "STU$random"
    department = "CSE"
    year_of_study = "3"
} | ConvertTo-Json

try {
    $signupResponse = Invoke-RestMethod -Uri "$apiUrl/register/" `
        -Method POST `
        -ContentType "application/json" `
        -Body $signupData

    Write-Success "✅ Signup Success (201 Created)"
    Write-Info "Response: $($signupResponse | ConvertTo-Json)"
    
    # Extract values from response (user data is nested under "user" key)
    $user = $signupResponse.user
    if ($user) {
        $userId = $user.id
        $userEmail = $user.email
        $userUsername = $user.username
    } else {
        $userId = $signupResponse.id
        $userEmail = $signupResponse.email
        $userUsername = $signupResponse.username
    }
    
    Write-Info "DEBUG: userId=$userId"
    Write-Info "DEBUG: userEmail=$userEmail"
    Write-Info "DEBUG: userUsername=$userUsername"
}
catch {
    Write-Error "❌ Signup Failed"
    Write-Error "Error: $($_.Exception.Response.StatusCode) - $($_.Exception.Message)"
    if ($_.ErrorDetails) {
        Write-Error "Details: $($_.ErrorDetails.Message)"
    }
    exit
}

# Test 2: Login
Write-Info "`n[2] Testing LOGIN..."
$loginData = @{
    email_or_phone = $userEmail
    password = "TestPassword@123"
}
$loginJson = $loginData | ConvertTo-Json
Write-Info "Sending login data: $loginJson"

try {
    $loginResponse = Invoke-RestMethod -Uri "$apiUrl/login/" `
        -Method POST `
        -ContentType "application/json" `
        -Body $loginJson

    Write-Success "✅ Login Success (200 OK)"
    Write-Info "Response Keys: $($loginResponse.PSObject.Properties.Name)"
    
    $accessToken = $loginResponse.access
    $refreshToken = $loginResponse.refresh
    $user = $loginResponse.user
    
    if ($accessToken) {
        Write-Success "✅ Access Token received"
    }
    if ($user) {
        Write-Success "✅ User data received: $($user.email)"
    }
}
catch {
    Write-Error "❌ Login Failed"
    Write-Error "Error: $($_.Exception.Response.StatusCode) - $($_.Exception.Message)"
    if ($_.ErrorDetails) {
        Write-Error "Details: $($_.ErrorDetails.Message)"
    }
    exit
}

# Test 3: Fetch Profile
Write-Info "`n[3] Testing GET PROFILE..."
$headers = @{
    "Authorization" = "Bearer $accessToken"
    "Content-Type" = "application/json"
}

try {
    $profileResponse = Invoke-RestMethod -Uri "$apiUrl/profile/" `
        -Method GET `
        -Headers $headers

    Write-Success "✅ Profile Fetch Success (200 OK)"
    Write-Info "User: $($profileResponse.email) - $($profileResponse.first_name) $($profileResponse.last_name)"
    Write-Info "Student ID: $($profileResponse.student_id)"
    Write-Info "Department: $($profileResponse.department)"
    Write-Info "Year: $($profileResponse.year_of_study)"
}
catch {
    Write-Error "❌ Profile Fetch Failed"
    Write-Error "Error: $($_.Exception.Response.StatusCode) - $($_.Exception.Message)"
    if ($_.ErrorDetails) {
        Write-Error "Details: $($_.ErrorDetails.Message)"
    }
    exit
}

# Test 4: Update Profile
Write-Info "`n[4] Testing UPDATE PROFILE..."
$updateData = @{
    phone = "9876543211"
    department = "ECE"
} | ConvertTo-Json

try {
    $updateResponse = Invoke-RestMethod -Uri "$apiUrl/profile/" `
        -Method PATCH `
        -Headers $headers `
        -Body $updateData

    Write-Success "✅ Profile Update Success (200 OK)"
    Write-Info "Updated Phone: $($updateResponse.phone)"
    Write-Info "Updated Department: $($updateResponse.department)"
}
catch {
    Write-Error "❌ Profile Update Failed"
    Write-Error "Error: $($_.Exception.Response.StatusCode) - $($_.Exception.Message)"
    if ($_.ErrorDetails) {
        Write-Error "Details: $($_.ErrorDetails.Message)"
    }
}

# Test 5: Verify Updated Data
Write-Info "`n[5] Verifying Updated Data..."
try {
    $verifyResponse = Invoke-RestMethod -Uri "$apiUrl/profile/" `
        -Method GET `
        -Headers $headers

    Write-Success "✅ Data Persisted Successfully"
    Write-Info "Phone: $($verifyResponse.phone) (should be 9876543211)"
    Write-Info "Department: $($verifyResponse.department) (should be ECE)"
}
catch {
    Write-Error "❌ Verification Failed"
}

Write-Info "`n=== Full Flow Integration Test Complete ==="
Write-Success "✅ All tests passed! Data flows successfully from signup → login → profile → update"
