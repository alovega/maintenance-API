from flask import Flask ,jsonify,abort,request
from instance.config import app_config
from maintenance.Request import RequestDao
import json
def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    return app
