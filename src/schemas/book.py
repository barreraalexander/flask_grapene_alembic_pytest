import graphene as gp
from src import db, models
from secrets import token_hex

class Book(gp.ObjectType):
    id = gp.ID(required=True)
    author_id = gp.ID(required=True)
    title = gp.String()
    description  = gp.String()
    # urls = gp.List(gp.String)
    # background_gradient = gp.String(default_value='none')

    created_at = gp.Date()
    modified_at = gp.Date()

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
        urls = gp.String(default_value=False)
        #background_gradient = gp.String(default_value=False)

    Output = Book

    def mutate(root, info, id,
            author_id, title, description, urls, background_gradient):
        statement = "select * from books where id = '{}'".format(id)
        
        cursor = db.connection.cursor()
        cursor.execute(statement)
        record = cursor.fetchone()

        if title:
            record['title'] = title

        if description:
            record['description'] = description

        if urls:
            record['urls'] = urls

        if background_gradient:
            record['background_gradient'] = background_gradient

        update_statement = """UPDATE books
        SET
            title = %s,
            description = %s,
            urls = %s,
            background_gradient = %s,
            moddate = CURRENT_TIMESTAMP()
        WHERE id = %s 
        """

        updates = (
            record['title'], record['description'],
            record['urls'], record['background_gradient'],
            record['id']
        )

        cursor.execute(update_statement, updates)
        db.connection.commit()
        return record

class DeleteBook(gp.Mutation):
    class Arguments:
        id = gp.ID(required=True)

    Output = Book


    def mutate(root, info, id):
        cursor = db.connection.cursor()
        statement = "select * from books where id = '{}'".format(id)
        cursor.execute(statement)
        record = cursor.fetchone()

        delete_statement = "DELETE FROM books WHERE id = '{}' ".format(id)

        cursor = db.connection.cursor()
        cursor.execute(delete_statement)
        db.connection.commit()
        return record

class Mutation(gp.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()

schema = gp.Schema(
    query=Query,
    mutation=Mutation, 
    )