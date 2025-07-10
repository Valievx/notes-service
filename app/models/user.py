from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
import enum


class Role(str, enum.Enum):
    USER = "User"
    ADMIN = "Admin"


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(256), nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.USER)

    notes: Mapped[list["Note"]] = relationship("Note", back_populates="owner")
