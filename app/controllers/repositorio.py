# -*- coding: utf-8 -*-
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
from flask import render_template,Blueprint,redirect,request,session,flash,url_for
from app.models.Repositorio import Repositorio
from app.models.Usuario import Usuario
from app.models.Projeto import Projeto
from app.models.forms.formRepositorio import formRepo
from app.controllers.verify import check_login, pertence_projeto
from datetime import datetime
import hashlib
from datetime import date
from app import db

repositorio = Blueprint('repositorio', __name__)

@repositorio.route("/repositorios/<nome>", methods = ['GET', 'POST'])
def repositorios(nome):
    projeto = Projeto.query.filter_by(nome = nome).first()
    if projeto:
        if projeto.repositorios:
            if check_login(0):
                usuario = Usuario.query.get(session['user']['id'])
                if pertence_projeto(usuario, projeto):
                    pass
            else:
                pass
            return render_template('repositorio/repositorios.html',projeto=projeto)
        else:
            flash(u'Projeto não possui repositórios!', 'danger')
            return redirect('/detalhes/'+projeto.nome)
    else:
        flash(u'Projeto não existe!', 'danger')
        return redirect('/inicio')

@repositorio.route('/criar_repositorio/<id_projeto>', methods = ['GET', 'POST'])
def criar_repositorio(id_projeto):
    if check_login(0):
        projeto = Projeto.query.get(id_projeto)
        if projeto:
            usuario = Usuario.query.get(session['user']['id'])
            if pertence_projeto(usuario, projeto):
                form = formRepo()
                if form.validate_on_submit():
                    nome = request.form['nome']
                    link = request.form['link']
                    data_publicacao = date.today()
                    data_alteracao = date.today()

                    repositorio = Repositorio(nome = nome, link = link, data_publicacao = data_publicacao,data_alteracao = data_alteracao, id_usuario = session['user']['id'], id_projeto=projeto.id)
                    projeto.repositorios.append(repositorio)
                    db.session.add(projeto)
                    db.session.commit()
                    flash(u'Repositório adicionado com sucesso!', 'success')
                    return redirect('/repositorios/' + projeto.nome)
                    
                return render_template('repositorio/criar.html',form=form,projeto=projeto)
            else:
                flash(u'Você não faz parte deste projeto!', 'danger')
                return redirect('/painel_usuario')
        else:
            flash(u'Projeto não existe!', 'danger')
            return redirect('/painel_usuario')        
    else:
        return redirect('/entrar')


@repositorio.route('/editar_repositorio/<nome_projeto>/<id_repositorio>', methods = ['GET', 'POST'])
def editar_repositorio(nome_projeto,id_repositorio):
    if check_login(0):
        projeto = Projeto.query.filter_by(nome = nome_projeto).first()
        if projeto:
            usuario = Usuario.query.get(session['user']['id'])
            if pertence_projeto(usuario, projeto):
                form = formRepo()
                repositorio = Repositorio.query.get(id_repositorio)
                if repositorio:
                    if repositorio.id_projeto == projeto.id:
                        if repositorio.id_usuario == session['user']['id'] or session['user']['id'] == projeto.id_autor:
                            if form.validate_on_submit():
                                repositorio = Repositorio.query.filter_by(id = id_repositorio).update(dict(nome=request.form['nome'],link = request.form['link'],data_alteracao = date.today()))
                                db.session.commit()
                                flash(u'Repositório editado com sucesso!', 'success')
                                return redirect('/repositorios/'+projeto.nome)
                            return render_template('repositorio/editar.html',form=form,projeto=projeto,repositorio=repositorio)
                        else:
                            flash(u'Você não tem permissão para realizar a ação!', 'danger')
                            return redirect('/entrar')
                    else:
                        flash(u'Repositório não está vinculado ao projeto!', 'danger')
                        return redirect('/repositorios/'+projeto.nome)
                else:
                    flash(u'Repositório não existe!', 'danger')
                    redirect('/painel_usuario')
            else:
                flash(u'Você não faz parte deste projeto!', 'danger')
                return redirect('/painel_usuario')
        else:
            flash(u'Projeto não existe!', 'danger')
            return redirect('/painel_usuario')
    else:
        return redirect('/entrar') 



@repositorio.route('/deletar_repositorio/<nome_projeto>/<id_repositorio>', methods = ['GET', 'POST'])
def deletar_repositorio(nome_projeto,id_repositorio):
    if check_login(0):
        projeto = Projeto.query.filter_by(nome = nome_projeto).first()
        if projeto:
            usuario = Usuario.query.get(session['user']['id'])
            if pertence_projeto(usuario, projeto):
                repositorio = Repositorio.query.get(id_repositorio)
                if repositorio:
                    if repositorio.id_projeto == projeto.id:
                        if repositorio.id_usuario == session['user']['id'] or session['user']['id'] == projeto.id_autor:
                            projeto.repositorios.remove(repositorio)
                            db.session.add(projeto)
                            db.session.commit()
                            flash(u'Repositório deletado com sucesso!', 'success')
                            return redirect('/detalhes/'+projeto.nome)
                        else:
                            flash(u'Você não tem permissão para realizar a ação!', 'danger')
                            return redirect('/entrar')
                    else:
                        flash(u'Repositório não está vinculado ao projeto!', 'danger')
                        return redirect('/repositorios/'+projeto.nome)
                else:
                    flash(u'Repositório não existe!', 'danger')
                    redirect('/painel_usuario')
            else:
                flash(u'Você não faz parte deste projeto!', 'danger')
                return redirect('/painel_usuario')
        else:
            flash(u'Projeto não existe!', 'danger')
            return redirect('/painel_usuario')
    else:
        return redirect('/entrar') 