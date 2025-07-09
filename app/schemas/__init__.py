from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


# User schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class User(UserInDB):
    pass


# Item schemas
class ItemBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[int] = Field(None, ge=0)  # Price in cents


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class ItemInDB(ItemBase):
    id: int
    is_active: bool
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class Item(ItemInDB):
    owner: Optional[User] = None


# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


# Response schemas
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime
    # Don't include items by default to avoid lazy loading issues
    # items: List[Item] = []

    model_config = ConfigDict(from_attributes=True)


class UserWithItemsResponse(UserResponse):
    """User response that includes items - only use when items are explicitly loaded."""
    items: List["Item"] = []


class ItemResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: Optional[int]
    is_active: bool
    created_at: datetime
    owner: Optional[UserResponse] = None

    model_config = ConfigDict(from_attributes=True)
