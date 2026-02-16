$ErrorActionPreference = "Stop"
cd (Split-Path $PSScriptRoot -Parent)
.\.venv\Scripts\activate
uvicorn api.main:app --port 8000
