import pytest
from src import create_app
from src.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src import models
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base


POSTGRES_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(POSTGRES_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# @pytest.fixture()
# def db_session():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @pytest.fixture()
# def db_session():
#     db = SQLAlchemy(metadata=models.Base.metadata)
#     return db
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)
    # db = TestingSessionLocal()
    # try:
    #     yield db
    # finally:
    #     db.close()

@pytest.fixture()
def client():
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # session = db_session
        # Establish an application context
        # session.init_app(testing_client)
        # db = db_session
        # db.init_app(testing_client)
        with flask_app.app_context():
            
            yield testing_client  # this is where the testing happens!


# @pytest.fixture()
# def app():
#     # models.Base = 
#     # models.Base.metadata = Base.metadata
#     # db = SQLAlchemy(metadata=models.Base.metadata)


#     app = create_app()
#     # db.init_app(app)

#     app.config.update({'TESTING' : True})


#     yield app


# @pytest.fixture()
# def client(app):
#     return app.test_client()