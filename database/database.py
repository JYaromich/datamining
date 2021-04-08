# определяет какая бд будет MySql, Postgres, Oracle и т.д.
from sqlalchemy import create_engine
from . import models

from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self, db_url):
        engine = create_engine(db_url)
        models.Base.metadata.create_all(bind=engine)
        self.maker = sessionmaker(bind=engine)

    def _get_or_create(self, session, model, data, unique_field=None):
        instance = None
        if unique_field:
            instance = session.query(model).filter_by(**{unique_field: data[unique_field]}).first()

        if not instance:
            instance = model(**data)

        return instance

    def create_post(self, data):
        session = self.maker()

        post: models.Post = self._get_or_create(session, models.Post, data['post_data'], unique_field='url')
        writer = self._get_or_create(session, models.Writer, data['writer'], unique_field='url')
        tags = [self._get_or_create(session, models.Tag, tag_data, unique_field='url')
                for tag_data in data['tags']]
        comments = [self._get_or_create(session, models.Comment, comment_data)
                     for comment_data in data['comment']]

        post.writer = writer
        post.tags.extend(tags)
        post.comments.extend(comments)

        session.add(post)
        try:
            session.commit()
        except Exception as ex:
            print(ex)
            session.rollback()
        finally:
            session.close()
