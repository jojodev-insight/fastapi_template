from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional, List

from app.models import User, Item
from app.schemas import UserCreate, UserUpdate, ItemCreate, ItemUpdate
from app.core.security import get_password_hash, verify_password


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(
            select(User).options(selectinload(User.items)).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[User]:
        result = await self.db.execute(
            select(User).options(selectinload(User.items)).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def create(self, user_data) -> User:
        """Create a new user. Accepts either UserCreate or dict."""
        if isinstance(user_data, UserCreate):
            # Handle UserCreate schema - hash the password
            hashed_password = get_password_hash(user_data.password)
            db_user = User(
                username=user_data.username,
                email=user_data.email,
                full_name=user_data.full_name,
                hashed_password=hashed_password,
            )
        else:
            # Handle dict input (for tests and direct creation)
            db_user = User(**user_data)
        
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def update(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        db_user = await self.get_by_id(user_id)
        if not db_user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)

        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def delete(self, user_id: int) -> bool:
        db_user = await self.get_by_id(user_id)
        if not db_user:
            return False

        await self.db.delete(db_user)
        await self.db.commit()
        return True

    async def authenticate(self, username: str, password: str) -> Optional[User]:
        user = await self.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


class ItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, item_id: int) -> Optional[Item]:
        result = await self.db.execute(
            select(Item).options(selectinload(Item.owner)).where(Item.id == item_id)
        )
        return result.scalar_one_or_none()

    async def get_multi(
        self, skip: int = 0, limit: int = 100, owner_id: Optional[int] = None
    ) -> List[Item]:
        query = select(Item).options(selectinload(Item.owner))
        if owner_id:
            query = query.where(Item.owner_id == owner_id)
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create(self, item_create: ItemCreate, owner_id: int) -> Item:
        db_item = Item(
            title=item_create.title,
            description=item_create.description,
            price=item_create.price,
            owner_id=owner_id,
        )
        self.db.add(db_item)
        await self.db.commit()
        await self.db.refresh(db_item)
        return db_item

    async def update(self, item_id: int, item_update: ItemUpdate) -> Optional[Item]:
        db_item = await self.get_by_id(item_id)
        if not db_item:
            return None

        update_data = item_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)

        await self.db.commit()
        await self.db.refresh(db_item)
        return db_item

    async def delete(self, item_id: int) -> bool:
        db_item = await self.get_by_id(item_id)
        if not db_item:
            return False

        await self.db.delete(db_item)
        await self.db.commit()
        return True
