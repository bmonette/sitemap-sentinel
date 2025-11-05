from pydantic import BaseModel, EmailStr, Field, AnyHttpUrl
from datetime import datetime


class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True   # allow ORM -> schema


class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ProjectIn(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    site_url: AnyHttpUrl
    sitemap_url: AnyHttpUrl


class ProjectOut(BaseModel):
    id: int
    name: str
    site_url: AnyHttpUrl
    sitemap_url: AnyHttpUrl
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    site_url: AnyHttpUrl | None = None
    sitemap_url: AnyHttpUrl | None = None
