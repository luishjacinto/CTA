# -*- coding: utf-8 -*-
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
from flask import render_template,Blueprint,redirect,request,session,flash,url_for
from app.models.Arquivo import Arquivo
from app.models.Foto import Foto
from app.models.Noticia import Noticia
from app.models.Repositorio import Repositorio
from app.models.Tarefa import Tarefa
from app.models.Usuario import Usuario
from app.models.Projeto import Projeto
from app.models.forms.formProjeto import formProjeto
from app.models.forms.formMembro import formMembro
from app.models.forms.busca import formBusca
from app.controllers.verify import check_login, pertence_projeto, pertence_tarefa_projeto
from datetime import datetime
import hashlib
import datetime
import os
from app import app, db

projeto = Blueprint('projeto', __name__)


@projeto.route('/criar_projeto', methods = ['GET', 'POST'])
def criar_projeto():
    if check_login(0):
        form = formProjeto()
        if form.validate_on_submit():
            nome = request.form['nome']
            descricao = request.form['descricao']
            status = request.form['status']
            autor = Usuario.query.get(session['user']['id'])
            if autor:
                projeto = Projeto(nome = nome, descricao = descricao, status = status, id_autor = autor.id)
                projeto.usuarios.append(autor)
                db.session.add(projeto) 
                db.session.commit()
                flash(u'Projeto criado com sucesso!', 'success')
                return redirect('/painel_usuario')
            else:
                flash(u'Ocorreu um erro ao adicionar o projeto!', 'danger')
                return redirect('/entrar')
        return render_template('projeto/criar.html',form=form)
    else:
        return redirect('/entrar')

@projeto.route('/deletar_projeto/<id>', methods = ['GET', 'POST'])
def deletar_projeto(id):
    if check_login(0) or check_login(1):
        projeto = Projeto.query.get(id)
        if projeto:
            if projeto.id_autor == session['user']['id'] or check_login(1):
                for arquivo in projeto.arquivos:
                    os.remove(app.config['UPLOAD_FOLDER']+'arquivos/'+arquivo.caminho)
                projeto.arquivos.clear()

                for foto in projeto.fotos:
                    os.remove(app.config['UPLOAD_FOLDER']+'fotos/'+foto.caminho)
                projeto.fotos.clear()

                for tarefa in projeto.tarefas:
                    tarefa.usuarios.clear()
                    db.session.add(tarefa)
                    db.session.commit()
                projeto.tarefas.clear()

                projeto.usuarios.clear()
                projeto.noticias.clear()
                projeto.repositorios.clear()
                    
                db.session.commit()
                db.session.delete(projeto)
                db.session.commit()
                flash(u'Projeto deletado com sucesso!', 'success')
                return redirect('/painel_usuario')
            else:
                flash(u'Você não possui permissão para realizar a ação!', 'danger')
                return redirect('/painel_usuario')
        else:
            flash(u'Projeto não existe!', 'danger')
            return redirect('/painel_usuario')
    else:
        return redirect('/entrar')

@projeto.route('/editar_projeto/<nome>', methods = ['GET', 'POST'])
def editar_projeto(nome):
    if check_login(0):
        form = formProjeto()
        projeto = Projeto.query.filter_by(nome = nome).first()
        if projeto:
            if projeto.id_autor == session['user']['id']:
                if form.validate_on_submit():
                    projeto = Projeto.query.filter_by(nome = nome).update(dict(nome=request.form['nome'],descricao = request.form['descricao'], status=request.form['status']))
                    db.session.commit()
                    flash(u'Projeto editado com sucesso!', 'success')
                    return redirect('/painel_usuario')
                return render_template('projeto/editar.html',form=form,projeto=projeto)
            else:
                flash(u'Você não possui permissão para realizar a ação!', 'danger')
                return redirect('/painel_usuario')
        else:
            flash(u'Projeto não existe!', 'danger')
            return redirect('/painel_usuario')
    else:
        return redirect('/entrar')

@projeto.route("/projetos", methods = ['GET', 'POST'])
def projetos():        
    form = formBusca()
    if form.validate_on_submit():
        busca = request.form['busca']
        projetos = Projeto.query.filter(Projeto.nome.ilike('%'+busca+'%')).order_by(Projeto.nome).all()
        if projetos and busca != '':
            pass
        else:
            flash(u'Busca não encontrou resultado!', 'danger')
            return redirect('/projetos')
        return render_template('projeto/projetos.html',projetos=projetos,form=form,busca=busca)
    projetos = Projeto.query.order_by(Projeto.nome).all()
    return render_template('projeto/projetos.html',projetos=projetos,form=form,busca="Todos")

@projeto.route('/adicionar_membro/<nome>', methods = ['GET', 'POST'])
def adicionar_membro(nome):
    if check_login(0):
        projeto = Projeto.query.filter_by(nome = nome).first()
        if projeto:
            usuario = Usuario.query.get(session['user']['id'])
            if usuario in projeto.usuarios:
                projeto.pertence = True
            if projeto.id_autor == session['user']['id']:
                form = formMembro()
                if form.validate_on_submit():
                    email = request.form['email']
                    usuario = Usuario.query.filter_by(email = email).first()
                    if usuario:
                        if usuario not in projeto.usuarios:
                            if usuario.permissoes == False:
                                projeto.usuarios.append(usuario)
                                db.session.add(projeto) 
                                db.session.commit()
                                flash(u'Membro adicionado ao projeto!', 'success')
                                return redirect('/detalhes/'+projeto.nome)
                            else:
                                flash(u'Usuário não pode ser adicionado como membro!', 'danger')
                                return redirect('/adicionar_membro/'+projeto.nome)
                        else:
                            flash(u'Usuário já existe no projeto!', 'danger')
                            return redirect('/adicionar_membro/'+projeto.nome)
                    else:
                        flash(u'Não foi encontrado um usuário com o email fornecido!', 'danger')
                        return redirect('/adicionar_membro/'+projeto.nome)
                return render_template('projeto/adicionar-membro.html',form=form,projeto=projeto)
            else:
                flash(u'Você não possui permissão para realizar a ação!', 'danger')
                return redirect('/painel_usuario')
        else:
            flash(u'Projeto não existe!', 'danger')
            return redirect('/painel_usuario')
    else:
        return redirect('/entrar')

@projeto.route('/remover_membro/<nome_projeto>/<id_usuario>', methods = ['GET', 'POST'])
def remover_membro(nome_projeto,id_usuario):
    if check_login(0):
        projeto = Projeto.query.filter_by(nome = nome_projeto).first()
        if projeto:
            if projeto.id_autor == session['user']['id']:
                usuario = Usuario.query.get(id_usuario)
                if usuario in projeto.usuarios and usuario.id != projeto.id_autor:
                    for tarefa in projeto.tarefas:
                        if usuario in tarefa.usuarios:
                            tarefa.usuarios.remove(usuario)
                            db.session.add(tarefa)
                            db.session.commit()

                    projeto.usuarios.remove(usuario)
                    db.session.add(projeto) 
                    db.session.commit()
                    flash(u'Membro removido com sucesso!', 'success')
                    return redirect('/detalhes/'+projeto.nome)
                else:
                    flash(u'Ocorreu um erro ao remover o membro!', 'danger')
                    return redirect('/painel_usuario')
            else:
                flash(u'Você não possui permissão para realizar a ação!', 'danger')
                return redirect('/painel_usuario')
        else:
            flash(u'Projeto não existe!', 'danger')
            return redirect('/painel_usuario')
    else:
        return redirect('/entrar')

@projeto.route("/detalhes/<nome>", methods = ['GET', 'POST'])
def detalhes(nome):
    projeto = Projeto.query.filter_by(nome = nome).first()
    if projeto: 
        if check_login(0):
            usuario = Usuario.query.get(session['user']['id'])
            if pertence_projeto(usuario, projeto):
                pass
        else:
            pass
        return render_template('projeto/detalhes.html',projeto=projeto)
    else:
        flash(u'Projeto não existe!', 'danger')
        return redirect('/inicio') 
