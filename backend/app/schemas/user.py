from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    department_id: int
    role_id: int


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class UserResponse(UserBase):
    id: int
    department_id: int
    role_id: int

    model_config = ConfigDict(
        from_attributes=True
    )