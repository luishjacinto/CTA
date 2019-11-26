# -*- coding: utf-8 -*-
from flask import render_template,Blueprint,redirect,request,session,flash,url_for
import hashlib
import datetime
from app import db
from app.models.Arquivo import Arquivo
from app.models.Foto import Foto
from app.models.Noticia import Noticia
from app.models.Repositorio import Repositorio
from app.models.Tarefa import Tarefa
from app.models.Usuario import Usuario
from app.models.Projeto import Projeto

def check_login(tipo):
    if tipo == 0:# se for usuario
        if 'logado' in session:
            if session['logado'] == 'administrador':
                return False
            else:
                return True
        else:
            return False
    elif tipo == 1:# se for administrador
        if 'logado' in session:
            if session['logado'] == 'usuario':
                return False
            else:
                return True
        else:
            return False
    elif tipo == 2:# se não pode estar logado
        if 'logado' in session:
            return False
        else:
            return True
    else:
        pass

def pertence_projeto(usuario, projeto):
    if usuario in projeto.usuarios:
        projeto.pertence = True
        return True
    else:
        return False

def pertence_tarefa_projeto(usuario, projeto):
    for tarefa in projeto.tarefas:
        if usuario in tarefa.usuarios:
            tarefa.pertence = True


def pertence_tarefa(usuario, tarefa):
    if usuario in tarefa.usuarios:
        return True
    else:
        return False