from flask import Flask
from src import models
from src.database import engine

models.Base.metadata.create_all(bind=engine)


app = Flask(__name__)



@app.route('/api/healthcheck')
def healthcheck():
    return {
        "status" : "good"
    }

