import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_user):
    """Test successful login."""
    login_data = {
        "username": test_user.username,
        "password": "testpassword123"
    }
    response = await client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient, test_user):
    """Test login with invalid credentials."""
    login_data = {
        "username": test_user.username,
        "password": "wrongpassword"
    }
    response = await client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


@pytest.mark.asyncio
async def test_token_endpoint(client: AsyncClient, test_user):
    """Test the OAuth2 token endpoint."""
    form_data = {
        "username": test_user.username,
        "password": "testpassword123"
    }
    response = await client.post("/api/v1/auth/token", data=form_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
