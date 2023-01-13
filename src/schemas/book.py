import graphene as gp
from src import db, models
from flask import abort
from datetime import datetime

class Book(gp.ObjectType):
    id = gp.ID(required=True)
    author_id = gp.ID(required=True)
    title = gp.String()
    description  = gp.String()

    created_at = gp.Date()
    modified_at = gp.Date()

class DeleteBookObject(gp.ObjectType):
    status_code = gp.Int()
    status = gp.String()


class Query(gp.ObjectType):
    book = gp.Field(Book)
    book_by_id = gp.Field(Book, id=gp.ID(required=True))
    allbooks = gp.List(Book)

    def resolve_book_by_id(root, info, id):
        db_session = db.session()
        record = db_session.query(models.Book).filter(models.Book.id == id).first()
        db_session.close()
        return record


    def resolve_allbooks(root, info):
        db_session = db.session()
        records = db_session.query(models.Book).all()
        db_session.close()
        return records



class CreateBook(gp.Mutation):
    class Arguments:
        author_id = gp.ID(required=True)
        title = gp.String(required=True)
        description = gp.String()

    Output = Book

    def mutate(root, info, author_id,
                title, description):

        book_dict = {
            'author_id' : author_id,
            'title' : title,
            'description' : description,
        }

        new_book = models.Book(**book_dict)

        db_session = db.session()
        db_session.add(new_book)
        db_session.commit()
        db_session.refresh(new_book)
        db_session.close()

        return new_book

class UpdateBook(gp.Mutation):
    class Arguments:
        id = gp.ID(required=True)
        author_id = gp.ID(default_value=False) #should delete this and cascade changes of user id
        title = gp.String(default_value=False)
        description = gp.String(default_value=False)

    Output = Book

    def mutate(root, info, id, author_id, title, description):
        db_session = db.session()

        record_query = db_session.query(models.Book).filter(models.Book.id == id)

        record = record_query.first()

        if record == None:
            abort(404, description='Record Not Found')


        updated_record = {}
        if author_id:
            updated_record['author_id'] = author_id

        if title:
            updated_record['title'] = title

        if description:
            updated_record['description'] = description

        updated_record['modified_at'] = datetime.utcnow()
        record_query.update(updated_record, synchronize_session=False)
        db_session.commit()
        updated_record = record_query.first()
        db_session.close()

        return updated_record

class DeleteBook(gp.Mutation):
    class Arguments:
        id = gp.ID(required=True)

    Output = DeleteBookObject


    def mutate(root, info, id):
        db_session = db.session()

        record_query = db_session.query(models.Book).filter(models.Book.id == id)

        record = record_query.first()

        if record == None:
            abort(404, description='Record Not Found')
        
        record_query.delete(synchronize_session=False)
        db_session.commit()
        
        deleted_record = {
            'status': f'Successfully Deleted Author {id}',
            'status_code': 200
        }

        return deleted_record

class Mutation(gp.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()

schema = gp.Schema(
    query=Query,
    mutation=Mutation,
    )