import graphene as gp
from src import db, bcrypt
from src.schemas.book import Book
from secrets import token_hex
from src import models

class User(gp.ObjectType):
    id = gp.ID(required=True)
    name = gp.String()
    email = gp.String()
    password = gp.String()
    verified = gp.Int()
    books = gp.List(Book)


class Query(gp.ObjectType):
    user = gp.Field(User)
    user_by_id = gp.Field(User, id=gp.ID(required=True))
    user_by_email = gp.Field(User, email=gp.String(required=True))
    allusers = gp.List(User)

    def resolve_user_by_id(root, info, id):
        cursor = db.connection.cursor()
        statement = "select * from users where id = '{}'".format(id)
        cursor.execute(statement)
        record = cursor.fetchone()
        return record

    def resolve_user_by_email(root, info, email):
        db_session = db.session()
        record = db_session.query(models.User).all()
        # cursor = db.connection.cursor()
        # statement = "select * from users where email = '{}'".format(email)
        # cursor.execute(statement)
        # record = cursor.fetchone()
        return record

    def resolve_allusers(root, info):
        db_session = db.session()
        records = db_session.query(models.User).all()
        db_session.close()
        return records


class CreateUser(gp.Mutation):
    class Arguments:
        name = gp.String()
        email = gp.String()
        password = gp.String()

    Output = User

    def mutate(root, info, name, email,
                password):

        user_dict = {
            'username': name,
            'email': email,
            'password': bcrypt.generate_password_hash(password).decode('utf8')
        }

        new_user = models.User(**user_dict)

        db_session = db.session()
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)

        return new_user

class UpdateUser(gp.Mutation):
    class Arguments:
        id = gp.ID(required=True)
        name = gp.String(default_value=False)
        email = gp.String(default_value=False)
        books = gp.List(gp.String,default_value=False)

    Output = User

    def mutate(root, info, id,
            name, email, books):

        statement = "select * from users where id = '{}'".format(id)

        cursor = db.connection.cursor()
        cursor.execute(statement)
        record = cursor.fetchone()

        if name:
            record['name'] = name

        if email:
            record['email'] = email

        if email:
            record['books'] = books

        update_statement = """ UPDATE users
        SET
            name = %s,
            email = %s,
            books = %s,
            moddate = CURRENT_TIMESTAMP()
        WHERE id = %s
        """

        updates = (
            record['name'], record['email'],
            record['books'], record['id']
        )


        cursor.execute(update_statement, updates)
        db.connection.commit()
        return record

class DeleteUser(gp.Mutation):
    class Arguments:
        id = gp.ID(required=True)

    Output = User

    def mutate(root, info, id):
        cursor = db.connection.cursor()
        statement = "select * from users where id = '{}'".format(id)
        cursor.execute(statement)
        record = cursor.fetchone()

        delete_statement = "DELETE FROM users WHERE id = '{}' ".format(id)

        cursor = db.connection.cursor()
        cursor.execute(delete_statement)
        db.connection.commit()
        return record

class VerifyUser(gp.Mutation):
    class Arguments:
        id = gp.ID(required=True)

    Output = User

    def mutate(root, info, id):
        pass

class Mutation(gp.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

schema = gp.Schema(
    query=Query,
    mutation=Mutation,
    # auto_camelcase=False
)