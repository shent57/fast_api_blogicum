from datetime import datetime

from src.infrastructure.sqlite.database import Base
from sqlalchemy import Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column


class Comment(Base):
    __tablename__ = "blog_comment"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, nullable=False, default="")
    pub_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_published: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False, 
        default=True)
    created_at: Mapped[str] = mapped_column(DateTime, nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("blog_myuser.id"), 
        nullable=False)
    post_id: Mapped[int] = mapped_column(
        ForeignKey("blog_post.id"), 
        nullable=False)
