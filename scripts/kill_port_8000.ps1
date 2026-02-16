$line = netstat -ano | findstr :8000 | findstr LISTENING
if (-not $line) { Write-Host "Nothing is listening on 8000."; exit 0 }
$pid = ($line -split "\s+")[-1]
Write-Host "Killing PID $pid on port 8000"
taskkill /PID $pid /F
