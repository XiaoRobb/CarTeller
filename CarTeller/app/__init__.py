import logging
from logging.handlers import RotatingFileHandler
from imp import reload
import sys
import os
from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

reload(sys)
# sys.setdefaultencoding('utf-8')

app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app, supports_credentials=True)
app.secret_key=os.urandom(24)
app.config.from_object("config")
db = SQLAlchemy(app)

from app import views,models