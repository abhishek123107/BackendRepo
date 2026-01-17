$ts = Get-Date -Format yyyyMMddHHmmss
$valid = @{
    username = "apitest$ts"
    email = "apitest$ts@library.com"
    password = "TestPass123!"
    password_confirm = "TestPass123!"
    first_name = "API"
    last_name = "Valid"
    student_id = "STU$ts"
    department = "IT"
    year_of_study = 2
} | ConvertTo-Json

Write-Host '--- VALID REQUEST ---'
Write-Host $valid
try {
    $r = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/auth/register/' -Method Post -ContentType 'application/json' -Body $valid
    Write-Host '--- VALID RESPONSE ---'
    $r | ConvertTo-Json -Depth 10 | Write-Host
} catch {
    if ($_.Exception.Response) {
        $stream = $_.Exception.Response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($stream)
        $resp = $reader.ReadToEnd()
        Write-Host '--- VALID ERROR RESPONSE ---'
        Write-Host $resp
    } else {
        Write-Host '--- VALID ERROR ---'
        Write-Host $_.Exception.Message
    }
}

$invalid = @{
    username = "baduser$ts"
    email = ""
    password = ""
    password_confirm = ""
    first_name = "Bad"
    last_name = "User"
} | ConvertTo-Json

Write-Host '--- INVALID REQUEST ---'
Write-Host $invalid
try {
    $r2 = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/auth/register/' -Method Post -ContentType 'application/json' -Body $invalid
    Write-Host '--- INVALID RESPONSE ---'
    $r2 | ConvertTo-Json -Depth 10 | Write-Host
} catch {
    if ($_.Exception.Response) {
        $stream2 = $_.Exception.Response.GetResponseStream()
        $reader2 = New-Object System.IO.StreamReader($stream2)
        $resp2 = $reader2.ReadToEnd()
        Write-Host '--- INVALID ERROR RESPONSE ---'
        Write-Host $resp2
    } else {
        Write-Host '--- INVALID ERROR ---'
        Write-Host $_.Exception.Message
    }
}
