import graphene as gp
from flask import abort
from src import db, bcrypt, models
from datetime import datetime

class User(gp.ObjectType):
    id = gp.ID(required=True)
    name = gp.String()
    email = gp.String()
    password = gp.String()
    created_at = gp.Date()
    modified_at = gp.Date()

class DeleteUserObject(gp.ObjectType):
    status_code = gp.Int()
    status = gp.String()

class Query(gp.ObjectType):
    user = gp.Field(User)
    user_by_id = gp.Field(User, id=gp.ID(required=True))
    user_by_email = gp.Field(User, email=gp.String(required=True))
    allusers = gp.List(User)

    def resolve_user_by_id(root, info, id):
        db_session = db.session()
        record = db_session.query(models.User).filter(models.User.id == id).first()
        print (record)
        print (record.created_at)
        print (type(record.created_at))
        db_session.close()
        return record

    def resolve_user_by_email(root, info, email):
        db_session = db.session()
        record = db_session.query(models.User).filter(models.User.email == email).first()
        db_session.close()
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

    def mutate(root, info, name, email, password):

        user_dict = {
            'name': name,
            'email': email,
            'password': bcrypt.generate_password_hash(password).decode('utf8'),
        }

        new_user = models.User(**user_dict)

        db_session = db.session()
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)
        db_session.close()

        return new_user

class UpdateUser(gp.Mutation):
    class Arguments:
        id = gp.ID(required=True)
        name = gp.String(default_value=False)
        email = gp.String(default_value=False)

    Output = User

    def mutate(root, info, id, name, email):
        db_session = db.session()

        record_query = db_session.query(models.User).filter(models.User.id == id)

        record = record_query.first()

        if record == None:
            abort(404, description='Record Not Found')

        updated_record = {}
        if name:
            updated_record['name'] = name

        if email:
            updated_record['email'] = email

        updated_record['modified_at'] = datetime.utcnow()
        record_query.update(updated_record, synchronize_session=False)
        db_session.commit()
        updated_record = record_query.first()
        db_session.close()

        return updated_record

class DeleteUser(gp.Mutation):
    class Arguments:
        id = gp.ID(required=True)

    Output = DeleteUserObject

    def mutate(root, info, id):
        db_session = db.session()

        record_query = db_session.query(models.User).filter(models.User.id == id)

        record = record_query.first()

        if record == None:
            abort(404, description='Record Not Found')
        
        record_query.delete(synchronize_session=False)
        db_session.commit()
        
        deleted_user = {
            'status': f'Successfully Deleted User {id}',
            'status_code': 200
        }

        return deleted_user

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
    mutation=Mutation
)