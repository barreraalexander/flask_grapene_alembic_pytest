import graphene as gp
from graphene_sqlalchemy import SQLAlchemyConnectionField

from src.schemas.book import schema as book_schema
from src.schemas.user import schema as user_schema

class Query(gp.ObjectType):
    # node = gp.relay.Node.Field()
    pass

    # books = gp.relay.Node.Field(book_schema)
    # book_schema = gp.Field()
