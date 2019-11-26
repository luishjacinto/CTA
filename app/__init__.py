# -*- coding: utf-8 -*-
__version__ = '0.1'
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.controllers import *


db = SQLAlchemy()

app = Flask('app')
app.config['SECRET_KEY'] = 'random'
app.config['UPLOAD_FOLDER'] = 'app/static/uploads/'
app.debug = True