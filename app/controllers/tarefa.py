# -*- coding: utf-8 -*-
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
from flask import render_template,Blueprint,redirect,request,session,flash,url_for
from app.models.Tarefa import Tarefa
from app.models.Usuario import Usuario
from app.models.Projeto import Projeto
from app.models.forms.formTarefa import formTarefa
from app.controllers.verify import check_login, pertence_projeto, pertence_tarefa_projeto, pertence_tarefa
from datetime import datetime
import hashlib
from datetime import date
from app import db

tarefa = Blueprint('tarefa', __name__)

@tarefa.route("/tarefas/<nome>", methods = ['GET', 'POST'])
def tarefas(nome):
    projeto = Projeto.query.filter_by(nome = nome).first()
    if projeto:
        if projeto.tarefas:
            if check_login(0):
                usuario = Usuario.query.get(session['user']['id'])
                if pertence_projeto(usuario, projeto):
                    pass
                if pertence_tarefa_projeto(usuario, projeto):
                    pass
            else:
                pass
            return render_template('tarefa/tarefas.html',projeto=projeto)
        else:
            flash(u'Projeto não possui tarefas!', 'danger')
            return redirect('/detalhes/'+projeto.nome)
    else:
        flash(u'Projeto não existe!', 'danger')
        return redirect('/inicio')

@tarefa.route('/criar_tarefa/<id_projeto>', methods = ['GET', 'POST'])
def criar_tarefa(id_projeto):
    if check_login(0):
        projeto = Projeto.query.get(id_projeto)
        if projeto:
            usuario = Usuario.query.get(session['user']['id'])
            if pertence_projeto(usuario, projeto):
                form = formTarefa()
                if form.validate_on_submit():
                    nome = request.form['nome']
                    prioridade = request.form['prioridade']
                    status = request.form['status']
                    tipo = request.form['tipo']
                    data_alteracao = date.today()
                    autor = Usuario.query.get(session['user']['id'])

                    tarefa = Tarefa(nome = nome, prioridade = prioridade, status = status, tipo = tipo, data_alteracao = data_alteracao, id_autor = autor.id, id_projeto=projeto.id)
                    tarefa.usuarios.append(autor)
                    projeto.tarefas.append(tarefa)
                    db.session.add(projeto)
                    db.session.commit()
                    flash(u'Tarefa adicionada com sucesso!', 'success')
                    return redirect('/tarefas/' + projeto.nome)
                    
                return render_template('tarefa/criar.html',form=form,projeto=projeto)
            else:
                flash(u'Você não faz parte deste projeto!', 'danger')
                return redirect('/painel_usuario')
        else:
            flash(u'Projeto não existe!', 'danger')
            return redirect('/painel_usuario')          
    else:
        return redirect('/entrar')

@tarefa.route('/editar_tarefa/<nome_projeto>/<id_tarefa>', methods = ['GET', 'POST'])
def editar_tarefa(nome_projeto,id_tarefa):
    if check_login(0):
        projeto = Projeto.query.filter_by(nome = nome_projeto).first()
        if projeto:
            usuario = Usuario.query.get(session['user']['id'])
            if pertence_projeto(usuario, projeto):
                form = formTarefa()
                tarefa = Tarefa.query.get(id_tarefa)
                if tarefa:
                    if tarefa.id_projeto == projeto.id:
                        if pertence_tarefa(usuario, tarefa) or session['user']['id'] == projeto.id_autor:
                            if form.validate_on_submit():
                                tarefa = Tarefa.query.filter_by(id = id_tarefa).update(dict(nome=request.form['nome'],
                                prioridade = request.form['prioridade'],
                                status=request.form['status'],
                                tipo=request.form['tipo'],
                                data_alteracao=date.today()))
                                db.session.commit()
                                flash(u'Tarefa editada com sucesso!', 'success')
                                return redirect('/tarefas/'+projeto.nome)
                            return render_template('tarefa/editar.html',form=form,projeto=projeto,tarefa=tarefa)
                        else:
                            flash(u'Você não tem permissão para realizar a ação!', 'danger')
                            return redirect('/entrar')
                    else:
                        flash(u'Tarefa não existe ou não está vinculada ao projeto!', 'danger')
                        return redirect('/tarefas/'+projeto.nome)
                else:
                    flash(u'Tarefa não existe!', 'danger')
                    return redirect('/detalhes/'+projeto.nome)
            else:
                flash(u'Você não faz parte deste projeto!', 'danger')
                return redirect('/painel_usuario')
        else:
            flash(u'Projeto não existe!', 'danger')
            return redirect('/painel_usuario')
    else:
        return redirect('/entrar')

@tarefa.route('/deletar_tarefa/<nome_projeto>/<id_tarefa>', methods = ['GET', 'POST'])
def deletar_tarefa(nome_projeto,id_tarefa):
    if check_login(0):
        projeto = Projeto.query.filter_by(nome = nome_projeto).first()
        if projeto:
            usuario = Usuario.query.get(session['user']['id'])
            if pertence_projeto(usuario, projeto):  
                tarefa = Tarefa.query.get(id_tarefa)
                if tarefa:
                    if tarefa.id_projeto == projeto.id:
                        if tarefa.id_autor == session['user']['id'] or session['user']['id'] == projeto.id_autor:
                            for membro in tarefa.usuarios:
                                tarefa.usuarios.remove(membro)
                                db.session.add(tarefa) 
                                db.session.commit()
                            tarefa.usuarios.clear()
                            projeto.tarefas.remove(tarefa)
                            db.session.add(projeto)
                            db.session.commit()
                            flash(u'Tarefa deletada com sucesso!', 'success')
                            return redirect('/detalhes/'+projeto.nome)
                        else:
                            flash(u'Você não tem permissão para realizar a ação!', 'danger')
                            return redirect('/entrar')
                    else:
                        flash(u'Tarefa não está vinculada ao projeto!', 'danger')
                        return redirect('/tarefas/'+projeto.nome)
                else:
                    flash(u'Tarefa não existe!', 'danger')
                    return redirect('/detalhes/'+projeto.nome)
            else:
                flash(u'Você não faz parte deste projeto!', 'danger')
                return redirect('/painel_usuario')
        else:
            flash(u'Projeto não existe!', 'danger')
            return redirect('/painel_usuario')
    else:
        return redirect('/entrar') 


@tarefa.route('/adicionar_membro_tarefa/<nome_projeto>/<id_tarefa>/<id_usuario>', methods = ['GET', 'POST'])
def adicionar_membro_tarefa(nome_projeto,id_tarefa,id_usuario):
    if check_login(0):
        projeto = Projeto.query.filter_by(nome = nome_projeto).first()
        if projeto:
            usuario = Usuario.query.get(session['user']['id'])
            if pertence_projeto(usuario, projeto):
                tarefa = Tarefa.query.get(id_tarefa)
                if tarefa:
                    if tarefa.id_projeto == projeto.id:
                        if tarefa.id_autor == session['user']['id'] or session['user']['id'] == projeto.id_autor:
                            membro = Usuario.query.get(id_usuario)
                            if membro:
                                if membro in projeto.usuarios:
                                    if membro not in tarefa.usuarios:
                                        tarefa.usuarios.append(membro)
                                        db.session.add(tarefa) 
                                        db.session.commit()
                                        flash(u'Membro adicionado a tarefa!', 'success')
                                        return redirect('/editar_tarefa/'+projeto.nome+'/'+str(tarefa.id))
                                    else:
                                        flash(u'Usuário ja está atribuido a tarefa!', 'danger')
                                        return redirect('/tarefas/'+projeto.nome)
                                else:
                                    flash(u'Usuário não pertence ao projeto!', 'danger')
                                    return redirect('/tarefas/'+projeto.nome)
                            else:
                                flash(u'Usuário não existe!', 'danger')
                                return redirect('/tarefas/'+projeto.nome)
                        else:
                            flash(u'Você não possui permissão para realizar a ação!', 'danger')
                            return redirect('/tarefas/'+projeto.nome)
                    else:
                        flash(u'Tarefa não esta vinculada ao projeto', 'danger')
                        return redirect('/tarefas/'+projeto.nome)
                else:
                    flash(u'Tarefa não existe!', 'danger')
                    return redirect('/detalhes/'+projeto.nome)
            else:
                flash(u'Você não possui permissão para realizar a ação!', 'danger')
                return redirect('/tarefas/'+projeto.nome)
        else:
            flash(u'Projeto não existe!', 'danger')
            return redirect('/painel_usuario')
    else:
        return redirect('/entrar')

@tarefa.route('/remover_membro_tarefa/<nome_projeto>/<id_tarefa>/<id_usuario>', methods = ['GET', 'POST'])
def remover_membro_tarefa(nome_projeto,id_tarefa,id_usuario):
    if check_login(0):
        projeto = Projeto.query.filter_by(nome = nome_projeto).first()
        if projeto:
            usuario = Usuario.query.get(session['user']['id'])
            if pertence_projeto(usuario, projeto):
                tarefa = Tarefa.query.get(id_tarefa)
                if tarefa:
                    if tarefa.id_projeto == projeto.id:
                        if tarefa.id_autor == session['user']['id'] or session['user']['id'] == projeto.id_autor:
                            membro = Usuario.query.get(id_usuario)
                            if membro:
                                if membro in tarefa.usuarios:
                                    tarefa.usuarios.remove(membro)
                                    db.session.add(tarefa) 
                                    db.session.commit()
                                    flash(u'Membro removido com sucesso!', 'success')
                                    return redirect('/editar_tarefa/'+projeto.nome+'/'+str(tarefa.id))
                                else:
                                    flash(u'Usuário não está atribuido a tarefa!', 'danger')
                                    return redirect('/tarefas/'+projeto.nome)
                            else:
                                flash(u'Usuário não existe!', 'danger')
                                return redirect('/detalhes/'+projeto.nome)
                        else:
                            flash(u'Você não possui permissão para realizar a ação!', 'danger')
                            return redirect('/tarefas/'+projeto.nome)
                    else:
                        flash(u'Tarefa não esta vinculada ao projeto', 'danger')
                        return redirect('/tarefas/'+projeto.nome)
                else:
                    flash(u'Tarefa não existe!', 'danger')
                    return redirect('/detalhes/'+projeto.nome)
            else:
                flash(u'Você não possui permissão para realizar a ação!', 'danger')
                return redirect('/tarefas/'+projeto.nome)
        else:
            flash(u'Projeto não existe!', 'danger')
            return redirect('/painel_usuario')
    else:
        return redirect('/entrar')