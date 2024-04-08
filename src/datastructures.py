from database import Base


class UsernamePasswordForm(Base):
    username: str
    password: str


class UserForm(UsernamePasswordForm):
    email: str = None
    full_name: str = None
    user_type: str


class UserUpdateForm(Base):
    username: str
    email: str = None
    full_name: str = None
    user_type: str = None


class User(Base):
    id: int
    username: str
    email: str = None
    full_name: str = None
    user_type: str
    hashed_password: str
    created_by: int
