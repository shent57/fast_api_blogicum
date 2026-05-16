from datetime import datetime
from typing import List, Type

from src.application.core.exceptions.database_exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException)
from src.application.infrastructure.postgres.models.posts import Post as PostModel
from src.application.schemas.posts import PostUpdateData
from sqlalchemy import and_, desc, insert, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class PostRepository:
    def __init__(self):
        self._model: Type[PostModel] = PostModel

    async def get_by_id(self, session: AsyncSession, post_id: int) -> PostModel:
        try:
            query = select(self._model).where(self._model.id == post_id)

            post = await session.scalar(query)
            if not post:
                raise EntityNotFoundException(detail=f"Пост с id='{post_id}' не найден")
            return post
        except SQLAlchemyError:
            raise

    async def get_all(self, session: AsyncSession) ->  list[PostModel]:
        try:
            query = select(self._model)
            return list(await session.scalars(query))
        except SQLAlchemyError:
            raise

    async def get_published_posts(self, session: AsyncSession) -> List[PostModel]:
        try:
            query = (
                select(self._model)
                .where(
                    and_(
                        self._model.is_published, 
                        self._model.pub_date <= datetime.now())
                )
                .order_by(desc(self._model.pub_date))
            )
            return list(await session.scalars(query))
        except SQLAlchemyError:
            raise

    async def get_by_category(
        self, session: AsyncSession, category_id: int, only_published: bool = True
    ) -> List[PostModel]:
        try:
            query = (
                select(self._model)
                .where(self._model.category_id == category_id))

            if only_published:
                query = query.where(
                    and_(
                        self._model.is_published, 
                        self._model.pub_date <= datetime.now())
                )

            query = query.order_by(desc(self._model.pub_date))
            return list(await session.scalars(query))
        except SQLAlchemyError:
            raise

    async def get_by_author(
        self, session: AsyncSession, author_id: int, only_published: bool = True
    ) -> List[PostModel]:
        try:
            query = select(self._model).where(self._model.author_id == author_id)

            if only_published:
                query = query.where(
                    and_(
                        self._model.is_published, 
                        self._model.pub_date <= datetime.now())
                )

            query = query.order_by(desc(self._model.pub_date))
            return list(await session.scalars(query))
        except SQLAlchemyError:
            raise

    async def create(self, session: AsyncSession, post_data: dict) -> PostModel:
        query = insert(self._model).values(**post_data).returning(self._model)

        try:
            post = await session.scalar(query)
            await session.commit()
            return post
        except IntegrityError:
            await session.rollback()
            raise EntityAlreadyExistsException(detail=f"Пост с заголовком '{post_data.get('title')}' уже существует")
        except SQLAlchemyError:
            await session.rollback()
            raise

    async def update(
        self,
        session: AsyncSession,
        post_id: int,
        user_id: int,
        post_data: PostUpdateData,
        is_staff: bool = False,
    ) -> PostModel:
        try:
            post = self.get_by_id(session, post_id)

            if post.author_id != user_id and not is_staff:
                raise PermissionError(
                    "You do not have permission to edit this post")

            update_values = {
                k: v for k, v in post_data.model_dump().items() if v is not None
            }

            for key, value in update_values.items():
                setattr(post, key, value)

            await session.commit()

            return post
        except SQLAlchemyError:
            raise

    async def delete(
        self, 
        session: AsyncSession, 
        post_id: int, 
        user_id: int, 
        is_staff: bool = False
    ) -> None:
        try:
            post = self.get_by_id(session, post_id)

            if post.author_id != user_id and not is_staff:
                raise PermissionError(
                    "You do not have permission to delete this post")

            await session.delete(post)
            await session.commit()
        except SQLAlchemyError:
            raise