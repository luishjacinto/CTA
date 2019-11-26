# -*- coding: utf-8 -*-

import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
import os
from flask import render_template,Blueprint,redirect,request,session,flash,url_for,send_from_directory
from app.models.Arquivo import Arquivo
from app.models.Usuario import Usuario
from app.models.Projeto import Projeto
from datetime import datetime, date
import hashlib
from app import app, db
from uuid import uuid4
from werkzeug.utils import secure_filename
from app.models.forms.formArquivo import formArquivo
from app.controllers.verify import check_login, pertence_projeto

arquivo = Blueprint('arquivo', __name__)

def permitido(extencao): 
    return extencao in ['pdf', 'rar', 'zip', 'doc']

@arquivo.route("/arquivos/<nome>", methods = ['GET', 'POST'])
def arquivos(nome):
    projeto = Projeto.query.filter_by(nome = nome).first()
    if projeto:
        if projeto.arquivos:
            if check_login(0):
                usuario = Usuario.query.get(session['user']['id'])
                if pertence_projeto(usuario, projeto):
                    pass
            else:
                pass
            return render_template('arquivo/arquivos.html',projeto=projeto)
        else:
            flash(u'Projeto não possui arquivos!', 'danger')
            return redirect('/detalhes/'+projeto.nome)
    else:
        flash(u'Projeto não existe!', 'danger')
        return redirect('/inicio')

@arquivo.route('/criar_arquivo/<id_projeto>', methods=['GET', 'POST'])
def criar_arquivo(id_projeto):
    if check_login(0):
        projeto = Projeto.query.get(id_projeto)
        if projeto:
            usuario = Usuario.query.get(session['user']['id'])
            if pertence_projeto(usuario, projeto):
                form = formArquivo()
                if form.validate_on_submit():
                    nome = request.form['nome']
                    arquivo = form.arquivo.data
                    extencao = arquivo.filename.split('.')[-1].lower()
                    data_publicacao = date.today()

                    novo_nome_arquivo = uuid4()
                    is_permitido = permitido(extencao)
                    
                    if is_permitido:
                        novo_nome_arquivo = str(novo_nome_arquivo) + '.' + extencao
                        arquivo_aux = secure_filename(arquivo.filename)

                        diretorio = os.path.join(app.config['UPLOAD_FOLDER']+'arquivos/', arquivo_aux)

                        diretorio_novo = os.path.join(app.config['UPLOAD_FOLDER']+'arquivos/', novo_nome_arquivo)

                        arquivo.save(diretorio)
                        os.rename(diretorio, diretorio_novo)

                        arquivo = Arquivo(nome = nome+'.'+extencao, data_publicacao = data_publicacao, id_usuario = session['user']['id'], id_projeto=projeto.id, caminho = novo_nome_arquivo)

                        projeto.arquivos.append(arquivo)
                        db.session.add(projeto)
                        db.session.commit()
                        flash(u'Arquivo adicionado com sucesso!', 'success')
                        return redirect('/arquivos/' + projeto.nome)
                    else:
                        flash(u'Extensão de arquivo não permitida!', 'danger')
                        return render_template('arquivo/criar.html',form=form,projeto=projeto)                     
                return render_template('arquivo/criar.html',form=form,projeto=projeto)
            else:
                flash(u'Você não faz parte deste projeto!', 'danger')
                return redirect('/painel_usuario')
        else:
            flash(u'Projeto não existe!', 'danger')
            return redirect('/painel_usuario')          
    else:
        return redirect('/entrar')

@arquivo.route('/deletar_arquivo/<nome_projeto>/<id_arquivo>', methods = ['GET', 'POST'])
def excluir_arquivo(nome_projeto,id_arquivo):
    if check_login(0):
        projeto = Projeto.query.filter_by(nome = nome_projeto).first()
        if projeto:
            usuario = Usuario.query.get(session['user']['id'])
            if pertence_projeto(usuario, projeto):
                arquivo = Arquivo.query.get(id_arquivo)
                if arquivo:
                    if arquivo.id_projeto == projeto.id:
                        if arquivo.id_usuario == session['user']['id'] or session['user']['id'] == projeto.id_autor:
                            os.remove(app.config['UPLOAD_FOLDER']+'arquivos/'+arquivo.caminho)
                            db.session.delete(arquivo)
                            db.session.commit()
                            flash(u'Arquivo deletado com sucesso!', 'success')
                            return redirect('/detalhes/'+projeto.nome)
                        else:
                            flash(u'Você não tem permissão para realizar a ação!', 'danger')
                            return redirect('/entrar')
                    else:
                        flash(u'Arquivo não está vinculada ao projeto!', 'danger')
                        return redirect('/noticias/'+projeto.nome)
                else:
                    flash(u'Arquivo não existe!', 'danger')
                    redirect('/painel_usuario')
            else:
                flash(u'Você não faz parte deste projeto!', 'danger')
                return redirect('/painel_usuario')
        else:
            flash(u'Projeto não existe!', 'danger')
            return redirect('/painel_usuario')
    else:
        return redirect('/entrar') 

@arquivo.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory=app.config['UPLOAD_FOLDER']+'arquivos/', filename=filename)
