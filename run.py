import app
import os
from app import db
from flask import Flask
from flask import Blueprint
from app.models import *

from app.controllers.nologin import nologin
from app.controllers.projeto import projeto
from app.controllers.usuario import usuario
from app.controllers.repositorio import repositorio
from app.controllers.noticia import noticia
from app.controllers.tarefa import tarefa
from app.controllers.foto import foto
from app.controllers.arquivo import arquivo

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.register_blueprint(foto)
app.register_blueprint(nologin)
app.register_blueprint(projeto)
app.register_blueprint(arquivo)
app.register_blueprint(usuario)
app.register_blueprint(repositorio)
app.register_blueprint(noticia)
app.register_blueprint(tarefa)


uri= "postgresql://postgres:postgres@localhost:5432/CTA"
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, port=5000)