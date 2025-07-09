import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_item(client: AsyncClient, auth_headers):
    """Test creating an item."""
    item_data = {
        "title": "Test Item",
        "description": "This is a test item",
        "price": 1000  # $10.00 in cents
    }
    response = await client.post("/api/v1/items/", json=item_data, headers=auth_headers)
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == item_data["title"]
    assert data["description"] == item_data["description"]
    assert data["price"] == item_data["price"]
    assert data["is_active"] is True
    assert "id" in data
    assert "owner" in data


@pytest.mark.asyncio
async def test_get_items(client: AsyncClient):
    """Test getting all items (public endpoint)."""
    response = await client.get("/api/v1/items/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_my_items(client: AsyncClient, auth_headers):
    """Test getting current user's items."""
    # First create an item
    item_data = {
        "title": "My Item",
        "description": "This is my item",
        "price": 500
    }
    create_response = await client.post("/api/v1/items/", json=item_data, headers=auth_headers)
    assert create_response.status_code == 201
    
    # Then get user's items
    response = await client.get("/api/v1/items/my-items", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(item["title"] == item_data["title"] for item in data)


@pytest.mark.asyncio
async def test_get_item_by_id(client: AsyncClient, auth_headers):
    """Test getting item by ID."""
    # First create an item
    item_data = {
        "title": "Test Item for Get",
        "description": "This item will be retrieved",
        "price": 750
    }
    create_response = await client.post("/api/v1/items/", json=item_data, headers=auth_headers)
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]
    
    # Then get the item
    response = await client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == item_id
    assert data["title"] == item_data["title"]


@pytest.mark.asyncio
async def test_update_item(client: AsyncClient, auth_headers):
    """Test updating an item."""
    # First create an item
    item_data = {
        "title": "Original Title",
        "description": "Original description",
        "price": 1000
    }
    create_response = await client.post("/api/v1/items/", json=item_data, headers=auth_headers)
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]
    
    # Then update the item
    update_data = {
        "title": "Updated Title",
        "price": 1500
    }
    response = await client.put(f"/api/v1/items/{item_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["price"] == update_data["price"]
    assert data["description"] == item_data["description"]  # Should remain unchanged


@pytest.mark.asyncio
async def test_delete_item(client: AsyncClient, auth_headers):
    """Test deleting an item."""
    # First create an item
    item_data = {
        "title": "Item to Delete",
        "description": "This item will be deleted",
        "price": 500
    }
    create_response = await client.post("/api/v1/items/", json=item_data, headers=auth_headers)
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]
    
    # Then delete the item
    response = await client.delete(f"/api/v1/items/{item_id}", headers=auth_headers)
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]
    
    # Verify item is deleted
    get_response = await client.get(f"/api/v1/items/{item_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_create_item_unauthorized(client: AsyncClient):
    """Test creating item without authentication."""
    item_data = {
        "title": "Unauthorized Item",
        "description": "This should fail",
        "price": 1000
    }
    response = await client.post("/api/v1/items/", json=item_data)
    assert response.status_code == 401
