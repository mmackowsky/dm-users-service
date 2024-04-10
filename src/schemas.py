from pydantic import BaseModel


class UsernamePasswordForm(BaseModel):
    username: str
    password: str


class UserForm(UsernamePasswordForm):
    email: str = None
    full_name: str = None
    user_type: str = "default"


class UserUpdateForm(BaseModel):
    username: str
    email: str = None
    full_name: str = None
    user_type: str = None


class User(BaseModel):
    id: int
    username: str
    email: str = None
    full_name: str = None
    user_type: str
    hashed_password: str

    class Config:
        orm_mode = True
