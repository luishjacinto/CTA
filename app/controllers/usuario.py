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
from app.models.forms.login import formLogin
from app.models.forms.cadastro import formCadastro
from app.models.forms.busca import formBusca
from datetime import datetime
from app.controllers.verify import check_login
from hashlib import md5
import datetime
from app import db

usuario = Blueprint('usuario', __name__)

@usuario.route("/cadastro", methods = ['GET', 'POST'])
def cadastro():
    if check_login(2):
        form = formCadastro()
        if form.validate_on_submit():
            nome = request.form['nome']
            senha = md5(request.form['senha'].encode())
            email = request.form['email']
            data_nascimento = request.form['data']
            usuario = Usuario(nome = nome, senha = senha.hexdigest(), email = email, 
            data_nascimento = data_nascimento, permissoes = 0)
            db.session.add(usuario)
            db.session.commit()
            flash(u'Cadastro efetuado com sucesso!', 'success')
            return redirect("/inicio")
        return render_template('usuario/cadastro.html',form=form)
    else:
        flash(u'Você não pode efetuar o cadastro enquanto logado!', 'danger')
        return redirect("/inicio")


@usuario.route("/entrar", methods = ['GET', 'POST'])
def entrar():
    if check_login(2):
        form=formLogin()
        if form.validate_on_submit():
            usuario = Usuario.query.filter_by(email = request.form['email']).first()
            senha = md5(request.form['senha'].encode())
            if usuario:
                if usuario.senha == senha.hexdigest():
                    usuario = usuario.as_dict()
                    if usuario["permissoes"] == False:
                        session['user'] = usuario
                        session['logado'] = 'usuario'
                        flash(u'Login efetuado com sucesso!', 'success')
                        return redirect('/painel_usuario')    
                    elif usuario['permissoes'] == True:
                        session['user'] = usuario
                        session['logado'] = 'administrador'
                        flash(u'Login efetuado com sucesso!', 'success')
                        return redirect('/projetos')    
                    else:
                        return redirect('/entrar')
                else:
                    flash(u'Senha incorreta!', 'danger')
                    return redirect('/entrar')
            else:
                flash(u'Email incorreto!', 'danger')
                return redirect('/entrar')
        return render_template('/usuario/entrar.html',form=form)
    else:
        return redirect("/inicio")

@usuario.route("/sair")
def sair():
    session.clear()
    return redirect('/inicio')

@usuario.route('/painel_usuario', methods = ['GET', 'POST'])
def painel_usuario():
    if check_login(0):
        usuario = Usuario.query.get(session['user']['id'])
        if usuario:
            return render_template('usuario/painel.html',usuario=usuario)
        else:
            flash(u'Ocorreu um erro!', 'danger')
            return redirect('/sair')
    else:
        return redirect('/entrar')

@usuario.route('/perfil/<nome>/<id>', methods = ['GET', 'POST'])
def perfil(nome,id):    
    usuario = Usuario.query.get(id)
    if usuario:
        if check_login(0):
            if usuario.id == session['user']['id']:
                return render_template('/usuario/perfil.html', usuario=usuario)
            else:
                if usuario.privado == False:
                    if usuario.permissoes == 0:
                        return render_template('/usuario/perfil.html', usuario=usuario)
                    else:
                        flash(u'Usuario não foi encontrado!', 'danger')
                        return redirect('/inicio')
                else:
                    flash(u'Usuario possui perfil privado', 'danger')
                    return redirect('/inicio')
        elif check_login(1):
            return render_template('/usuario/perfil.html', usuario=usuario)
        else:
            if usuario.privado == False:
                if usuario.permissoes == 0:
                    return render_template('/usuario/perfil.html', usuario=usuario)
                else:
                    flash(u'Usuario não foi encontrado!', 'danger')
                    return redirect('/inicio')
            else:
                flash(u'Usuario possui perfil privado', 'danger')
                return redirect('/inicio')
    else:
        flash(u'Usuario não foi encontrado!', 'danger')
        return redirect('/inicio')

@usuario.route('/alterar_privacidade/<id>', methods = ['GET', 'POST'])
def alterar_privacidade(id):
    if check_login(0):           
        usuario = Usuario.query.get(id)        
        if usuario:
            if usuario.id == session['user']['id']:
                if usuario.privado == True:
                    usuario.privado = False
                    db.session.add(usuario)
                    db.session.commit()
                    flash(u'Seu perfil agora é público!', 'success')
                    return redirect('/perfil/'+usuario.nome+'/'+str(usuario.id))
                else:
                    usuario.privado = True
                    db.session.add(usuario)
                    db.session.commit()
                    flash(u'Seu perfil agora é privado!', 'success')
                    return redirect('/perfil/'+usuario.nome+'/'+str(usuario.id))
            else:
                flash(u'Ocorreu um erro!', 'danger')
                return redirect('/painel_usuario')
        else:
            flash(u'Ocorreu um erro!', 'danger')
            return redirect('/painel_usuario')
    else:
        return redirect('/entrar')

@usuario.route("/usuarios", methods = ['GET', 'POST'])
def usuarios():
    if check_login(1):
        form = formBusca()
        if form.validate_on_submit():
            busca = request.form['busca']
            usuarios = Usuario.query.filter(Usuario.nome.ilike('%'+busca+'%')).filter_by(permissoes = False).order_by(Usuario.nome).all()
            if usuarios:
                pass
            else:
                flash(u'Busca não encontrou resultado!', 'danger')
                return redirect('/usuarios')
            return render_template('usuario/usuarios.html',usuarios=usuarios,form=form,busca=busca)
        usuarios = Usuario.query.filter_by(permissoes = False).order_by(Usuario.nome).all()
        return render_template('usuario/usuarios.html',usuarios=usuarios,form=form,busca="Todos")
    else:
        return redirect('/entrar')

@usuario.route('/deletar_usuario/<id>', methods = ['GET', 'POST'])
def deletar_usuario(id):
    if check_login(1):
        usuario = Usuario.query.get(id)
        if usuario:
            if usuario.permissoes == False:
                for projeto in usuario.projetos:
                    if projeto.id_autor == usuario.id:
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
                    else:
                        projeto.usuarios.remove(usuario)
                for tarefa in usuario.tarefas:
                    if tarefa.id_autor == usuario.id:
                        for membro in tarefa.usuarios:
                            tarefa.usuarios.remove(membro)
                            db.session.add(tarefa) 
                            db.session.commit()
                        tarefa.usuarios.clear()
                        db.session.delete(tarefa)
                        db.session.commit()
                    else:
                        tarefa.usuarios.remove(usuario)
                        db.session.add(tarefa) 
                        db.session.commit()
                db.session.delete(usuario)
                db.session.commit()
                flash(u'Usuário deletado com sucesso!', 'success')
                return redirect('/painel_usuario')
            else:
                flash(u'Usuário não pode ser deletado!', 'danger')
                return redirect('/painel_usuario')
        else:
            flash(u'Usuário não existe!', 'danger')
            return redirect('/painel_usuario')
    else:
        return redirect('/entrar')