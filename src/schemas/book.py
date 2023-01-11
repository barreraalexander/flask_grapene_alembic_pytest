import graphene as gp
from src import db
from secrets import token_hex

class Book(gp.ObjectType):
    id = gp.ID(required=True)
    user_id = gp.ID(required=True)
    title = gp.String()
    description  = gp.String()
    urls = gp.List(gp.String)
    background_gradient = gp.String(default_value='none')

    moddate = gp.Date()
    upldate = gp.Date()


class Query(gp.ObjectType):
    book = gp.Field(Book)
    book_by_id = gp.Field(Book, id=gp.ID(required=True))
    allbooks = gp.List(Book)

    def resolve_book_by_id(root, info, id):
        cursor = db.connection.cursor()
        statement = "select * from books where id = '{}'".format(id)
        cursor.execute(statement)
        record = cursor.fetchone()
        return record


    def resolve_allbooks(root, info):
        cursor = db.connection.cursor()

        statement = "select * from books"
        cursor.execute(statement)

        records = cursor.fetchall()

        return records

class CreateBook(gp.Mutation):
    class Arguments:
        user_id = gp.ID(required=True)
        title = gp.String()
        description = gp.String()
        urls = gp.List(gp.String)

    Output = Book

    def mutate(root, info, user_id,
                title, description, urls):
        insert_statement = """ INSERT INTO books
            (id, user_id, title, description, urls)
        VALUES
            (%s, %s, %s, %s, %s)
        """

        new_token = token_hex(8)

        insertions = (new_token, user_id, title,
                description, urls)

        cursor = db.connection.cursor()
        cursor.execute(insert_statement, insertions)
        db.connection.commit()

        check_statement = "select * from books where id = '{}'".format(id)
        cursor.execute(check_statement)
        new_record = cursor.fetchone()

        return new_record

class UpdateBook(gp.Mutation):
    class Arguments:
        id = gp.ID(required=True)
        user_id = gp.ID(default_value=False) #should delete this and cascade changes of user id
        title = gp.String(default_value=False)
        description = gp.String(default_value=False)
        urls = gp.String(default_value=False)
        #background_gradient = gp.String(default_value=False)

    Output = Book

    def mutate(root, info, id,
            user_id, title, description, urls, background_gradient):
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
    auto_camelcase=False
    )