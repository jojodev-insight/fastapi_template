"""
Database setup script for different database types.
This script helps you set up the database configuration for SQLite, PostgreSQL, or MySQL.
"""



def setup_sqlite():
    """Setup SQLite configuration."""
    env_content = """# SQLite Configuration
DEBUG=true
LOG_LEVEL=debug
HOST=127.0.0.1
PORT=8000

# Database Configuration
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
"""

    with open(".env", "w") as f:
        f.write(env_content)

    print("✅ SQLite configuration created in .env file")
    print("📝 SQLite database will be created automatically when you run the app")


def setup_postgresql():
    """Setup PostgreSQL configuration."""
    env_content = """# PostgreSQL Configuration
DEBUG=true
LOG_LEVEL=debug
HOST=127.0.0.1
PORT=8000

# Database Configuration
DATABASE_TYPE=postgresql
DATABASE_URL=postgresql+asyncpg://fastapi_user:fastapi_password@localhost:5432/fastapi_db

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
ALLOWED_METHODS=["*"]
ALLOWED_HEADERS=["*"]
"""

    with open(".env", "w") as f:
        f.write(env_content)

    print("✅ PostgreSQL configuration created in .env file")
    print("🐳 To start PostgreSQL with Docker:")
    print("   docker-compose up postgres")
    print("🔧 Or install PostgreSQL manually and create:")
    print("   - Database: fastapi_db")
    print("   - User: fastapi_user")
    print("   - Password: fastapi_password")


def setup_mysql():
    """Setup MySQL configuration."""
    env_content = """# MySQL Configuration
DEBUG=true
LOG_LEVEL=debug
HOST=127.0.0.1
PORT=8000

# Database Configuration
DATABASE_TYPE=mysql
DATABASE_URL=mysql+aiomysql://fastapi_user:fastapi_password@localhost:3306/fastapi_db

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
ALLOWED_METHODS=["*"]
ALLOWED_HEADERS=["*"]
"""

    with open(".env", "w") as f:
        f.write(env_content)

    print("✅ MySQL configuration created in .env file")
    print("🐳 To start MySQL with Docker:")
    print("   docker-compose up mysql")
    print("🔧 Or install MySQL manually and create:")
    print("   - Database: fastapi_db")
    print("   - User: fastapi_user")
    print("   - Password: fastapi_password")


def main():
    """Main setup function."""
    print("🚀 FastAPI Template Database Setup")
    print("===================================")
    print()
    print("Choose your database type:")
    print("1. SQLite (recommended for development)")
    print("2. PostgreSQL")
    print("3. MySQL")
    print()

    while True:
        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            setup_sqlite()
            break
        elif choice == "2":
            setup_postgresql()
            break
        elif choice == "3":
            setup_mysql()
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

    print()
    print("🎯 Next steps:")
    print("1. Install dependencies: uv sync --dev")
    print("2. Run database migrations: uv run alembic upgrade head")
    print("3. Start the development server: uv run uvicorn app.main:app --reload")
    print()
    print("📚 For more information, see the README.md file")


if __name__ == "__main__":
    main()
