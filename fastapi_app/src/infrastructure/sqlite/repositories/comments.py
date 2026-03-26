from typing import List, Type

from core.exceptions.database_exceptions import (PostAlreadyExistsException,
                                                 PostNotFoundException)
from infrastructure.sqlite.models.comments import Comment as CommentModel
from schemas.comments import CommentCreate, CommentUpdateData
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


class CommentRepository:
    def __init__(self):
        self._model: Type[CommentModel] = CommentModel

    def get_by_id(self, session: Session, comment_id: int) -> CommentModel:
        query = select(self._model).where(self._model.id == comment_id)
        comment = session.scalar(query)
        if not comment:
            raise PostNotFoundException

        return comment

    def get_by_post(
        self, session: Session, post_id: int, only_published: bool = True
    ) -> List[CommentModel]:
        query = select(self._model).where(self._model.post_id == post_id)

        if only_published:
            query = query.where(self._model.is_published)

        query = query.order_by(self._model.created_at)
        return list(session.scalars(query))

    def create(
        self, session: Session, comment: CommentCreate, author_id: int
    ) -> CommentModel:

        comment_data = comment.model_dump()
        comment_data["author_id"] = author_id

        query = (insert(self._model)
                 .values(**comment_data)
                 .returning(self._model))

        try:
            comment = session.scalar(query)
        except IntegrityError:
            raise PostAlreadyExistsException()

        return comment

    def update(
        self,
        session: Session,
        comment_id: int,
        user_id: int,
        comment_data: CommentUpdateData,
    ) -> CommentModel:
        comment = self.get_by_id(session, comment_id)

        if comment.author_id != user_id:
            raise PermissionError(
                "You do not have permission to edit this comment")

        update_values = {
            k: v for k, v in comment_data.model_dump().items() if v is not None
        }

        for key, value in update_values.items():
            setattr(comment, key, value)

        return comment

    def delete(self, session: Session, comment_id: int, user_id: int) -> None:
        comment = self.get_by_id(session, comment_id)

        if comment.author_id != user_id:
            raise PermissionError(
                "You do not have permission to delete this comment")

        session.delete(comment)
