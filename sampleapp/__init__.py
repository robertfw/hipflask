from flask import Flask, render_template
import config
from hipflask import HipFlask

#Setup our app and database
app = Flask(__name__)
hipflask = HipFlask(app, config)


@app.route('/')
def index():
    return render_template('index.html')
