from datetime import date, datetime
from uuid import UUID
from typing import Optional, List

from pydantic import BaseModel, Field

from .address_dto import AddressDTO


class SignInReq(BaseModel):
    username: str
    password: str


class SignInRes(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserDTO(BaseModel):
    id: UUID
    username: str
    email: str

    phone: Optional[str] = None
    birth_date: Optional[date] = None
    avatar_url: Optional[str] = None

    addresses: List[AddressDTO] = Field(default_factory=list)

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class SignedInUserRes(UserDTO):
    pass

class SignUpReq(BaseModel):
    username: str
    email: str
    password: str

class UpdateProfileReq(BaseModel):
    # This matches the payload the frontend sends for PUT /me/user
    email: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    birth_date: Optional[date] = None

class GoogleLoginReq(BaseModel):
    id_token: str = Field(
        ...,
        description="Google ID token returned by Google login"
    )

class PublicUserRes(BaseModel):
    """Public user information (safe to expose)"""
    id: UUID
    username: str
    avatar_url: Optional[str] = None