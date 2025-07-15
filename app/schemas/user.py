from pydantic import BaseModel, EmailStr


class UserBases(BaseModel):
    email: EmailStr


class UserCreate(UserBases):
    password: str


class User(UserBases):
    id: int

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    email: str | None = None


class UserInDB(User):
    hashed_password: str