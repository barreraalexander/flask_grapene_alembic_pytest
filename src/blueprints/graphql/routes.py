from flask import Blueprint, request
# from flask_login import current_user
from src.schemas.book import schema as BookSchema
from src.schemas.user import schema as UserSchema
from src.schemas.author import schema as AuthorSchema
# from src.blueprints.graphql import RES_DICTS
import json

router = Blueprint('graphql', __name__,
    url_prefix="/graphql")


@router.route('/book_ep', methods=['POST', 'GET'])
def book_ep():
    if request.method == "POST":
        data = json.loads(request.data)
        element = BookSchema.execute(data['query'])
        if element.errors:
            print (element.errors)
            return element.errors
            # return RES_DICTS['error']
        
    return element.data, 200


@router.route('/user_ep', methods=['POST', 'GET'])
def user_ep():
    if request.method == "POST":
        data = json.loads(request.data)
        element = UserSchema.execute(data['query'])
        if element.errors:
            print ('ERROR \n')
            print (element.errors)
            # return RES_DICTS['error']
            return element.errors
        
    return element.data, 200

@router.route('/author_ep', methods=['POST'])
def author_ep():
    if request.method == "POST":
        data = json.loads(request.data)
        element = AuthorSchema.execute(data['query'])
        if element.errors:
            print ('ERROR \n')
            print (element.errors)
            return element.errors
        
    return element.data, 200
