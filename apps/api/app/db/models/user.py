from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from app.core.security import get_password_hash
from app.db.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, nullable=False)  # "student", "teacher", "principal"

    def hash_password(self, password: str) -> str:
        return get_password_hash(password)
