from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.core.database import get_db
from app.repositories import ItemRepository
from app.schemas import Item, ItemCreate, ItemUpdate, ItemResponse
from app.api.v1.auth import get_current_user
from app.models import User as UserModel

router = APIRouter()


@router.get("/", response_model=List[ItemResponse])
async def read_items(
    skip: int = 0,
    limit: int = 100,
    owner_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    """Get all items (public endpoint)."""
    item_repo = ItemRepository(db)
    items = await item_repo.get_multi(skip=skip, limit=limit, owner_id=owner_id)
    return items


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Create a new item (requires authentication)."""
    item_repo = ItemRepository(db)
    return await item_repo.create(item_create=item, owner_id=current_user.id)


@router.get("/my-items", response_model=List[ItemResponse])
async def read_my_items(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Get current user's items."""
    item_repo = ItemRepository(db)
    items = await item_repo.get_multi(skip=skip, limit=limit, owner_id=current_user.id)
    return items


@router.get("/{item_id}", response_model=ItemResponse)
async def read_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific item by ID (public endpoint)."""
    item_repo = ItemRepository(db)
    db_item = await item_repo.get_by_id(item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item_update: ItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Update an item (only the owner can update)."""
    item_repo = ItemRepository(db)
    
    # Check if item exists and user owns it
    db_item = await item_repo.get_by_id(item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if db_item.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    updated_item = await item_repo.update(item_id=item_id, item_update=item_update)
    return updated_item


@router.delete("/{item_id}")
async def delete_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Delete an item (only the owner can delete)."""
    item_repo = ItemRepository(db)
    
    # Check if item exists and user owns it
    db_item = await item_repo.get_by_id(item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if db_item.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    success = await item_repo.delete(item_id=item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
