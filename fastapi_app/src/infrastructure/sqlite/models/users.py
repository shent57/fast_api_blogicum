from datetime import datetime

from infrastructure.sqlite.database import Base
from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "blog_myuser"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(150), 
        nullable=False, 
        unique=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    first_name: Mapped[str] = mapped_column(
        String(150), 
        nullable=False, 
        default="")
    last_name: Mapped[str] = mapped_column(
        String(150), 
        nullable=False, 
        default="")
    email: Mapped[str] = mapped_column(String(254), nullable=False, default="")
    is_active: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False, 
        default=True)
    is_staff: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False, 
        default=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False, 
        default=False)
    date_joined: Mapped[str] = mapped_column(DateTime, nullable=False)
    last_login: Mapped[datetime | None] = mapped_column(
        DateTime, 
        nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=False, default="")
