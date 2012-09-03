from flask import Flask, render_template
import config
from hipflask import HipFlask

#Setup our app and database
app = Flask(__name__)

hipflask = HipFlask(app,
    secret_key=config.SECRET_KEY,
    db_url=config.DB_URL)

db = hipflask.db


@app.route('/')
def index():
    return render_template('index.html')
