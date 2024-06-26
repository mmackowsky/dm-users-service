from sqlalchemy import Column, Integer, String

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    full_name = Column(String(150), unique=False, nullable=True)
    user_type = Column(String(50), unique=False, nullable=False)
    hashed_password = Column(String(200), unique=True, nullable=False)

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email}, hashed_password={self.hashed_password})>"
