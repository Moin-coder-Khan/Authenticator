
from pydantic import BaseModel, EmailStr,Field


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    is_active: bool
    role:str

    model_config = {
        "from_attributes": True
    }



class UserUpdate(BaseModel):
    full_name: str | None = Field(
        default=None,
        min_length=3,
        max_length=50
    )

    email: EmailStr | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenWithRefresh(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str