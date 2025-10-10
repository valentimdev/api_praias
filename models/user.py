from sqlalchemy import Column, Integer, String
from db.session import Base
from auth.cryptography import hash_password


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    refresh_token_hash = Column(String, nullable=True)

    def __init__(self, username: str, password: str, **kwargs):
        self.username = username
        hashed_password = hash_password(password)
        self.hashed_password = hashed_password
        for key, value in kwargs.items():
            setattr(self, key, value)

