import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(120), nullable=False, unique=True)
    firstname = Column(String(120), nullable=True)
    lastname = Column(String(120), nullable=True)
    email = Column(String(120), nullable=False, unique=True)

    posts = relationship('Post', backref='user')
    followers = relationship('User', foreign_keys='Follower.user_to_id', back_populates='followed_user')
    following = relationship('User', foreign_keys='Follower.user_from_id', back_populates='follower_user')

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    comments = relationship('Comment', backref='post')


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(256), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)

    author = relationship('User')

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(Enum('image', 'video'), nullable=False)
    url = Column(String(120), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)

    post = relationship('Post', backref='media')


class Follower(Base):
    __tablename__ = 'followers'
    user_from_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user_to_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    follower_user = relationship('User', foreign_keys='user_from_id', back_populates='following')
    followed_user = relationship('User', foreign_keys='user_to_id', back_populates='followers')

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
