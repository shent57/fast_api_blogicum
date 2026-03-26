from datetime import datetime

from infrastructure.sqlite.database import Base
from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column


class Post(Base):
    __tablename__ = "blog_post"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    text: Mapped[str] = mapped_column(Text, nullable=False, default="")
    pub_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    image: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    created_at: Mapped[str] = mapped_column(DateTime, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("blog_myuser.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("blog_category.id"), nullable=False
    )
    location_id: Mapped[int] = mapped_column(
        ForeignKey("blog_location.id"), nullable=False
    )
