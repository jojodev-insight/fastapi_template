import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    """Test user creation."""
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpassword123",
        "full_name": "New User"
    }
    response = await client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "id" in data
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_create_user_duplicate_username(client: AsyncClient, test_user):
    """Test creating user with duplicate username."""
    user_data = {
        "username": test_user.username,
        "email": "different@example.com",
        "password": "password123",
    }
    response = await client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_users(client: AsyncClient, auth_headers):
    """Test getting all users (requires authentication)."""
    response = await client.get("/api/v1/users/", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, auth_headers, test_user):
    """Test getting current user information."""
    response = await client.get("/api/v1/users/me", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["username"] == test_user.username
    assert data["email"] == test_user.email


@pytest.mark.asyncio
async def test_get_user_by_id(client: AsyncClient, auth_headers, test_user):
    """Test getting user by ID."""
    response = await client.get(f"/api/v1/users/{test_user.id}", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == test_user.id
    assert data["username"] == test_user.username


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient, auth_headers, test_user):
    """Test updating user information."""
    update_data = {
        "full_name": "Updated Name",
    }
    response = await client.put(
        f"/api/v1/users/{test_user.id}", 
        json=update_data, 
        headers=auth_headers
    )
    assert response.status_code == 200
    
    data = response.json()
    assert data["full_name"] == update_data["full_name"]


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    """Test accessing protected endpoints without authentication."""
    response = await client.get("/api/v1/users/")
    assert response.status_code == 401
