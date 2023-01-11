from flask import Blueprint, request
from flask_login import current_user
from server.schemas.book import schema as BookSchema
from server.schemas.user import schema as UserSchema
from server.blueprints.graphql import RES_DICTS
import json
