# Development Scripts for Windows PowerShell
# These scripts help with common development tasks using uv

# Start the development server
function Start-DevServer {
    uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
}

# Run tests
function Run-Tests {
    uv run pytest tests/ -v
}

# Run tests with coverage
function Run-TestsWithCoverage {
    uv run pytest tests/ -v --cov=app --cov-report=html
}

# Format code
function Format-Code {
    uv run black app tests
    uv run ruff check app tests --fix
}

# Lint code
function Lint-Code {
    uv run black --check app tests
    uv run ruff check app tests
    uv run mypy app
}

# Generate database migration
function New-Migration {
    param([string]$Message = "auto migration")
    uv run alembic revision --autogenerate -m $Message
}

# Apply database migrations
function Update-Database {
    uv run alembic upgrade head
}

# Revert database migration
function Revert-Migration {
    uv run alembic downgrade -1
}

# Install dependencies
function Install-Dependencies {
    uv sync
}

# Install development dependencies
function Install-DevDependencies {
    uv sync --dev
}

# Clean up
function Clean-Project {
    Get-ChildItem -Path . -Include "*.pyc" -Recurse | Remove-Item -Force
    Get-ChildItem -Path . -Include "__pycache__" -Recurse -Directory | Remove-Item -Force -Recurse
    Get-ChildItem -Path . -Include "*.egg-info" -Recurse -Directory | Remove-Item -Force -Recurse
    if (Test-Path ".pytest_cache") { Remove-Item -Path ".pytest_cache" -Force -Recurse }
    if (Test-Path ".coverage") { Remove-Item -Path ".coverage" -Force }
    if (Test-Path "htmlcov") { Remove-Item -Path "htmlcov" -Force -Recurse }
    if (Test-Path "dist") { Remove-Item -Path "dist" -Force -Recurse }
    if (Test-Path "build") { Remove-Item -Path "build" -Force -Recurse }
}

# Help
function Show-Help {
    Write-Host "Available commands:"
    Write-Host "  Start-DevServer         - Start development server"
    Write-Host "  Run-Tests              - Run tests"
    Write-Host "  Run-TestsWithCoverage  - Run tests with coverage report"
    Write-Host "  Format-Code            - Format code with black and ruff"
    Write-Host "  Lint-Code              - Lint code"
    Write-Host "  New-Migration          - Generate database migration"
    Write-Host "  Update-Database        - Apply database migrations"
    Write-Host "  Revert-Migration       - Revert last migration"
    Write-Host "  Install-Dependencies   - Install dependencies"
    Write-Host "  Install-DevDependencies - Install development dependencies"
    Write-Host "  Clean-Project          - Clean up generated files"
    Write-Host "  Show-Help              - Show this help message"
}

# Create aliases for easier use
Set-Alias -Name dev -Value Start-DevServer
Set-Alias -Name test -Value Run-Tests
Set-Alias -Name test-cov -Value Run-TestsWithCoverage
Set-Alias -Name format -Value Format-Code
Set-Alias -Name lint -Value Lint-Code
Set-Alias -Name migrate -Value New-Migration
Set-Alias -Name upgrade -Value Update-Database
Set-Alias -Name downgrade -Value Revert-Migration
Set-Alias -Name install -Value Install-Dependencies
Set-Alias -Name install-dev -Value Install-DevDependencies
Set-Alias -Name clean -Value Clean-Project
Set-Alias -Name help -Value Show-Help

Write-Host "FastAPI Template PowerShell scripts loaded!"
Write-Host "Type 'Show-Help' or 'help' to see available commands."
