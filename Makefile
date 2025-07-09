# Development Scripts
# These scripts help with common development tasks

# Start the development server
dev:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Run tests
test:
	uv run pytest tests/ -v

# Run tests with coverage
test-coverage:
	uv run pytest tests/ -v --cov=app --cov-report=html

# Format code
format:
	uv run black app tests
	uv run ruff check app tests --fix

# Lint code
lint:
	uv run black --check app tests
	uv run ruff check app tests
	uv run mypy app

# Generate database migration
migrate:
	uv run alembic revision --autogenerate -m "$(MESSAGE)"

# Apply database migrations
upgrade:
	uv run alembic upgrade head

# Revert database migration
downgrade:
	uv run alembic downgrade -1

# Install dependencies
install:
	uv sync

# Install development dependencies
install-dev:
	uv sync --dev

# Clean up
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build

# Help
help:
	@echo "Available commands:"
	@echo "  dev           - Start development server"
	@echo "  test          - Run tests"
	@echo "  test-coverage - Run tests with coverage report"
	@echo "  format        - Format code with black and ruff"
	@echo "  lint          - Lint code"
	@echo "  migrate       - Generate database migration (use MESSAGE='description')"
	@echo "  upgrade       - Apply database migrations"
	@echo "  downgrade     - Revert last migration"
	@echo "  install       - Install dependencies"
	@echo "  install-dev   - Install development dependencies"
	@echo "  clean         - Clean up generated files"

.PHONY: dev test test-coverage format lint migrate upgrade downgrade install install-dev clean help
