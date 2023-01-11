from src.database import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(40), nullable=False)
    email = Column(String(40), nullable=False, unique=True)
    password = Column(String(40), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    modified_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(40), nullable=False)
    
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    modified_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(40), nullable=False)
    subtitle = Column(String(40), nullable=True)
    description = Column(String(40), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    modified_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    author_id = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"), nullable=False)
    author = relationship("Author")
