# FastAPI Template

A highly versatile FastAPI project template with multi-database support (SQLite, PostgreSQL, MySQL), authentication, and comprehensive testing.

## Features

- ✅ **FastAPI** - Modern, fast web framework for APIs
- ✅ **Multi-Database Support** - SQLite, PostgreSQL, MySQL with async support
- ✅ **Authentication** - JWT token-based authentication
- ✅ **Database Migrations** - Alembic for database version control
- ✅ **Testing** - Comprehensive test suite with pytest
- ✅ **Code Quality** - Black, Ruff, and MyPy for code formatting and linting
- ✅ **Docker Support** - Multi-database Docker Compose configuration
- ✅ **uv Integration** - Fast Python package manager
- ✅ **Type Hints** - Full type annotation support
- ✅ **Pydantic v2** - Data validation and settings management
- ✅ **CORS Support** - Cross-origin resource sharing
- ✅ **Async/Await** - Fully asynchronous implementation

## Quick Start

### Prerequisites

- Python 3.9+
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd fastapi-template
   ```

2. **Install dependencies**:
   ```bash
   uv sync --dev
   ```

3. **Set up your database**:
   ```bash
   uv run python scripts/setup_db.py
   ```

4. **Copy environment variables**:
   ```bash
   cp .env.example .env
   ```

5. **Run database migrations**:
   ```bash
   uv run alembic upgrade head
   ```

6. **Start the development server**:
   ```bash
   uv run uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

### Documentation

- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative API Docs**: `http://localhost:8000/redoc` (ReDoc)

## Database Configuration

### SQLite (Default)

Perfect for development and testing:

```env
DATABASE_TYPE=sqlite
DATABASE_URL=sqlite:///./app.db
```

### PostgreSQL

For production use:

```env
DATABASE_TYPE=postgresql
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/fastapi_db
```

**Using Docker**:
```bash
docker-compose up postgres
```

### MySQL

Alternative database option:

```env
DATABASE_TYPE=mysql
DATABASE_URL=mysql+aiomysql://username:password@localhost:3306/fastapi_db
```

**Using Docker**:
```bash
docker-compose up mysql
```

## Development

### Using uv Commands

```bash
# Install dependencies
uv sync --dev

# Run development server
uv run uvicorn app.main:app --reload

# Run tests
uv run pytest tests/ -v

# Run tests with coverage
uv run pytest tests/ -v --cov=app --cov-report=html

# Format code
uv run black app tests
uv run ruff check app tests --fix

# Type checking
uv run mypy app

# Create migration
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head
```

### Using PowerShell Scripts (Windows)

Load the PowerShell development scripts:

```powershell
. .\scripts\dev.ps1
```

Then use convenient aliases:

```powershell
dev              # Start development server
test             # Run tests
test-cov         # Run tests with coverage
format           # Format code
lint             # Lint code
migrate          # Create migration
upgrade          # Apply migrations
clean            # Clean up files
help             # Show help
```

### Using Make (Linux/macOS)

```bash
make dev         # Start development server
make test        # Run tests
make test-coverage # Run tests with coverage
make format      # Format code
make lint        # Lint code
make migrate MESSAGE="description"  # Create migration
make upgrade     # Apply migrations
make clean       # Clean up files
make help        # Show help
```

## API Endpoints

### Authentication

- `POST /api/v1/auth/login` - Login with username/password
- `POST /api/v1/auth/token` - OAuth2 token endpoint

### Users

- `GET /api/v1/users/` - Get all users (authenticated)
- `POST /api/v1/users/` - Create new user
- `GET /api/v1/users/me` - Get current user
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

### Items

- `GET /api/v1/items/` - Get all items (public)
- `POST /api/v1/items/` - Create new item (authenticated)
- `GET /api/v1/items/my-items` - Get current user's items
- `GET /api/v1/items/{id}` - Get item by ID
- `PUT /api/v1/items/{id}` - Update item (owner only)
- `DELETE /api/v1/items/{id}` - Delete item (owner only)

## Testing

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app --cov-report=html

# Run specific test file
uv run pytest tests/test_users.py

# Run with verbose output
uv run pytest -v
```

### Test Structure

```
tests/
├── conftest.py         # Test configuration and fixtures
├── test_main.py        # Main app tests
├── test_auth.py        # Authentication tests
├── test_users.py       # User endpoint tests
└── test_items.py       # Item endpoint tests
```

## Docker Support

### Development with Docker

```bash
# Start all services
docker-compose up

# Start specific database
docker-compose up postgres  # or mysql
```

### Production Deployment

```bash
# Build and run
docker-compose up -d
```

## Project Structure

```
fastapi-template/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app creation
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py      # Authentication endpoints
│   │       ├── users.py     # User endpoints
│   │       └── items.py     # Item endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Configuration settings
│   │   ├── database.py      # Database setup
│   │   └── security.py      # Security utilities
│   ├── models/
│   │   └── __init__.py      # SQLAlchemy models
│   ├── repositories/
│   │   └── __init__.py      # Database repositories
│   └── schemas/
│       └── __init__.py      # Pydantic schemas
├── tests/
│   ├── conftest.py          # Test configuration
│   ├── test_main.py         # Main tests
│   ├── test_auth.py         # Auth tests
│   ├── test_users.py        # User tests
│   └── test_items.py        # Item tests
├── alembic/                 # Database migrations
├── scripts/                 # Development scripts
├── config/                  # Configuration files
├── docker-compose.yml       # Multi-database Docker setup
├── Dockerfile              # Container configuration
├── pyproject.toml          # Project configuration
├── Makefile               # Development commands
└── README.md              # Documentation
```

## Configuration

### Environment Variables

Key environment variables (see `.env.example`):

```env
# App Configuration
DEBUG=true
LOG_LEVEL=debug
HOST=127.0.0.1
PORT=8000

# Database
DATABASE_TYPE=sqlite
DATABASE_URL=sqlite:///./app.db

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
ALLOWED_METHODS=["*"]
ALLOWED_HEADERS=["*"]
```

### Database Migrations

```bash
# Create a new migration
uv run alembic revision --autogenerate -m "Add new table"

# Apply migrations
uv run alembic upgrade head

# Revert migration
uv run alembic downgrade -1

# Show migration history
uv run alembic history
```

## Security

- **Password Hashing**: Uses bcrypt for secure password hashing
- **JWT Tokens**: Secure authentication with configurable expiration
- **CORS**: Configurable cross-origin resource sharing
- **Input Validation**: Pydantic models for request validation
- **SQL Injection Protection**: SQLAlchemy ORM with parameterized queries

## Code Quality

This project uses several tools to maintain code quality:

- **Black**: Code formatting
- **Ruff**: Fast Python linter
- **MyPy**: Static type checking
- **Pytest**: Testing framework
- **Pre-commit**: Git hooks for code quality

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Sample Usage

### Create a User

```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "full_name": "John Doe"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepassword123"
  }'
```

### Create an Item (with authentication)

```bash
curl -X POST "http://localhost:8000/api/v1/items/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "Sample Item",
    "description": "This is a sample item",
    "price": 2999
  }'
```

## Support

For questions, issues, or contributions, please open an issue on the GitHub repository.

---

**Happy coding! 🚀**

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_TYPE` | Database type (sqlite/postgresql/mysql) | sqlite |
| `DATABASE_URL` | Full database URL | sqlite:///./app.db |
| `SECRET_KEY` | JWT secret key | your-secret-key |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | 30 |

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `POST /auth/refresh` - Refresh token

### Users
- `GET /users/me` - Get current user
- `GET /users/{user_id}` - Get user by ID
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Items
- `GET /items/` - List items
- `POST /items/` - Create item
- `GET /items/{item_id}` - Get item by ID
- `PUT /items/{item_id}` - Update item
- `DELETE /items/{item_id}` - Delete item

## Testing

Run tests with pytest:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app
```

## Docker Deployment

Build and run with Docker:

```bash
docker-compose up --build
```

## License

MIT License
