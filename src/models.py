from src.database import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(40), nullable=False, )
    email = Column(String(40), nullable=False, unique=True)
    password = Column(String(40), nullable=False)
