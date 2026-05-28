from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, HttpUrl


class PlatformBase(BaseModel):
    name_slug: str
    name: str
    base_url: Optional[HttpUrl] = None
    auth_type: str


class PlatformCreate(PlatformBase):
    pass


class PlatformResponse(PlatformBase):
    id: int

    class Config:
        from_attributes = True


class PlatformAccountBase(BaseModel):
    platform_id: int
    username: str


class PlatformAccountCreate(PlatformAccountBase):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None


class PlatformAccountResponse(PlatformAccountBase):
    id: int
    user_id: UUID
    last_synced_at: Optional[str] = None
    sync_status: str
    metadata: dict

    class Config:
        from_attributes = True