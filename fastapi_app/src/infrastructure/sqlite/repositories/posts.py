from typing import Type, List

from sqlalchemy import insert, select, and_, desc
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from infrastructure.sqlite.models.posts import Post as PostModel
from schemas.posts import PostRequestSchema, PostUpdateData
from core.exceptions.database_exceptions import PostNotFoundException, PostAlreadyExistsException


class PostRepository:
    def __init__(self):
        self._model: Type[PostModel] = PostModel

    def get_by_id(self, session: Session, post_id: int) -> PostModel:
        query = (
            select(self._model)
            .where(self._model.id == post_id)
        )

        post = session.scalar(query)
        if not post:
            raise PostNotFoundException()

        return post
    

    def get_published_posts(self, session: Session) -> List[PostModel]:
        query = (
            select(self._model)
            .where(
                and_(
                    self._model.is_published == True,
                    self._model.pub_date <= datetime.now()
                )
            )
            .order_by(desc(self._model.pub_date))
        )

        return list(session.scalars(query))
    
    def get_by_category(self, session: Session, category_id: int, only_published: bool = True) -> List[PostModel]:
        query = (
            select(self._model)
            .where(self._model.category_id == category_id)
        )

        if only_published:
            query = query.where(
                and_(
                    self._model.is_published == True,
                    self._model.pub_date <= datetime.now()
                )
            )

        query = query.order_by(desc(self._model.pub_date))

        return list(session.scalars(query))
    
    def get_by_author(self, session: Session, author_id: int, only_published: bool = True) -> List[PostModel]:
        query = (
            select(self._model)
            .where(self._model.author_id == author_id)
        )

        if only_published:
            query = query.where(
                and_(
                    self._model.is_published == True,
                    self._model.pub_date <= datetime.now()
                )
            )

        query = query.order_by(desc(self._model.pub_date))

        return list(session.scalars(query))
    
    def create(self, session: Session, post: PostRequestSchema, author_id: int) -> PostModel:
        post_data = post.model_dump()
        post_data['author_id'] = author_id
        query = (
            insert(self._model)
            .values(**post_data)
            .returning(self._model)
        )

        try:
            post = session.scalar(query)
        except IntegrityError:
            raise PostAlreadyExistsException()

        return post
    
    def update(self, session: Session, post_id: int, user_id: int, post_data: PostUpdateData, is_staff: bool = False) -> PostModel:
        post = self.get_by_id(session, post_id)

        if post.author_id != user_id and not is_staff:
            raise PermissionError('You do not have permission to edit this post')
        
        update_values = {k: v for k, v in post_data.model_dump().items() if v is not None}

        for key, value in update_values.items():
            setattr(post, key, value)

        session.flush()

        return post
    
    def delete(self, session: Session, post_id: int, user_id: int, is_staff: bool = False) -> None:
        post = self.get_by_id(session, post_id)

        if post.author_id != user_id and not is_staff:
            raise PermissionError('You do not have permission to delete this post')
        
        session.delete(post)