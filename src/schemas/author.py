import graphene as gp
from flask import abort
from src import db, models
from src.schemas.book import Book
from datetime import datetime

class Author(gp.ObjectType):
    id = gp.ID(required=True)
    name = gp.String()
    books =  gp.List(Book)

    created_at = gp.Date()
    modified_at = gp.Date()
    # name

class DeleteAuthorObject(gp.ObjectType):
    status_code = gp.Int()
    status = gp.String()


class Query(gp.ObjectType):
    author = gp.Field(Author)
    author_by_id = gp.Field(Author, id=gp.ID(required=True))
    allauthors = gp.List(Author)

    def resolve_author_by_id(root, info, id):
        db_session = db.session()
        record = db_session.query(models.Author).filter(models.Author.id == id).first()
        db_session.close()
        return record

    def resolve_allauthors(root, info):
        db_session = db.session()
        records = db_session.query(models.Author).all()
        db_session.close()
        return records

    

class CreateAuthor(gp.Mutation):
    class Arguments:
        name = gp.String()

    Output = Author

    def mutate(root, info, name):
        author_dict = {
            'name' : name
        }

        new_author = models.Author(**author_dict)

        db_session = db.session()
        db_session.add(new_author)
        db_session.commit()
        db_session.refresh(new_author)
        db_session.close()

        return new_author


class UpdateAuthor(gp.Mutation):
    class Arguments:
        id = gp.ID(required=True)
        name = gp.String(default_value=False)
        
    Output = Author

    def mutate(root, info, id, name):
        db_session = db.session()

        record_query = db_session.query(models.Author).filter(models.Author.id == id)

        record = record_query.first()

        if record == None:
            abort(404, description='Record Not Found')

        updated_record = {}
        if name:
            updated_record['name'] = name


        updated_record['modified_at'] = datetime.utcnow()
        record_query.update(updated_record, synchronize_session=False)
        db_session.commit()
        updated_record = record_query.first()
        db_session.close()

        return updated_record


class DeleteAuthor(gp.Mutation):
    class Arguments:
        id = gp.ID(required=True)

    Output = DeleteAuthorObject

    def mutate(root, info, id):
        db_session = db.session()

        record_query = db_session.query(models.Author).filter(models.Author.id == id)

        record = record_query.first()

        if record == None:
            abort(404, description='Record Not Found')
        
        record_query.delete(synchronize_session=False)
        db_session.commit()
        
        deleted_author = {
            'status': f'Successfully Deleted Author {id}',
            'status_code': 200
        }

        return deleted_author


class Mutation(gp.ObjectType):
    create_author = CreateAuthor.Field()
    update_author = UpdateAuthor.Field()
    delete_author = DeleteAuthor.Field()
    

schema = gp.Schema(
    query=Query,
    mutation=Mutation
)