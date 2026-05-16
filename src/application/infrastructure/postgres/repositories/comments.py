from typing import List, Type

from src.application.core.exceptions.database_exceptions import (CommentAlreadyExistsException,
                                                 CommentNotFoundException)
from src.application.infrastructure.postgres.models.comments import Comment as CommentModel
from src.application.schemas.comments import CommentCreate, CommentUpdateData
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class CommentRepository:
    def __init__(self):
        self._model: Type[CommentModel] = CommentModel

    async def get_by_id(self, session: AsyncSession, comment_id: int) -> CommentModel:
        try:
            query = select(self._model).where(self._model.id == comment_id)
            comment = await session.scalar(query)
            if not comment:
                raise CommentNotFoundException(comment_id=comment_id)

            return comment
        except SQLAlchemyError:
            raise CommentNotFoundException(comment_id=comment_id)

    async def get_by_post(
        self, session: AsyncSession, post_id: int, only_published: bool = True
    ) -> List[CommentModel]:
        try:
            query = select(self._model).where(self._model.post_id == post_id)

            if only_published:
                query = query.where(self._model.is_published)

            query = query.order_by(self._model.created_at)
            return list(await session.scalars(query))
        except SQLAlchemyError:
            return []

    async def create(
        self, session: AsyncSession, comment: CommentCreate, author_id: int
    ) -> CommentModel:

        comment_data = comment.model_dump()
        comment_data["author_id"] = author_id

        query = (insert(self._model)
                 .values(**comment_data)
                 .returning(self._model))

        try:
            comment_obj = await session.scalar(query)
            await session.commit()
            return comment_obj
        except IntegrityError:
            await session.rollback()
            raise CommentAlreadyExistsException()
        except SQLAlchemyError:
            await session.rollback()
            raise CommentAlreadyExistsException()

    async def update(
        self,
        session: AsyncSession,
        comment_id: int,
        user_id: int,
        comment_data: CommentUpdateData,
    ) -> CommentModel:
        try:
            comment = self.get_by_id(session, comment_id)

            if comment.author_id != user_id:
                raise PermissionError(
                    "You do not have permission to edit this comment")

            update_values = {
                k: v for k, v in comment_data.model_dump().items() if v is not None
            }

            for key, value in update_values.items():
                setattr(comment, key, value)

            await session.commit()
            return comment
        except SQLAlchemyError:
            await session.rollback()
            raise CommentNotFoundException(comment_id=comment_id)

    async def delete(self, session: AsyncSession, comment_id: int, user_id: int) -> None:
        try:
            comment = self.get_by_id(session, comment_id)

            if comment.author_id != user_id:
                raise PermissionError(
                    "You do not have permission to delete this comment")

            await session.delete(comment)
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()
            raise CommentNotFoundException(comment_id=comment_id)
