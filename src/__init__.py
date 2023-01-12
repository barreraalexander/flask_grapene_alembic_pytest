from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_graphql import GraphQLView
from src import models
from src.database import engine
from src.config import settings

# from src.schemas.book import schema as book_schema
# from src.schemas.user import schema as user_schema

# models.Base.metadata.create_all(bind=engine)

bcrypt = Bcrypt()
# db = SQLAlchemy()
db = SQLAlchemy(metadata=models.Base.metadata)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

    
    @app.route('/api/healthcheck')
    def healthcheck():
        return {
            "status" : "good"
        }

    
    db.init_app(app)
    bcrypt.init_app(app)


    from src.blueprints.graphql.routes import router as graphql_router
    # from src.schemas.book import schema as book_schema
    from src.schemas.user import schema as user_schema
    from src.schemas.author import schema as author_schema

    app.register_blueprint(graphql_router)
    
    # app.add_url_rule('/graphiql', view_func=GraphQLView.as_view('graphql', schema=author_schema, graphiql=True))
    # app.add_url_rule('/graphiql', view_func=GraphQLView.as_view('graphql', schema=user_schema, graphiql=True))
    # app.add_url_rule('/author', view_func=GraphQLView.as_view('graphql', schema=author_schema, graphiql=True))
    # print ((db.metadata.tables))
    # db.create_all()
    models.Base.metadata.create_all(bind=engine)

    return app