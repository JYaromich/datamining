from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table

Base = declarative_base()

tag_post = Table(
    'tag_post',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('post.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False, unique=False)
    first_image_url = Column(String, nullable=True)
    date = Column(DateTime, nullable=True, unique=False)
    writer_id = Column(Integer, ForeignKey('writer.id'))
    writer = relationship('Writer')
    tags = relationship('Tag', secondary=tag_post)
    comments = relationship('Comment')


class Writer(Base):
    __tablename__ = 'writer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, unique=True, nullable=False)
    name = Column(String, unique=False, nullable=False)
    posts = relationship(Post)


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, unique=True, nullable=False)
    name = Column(String, unique=False, nullable=False)
    posts = relationship(Post, secondary=tag_post)


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, autoincrement=False, nullable=False)
    parent_id = Column(Integer, ForeignKey('comment.id'))
    author = Column(String, unique=False, nullable=False)
    text = Column(String)
    post_id = Column(Integer, ForeignKey(Post.id))
    post = relationship(Post)
    answer_on = relationship(lambda: Comment, remote_side=id, backref='parent_comment')
