from infrastructure.sqlite.database import Base
from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column


class Location(Base):
    __tablename__ = "blog_location"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    is_published: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False, 
        default=True)
    created_at: Mapped[str] = mapped_column(DateTime, nullable=False)
