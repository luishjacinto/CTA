# -*- coding: utf-8 -*-
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
from flask import render_template,Blueprint,redirect,request,session,flash,url_for
from app.models.Noticia import Noticia
from app.models.Usuario import Usuario
from app.models.Projeto import Projeto
from app.models.forms.formNoticia import formNoticia
from app.controllers.verify import check_login, pertence_projeto
from datetime import datetime, date
import hashlib
from app import db

noticia = Blueprint('noticia', __name__)

@noticia.route("/noticias/<nome>", methods = ['GET', 'POST'])
def noticias(nome):
    projeto = Projeto.query.filter_by(nome = nome).first()
    if projeto:
        if projeto.noticias:
            if check_login(0):
                usuario = Usuario.query.get(session['user']['id'])
                if pertence_projeto(usuario, projeto):
                    pass
            else:
                pass
            return render_template('noticia/noticias.html',projeto=projeto)
        else:
            flash(u'Projeto não possui notícias!', 'danger')
            return redirect('/detalhes/'+projeto.nome)
    else:
        flash(u'Projeto não existe!', 'danger')
        return redirect('/inicio')

@noticia.route('/criar_noticia/<id_projeto>', methods = ['GET', 'POST'])
def criar_noticia(id_projeto):
    if check_login(0):
        projeto = Projeto.query.get(id_projeto)
        if projeto:
            usuario = Usuario.query.get(session['user']['id'])
            if pertence_projeto(usuario, projeto):
                form = formNoticia()
                if form.validate_on_submit():
                    nome = request.form['nome']
                    conteudo = request.form['conteudo']
                    data_publicacao = date.today()

                    noticia = Noticia(nome = nome, conteudo = conteudo, data_publicacao = data_publicacao, id_usuario = session['user']['id'], id_projeto=projeto.id)
                    projeto.noticias.append(noticia)
                    db.session.add(projeto)
                    db.session.commit()
                    flash(u'Notícia adicionada com sucesso!', 'success')
                    return redirect('/noticias/' + projeto.nome)
                return render_template('noticia/criar.html',form=form,projeto=projeto)
            else:
                flash(u'Você não faz parte deste projeto!', 'danger')
                return redirect('/painel_usuario')
        else:
            flash(u'Projeto não existe!', 'danger')
            return redirect('/painel_usuario')        
    else:
        return redirect('/entrar')

@noticia.route('/editar_noticia/<nome_projeto>/<id_noticia>', methods = ['GET', 'POST'])
def editar_noticia(nome_projeto,id_noticia):
    if check_login(0):
        projeto = Projeto.query.filter_by(nome = nome_projeto).first()
        if projeto:
            usuario = Usuario.query.get(session['user']['id'])
            if pertence_projeto(usuario, projeto):
                form = formNoticia()
                noticia = Noticia.query.get(id_noticia)
                if noticia:
                    if noticia.id_projeto == projeto.id:
                        if noticia.id_usuario == session['user']['id'] or session['user']['id'] == projeto.id_autor:
                            if form.validate_on_submit():
                                noticia = Noticia.query.filter_by(id = id_noticia).update(dict(nome=request.form['nome'],conteudo = request.form['conteudo']))
                                db.session.commit()
                                flash(u'Notícia editada com sucesso!', 'success')
                                return redirect('/noticias/'+projeto.nome)
                            return render_template('noticia/editar.html',form=form,projeto=projeto,noticia=noticia)
                        else:
                            flash(u'Você não tem permissão para realizar a ação!', 'danger')
                            return redirect('/entrar')
                    else:
                        flash(u'Notícia não está vinculada ao projeto!', 'danger')
                        return redirect('/noticias/'+projeto.nome)
                else:
                    flash(u'Noticia não existe!', 'danger')
                    redirect('/painel_usuario')
            else:
                flash(u'Você não faz parte deste projeto!', 'danger')
                return redirect('/painel_usuario')
        else:
            flash(u'Projeto não existe!', 'danger')
            return redirect('/painel_usuario')
    else:
        return redirect('/entrar')


@noticia.route('/deletar_noticia/<nome_projeto>/<id_noticia>', methods = ['GET', 'POST'])
def deletar_noticia(nome_projeto,id_noticia):
    if check_login(0):
        projeto = Projeto.query.filter_by(nome = nome_projeto).first()
        if projeto:
            usuario = Usuario.query.get(session['user']['id'])
            if pertence_projeto(usuario, projeto):
                noticia = Noticia.query.get(id_noticia)
                if noticia:
                    if noticia.id_projeto == projeto.id:
                        if noticia.id_usuario == session['user']['id'] or session['user']['id'] == projeto.id_autor:
                            projeto.noticias.remove(noticia)
                            db.session.add(projeto)
                            db.session.commit()
                            flash(u'Notícia deletada com sucesso!', 'success')
                            return redirect('/noticias/'+projeto.nome)
                        else:
                            flash(u'Você não tem permissão para realizar a ação!', 'danger')
                            return redirect('/entrar')
                    else:
                        flash(u'Notícia não está vinculada ao projeto!', 'danger')
                        return redirect('/noticias/'+projeto.nome)
                else:
                    flash(u'Notícia não existe!', 'danger')
                    redirect('/painel_usuario')
            else:
                flash(u'Você não faz parte deste projeto!', 'danger')
                return redirect('/painel_usuario')
        else:
            flash(u'Projeto não existe!', 'danger')
            return redirect('/painel_usuario')
    else:
        return redirect('/entrar') 

@noticia.route("/noticia/<nome_projeto>/<nome_noticia>", methods = ['GET', 'POST'])
def detalhes_noticia(nome_projeto,nome_noticia):
    projeto = Projeto.query.filter_by(nome = nome_projeto).first()
    if projeto:    
        noticia = Noticia.query.filter_by(nome = nome_noticia).first()
        if noticia:   
            if noticia.id_projeto == projeto.id:
                if check_login(0):
                    usuario = Usuario.query.get(session['user']['id'])
                    if pertence_projeto(usuario, projeto):
                        pass
                    else:
                        pass
                return render_template('noticia/noticia.html',projeto=projeto,noticia=noticia)
            else:
                flash(u'Notícia não está vinculada ao projeto!', 'danger')
                return redirect('/noticias/'+projeto.nome)
        else:
            flash(u'Notícia não existe!', 'danger')
            return redirect('/painel_usuario')
    else:
        return redirect('/inicio')