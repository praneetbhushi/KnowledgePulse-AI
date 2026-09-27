# KnowledgePulse AI - Start Backend + Frontend

$ProjectRoot = "C:\Users\Dell\Desktop\KnowledgePulse-AI"

# Start Backend
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$ProjectRoot\backend'; .\.venv\Scripts\Activate.ps1; python -m uvicorn app.main:app --reload"
)

# Start Frontend
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$ProjectRoot\frontend'; npm run dev"
)

Write-Host "KnowledgePulse AI backend and frontend are starting..."
Write-Host "Backend:  http://127.0.0.1:8000"
Write-Host "Frontend: http://localhost:5173"