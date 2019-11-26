# -*- coding: utf-8 -*-
import os
from flask import render_template,Blueprint,redirect,request,session,flash,url_for,send_from_directory
from app.models.Foto import Foto
from app.models.Usuario import Usuario
from app.models.Projeto import Projeto
from datetime import datetime, date
import hashlib
from app import app, db
from uuid import uuid4
from werkzeug.utils import secure_filename
from app.models.forms.formFoto import formFoto
from app.controllers.verify import check_login, pertence_projeto


foto = Blueprint('foto', __name__)

def permitido(extencao): 
    return extencao in ['gif', 'png', 'jpeg', 'jpg']

#################verificar se o usuario é dono do foto


@foto.route("/fotos/<nome>", methods = ['GET', 'POST'])
def fotos(nome):
    projeto = Projeto.query.filter_by(nome = nome).first()
    if projeto:
        if projeto.fotos:
            if check_login(0):
                usuario = Usuario.query.get(session['user']['id'])
                if pertence_projeto(usuario, projeto):
                    pass
            else:
                pass
            return render_template('foto/fotos.html',projeto=projeto)
        else:
            flash(u'Projeto não possui fotos!', 'danger')
            return redirect('/detalhes/'+projeto.nome)
    else:
        flash(u'Projeto não existe!', 'danger')
        return redirect('/inicio')

@foto.route('/criar_foto/<id_projeto>', methods=['GET', 'POST'])
def criar_foto(id_projeto):
    if check_login(0):
        projeto = Projeto.query.get(id_projeto)
        if projeto:
            usuario = Usuario.query.get(session['user']['id'])
            if pertence_projeto(usuario, projeto):
                form = formFoto()
                if form.validate_on_submit():
                    descricao = request.form['descricao']
                    foto = form.foto.data
                    extencao = foto.filename.split('.')[-1].lower()
                    data_publicacao = date.today()

                    novo_nome_foto = uuid4()
                    is_permitido = permitido(extencao)
                    
                    if is_permitido:
                        novo_nome_foto = str(novo_nome_foto) + '.' + extencao
                        foto_aux = secure_filename(foto.filename)

                        diretorio = os.path.join(app.config['UPLOAD_FOLDER']+'fotos/', foto_aux)

                        diretorio_novo = os.path.join(app.config['UPLOAD_FOLDER']+'fotos/', novo_nome_foto)

                        foto.save(diretorio)
                        os.rename(diretorio, diretorio_novo)

                        foto = Foto(descricao = descricao, data_publicacao = data_publicacao, id_usuario = session['user']['id'], 
                        id_projeto=projeto.id, caminho = novo_nome_foto)

                        projeto.fotos.append(foto)
                        db.session.add(projeto)
                        db.session.commit()
                        flash(u'Foto adicionado com sucesso!', 'success')
                        return redirect('/fotos/' + projeto.nome)
                    else:
                        flash(u'Extensão de foto não permitida!', 'danger')
                        return render_template('foto/criar.html',form=form,projeto=projeto)             
                return render_template('foto/criar.html',form=form,projeto=projeto)
            else:
                flash(u'Você não faz parte deste projeto!', 'danger')
                return redirect('/painel_usuario')
        else:
            flash(u'Projeto não existe!', 'danger')
            return redirect('/painel_usuario')          
    else:
        return redirect('/entrar')

@foto.route('/editar_foto/<nome_projeto>/<id_foto>', methods = ['GET', 'POST'])
def editar_foto(nome_projeto,id_foto):
    if check_login(0):
        projeto = Projeto.query.filter_by(nome = nome_projeto).first()
        if projeto:
            usuario = Usuario.query.get(session['user']['id'])
            if pertence_projeto(usuario, projeto):
                form = formFoto()
                foto = Foto.query.get(id_foto)
                if foto:
                    if foto.id_projeto == projeto.id:
                        if foto.id_usuario == session['user']['id'] or session['user']['id'] == projeto.id_autor:
                            if request.method == 'POST':
                                if form.validate:
                                    foto = Foto.query.filter_by(id = id_foto).update(dict(descricao=request.form['descricao']))
                                    db.session.commit()
                                    flash(u'Foto editada com sucesso!', 'success')
                                    return redirect('/fotos/'+projeto.nome)
                            return render_template('foto/editar.html',form=form,projeto=projeto,foto=foto)
                        else:
                            flash(u'Você não tem permissão para realizar a ação!', 'danger')
                            return redirect('/entrar')
                    else:
                        flash(u'Foto não está vinculada ao projeto!', 'danger')
                        return redirect('/fotos/'+projeto.nome)
                else:
                    flash(u'Foto não existe!', 'danger')
                    redirect('/painel_usuario')
            else:
                flash(u'Você não faz parte deste projeto!', 'danger')
                return redirect('/painel_usuario')
        else:
            flash(u'Projeto não existe!', 'danger')
            return redirect('/painel_usuario')
    else:
        return redirect('/entrar')


@foto.route('/deletar_foto/<nome_projeto>/<id_foto>', methods = ['GET', 'POST'])
def excluir_foto(nome_projeto,id_foto):
    if check_login(0):
        projeto = Projeto.query.filter_by(nome = nome_projeto).first()
        if projeto:
            usuario = Usuario.query.get(session['user']['id'])
            if pertence_projeto(usuario, projeto):
                foto = Foto.query.get(id_foto)
                if foto:
                    if foto.id_projeto == projeto.id:
                        if foto.id_usuario == session['user']['id'] or session['user']['id'] == projeto.id_autor:
                            os.remove(app.config['UPLOAD_FOLDER']+'fotos/'+foto.caminho)
                            db.session.delete(foto)
                            db.session.commit()
                            flash(u'Foto deletada com sucesso!', 'success')
                            return redirect('/fotos/'+projeto.nome)
                        else:
                            flash(u'Você não tem permissão para realizar a ação!', 'danger')
                            return redirect('/entrar')
                    else:
                        flash(u'Foto não está vinculada ao projeto!', 'danger')
                        return redirect('/fotos/'+projeto.nome)
                else:
                    flash(u'Foto não existe!', 'danger')
                    redirect('/painel_usuario')
            else:
                flash(u'Você não faz parte deste projeto!', 'danger')
                return redirect('/painel_usuario')
        else:
            flash(u'Projeto não existe!', 'danger')
            return redirect('/painel_usuario')
    else:
        return redirect('/entrar') 

