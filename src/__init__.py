from flask import Flask

app = Flask(__name__)

@app.route('/api/healthcheck')
def healthcheck():
    return {
        "status" : "good"
    }

