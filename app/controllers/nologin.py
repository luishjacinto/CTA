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
from app.controllers.verify import check_login, pertence_projeto, pertence_tarefa_projeto
from datetime import datetime
from hashlib import md5
import datetime
from app import db

nologin = Blueprint('nologin', __name__)

@nologin.route("/")
def index():
    return redirect('/inicio')

@nologin.route("/inicio")
def inicio():
    return render_template('inicio.html') 

@nologin.route('/create', methods = ['GET', 'POST'])
def create():
    db.create_all()
    return redirect('/criar_adm')

@nologin.route('/drop', methods = ['GET', 'POST'])
def drop():
    db.drop_all()
    return redirect('/create')

@nologin.route('/criar_adm', methods = ['GET', 'POST'])
def criar_adm():
    usuario = Usuario(nome = 'Luis Henrique Jacinto', senha = md5('123'.encode()).hexdigest(), email = 'luishjacinto98@gmail.com', 
    data_nascimento = datetime.datetime(1998, 5, 23), permissoes = 1)
    db.session.add(usuario)
    db.session.commit()
    return redirect('/criar_user')

@nologin.route('/criar_user', methods = ['GET', 'POST'])
def criar_user():
    #usuarios
    usuario = Usuario(nome = 'Jucleison', senha = md5('123'.encode()).hexdigest(), email = 'juca@gmail.com', 
    data_nascimento = datetime.datetime(1996, 7, 3), permissoes = 0)
    usuario1 = Usuario(nome = 'Kleber', senha = md5('123'.encode()).hexdigest(), email = 'a@gmail.com', 
    data_nascimento = datetime.datetime(1998, 5, 23), permissoes = 0)
    usuario2 = Usuario(nome = 'Adair', senha = md5('123'.encode()).hexdigest(), email = 'b@gmail.com', 
    data_nascimento = datetime.datetime(2000, 1, 6), permissoes = 0, privado = False)
    usuario3 = Usuario(nome = 'Cesar', senha = md5('123'.encode()).hexdigest(), email = 'c@gmail.com', 
    data_nascimento = datetime.datetime(1997, 5, 12), permissoes = 0, privado = False)
    usuario4 = Usuario(nome = 'Jussara', senha = md5('123'.encode()).hexdigest(), email = 'd@gmail.com', 
    data_nascimento = datetime.datetime(1997, 12, 1), permissoes = 0, privado = False)
    db.session.add(usuario) #id = 2
    db.session.add(usuario1) #id = 3
    db.session.add(usuario2) #id = 4
    db.session.add(usuario3) #id = 5
    db.session.add(usuario4) #id = 6
    db.session.commit()

    #projetos
###########################
    projeto = Projeto(nome = 'Kart Ecológico', descricao =  'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer dapibus mauris sit amet ornare egestas. Proin at purus pulvinar, iaculis metus in, tincidunt diam. In rutrum augue vel porttitor accumsan. In eget libero eget arcu aliquet rutrum id sit amet odio. Quisque sed risus mollis, viverra mauris eget, posuere nisi. Maecenas ac congue elit. Vestibulum sed augue vel risus consequat luctus. Etiam eu sodales arcu. Maecenas sed sollicitudin augue, vitae ultrices felis. Ut sed dolor sagittis, blandit nibh eget, sagittis leo. Donec sollicitudin pharetra magna quis luctus. Sed dictum nulla est, quis efficitur sapien posuere non. Integer orci leo, aliquam et luctus a, dapibus vel nisl. Pellentesque maximus mauris lacus, nec dictum enim porttitor sed. Etiam et ipsum eu mauris sodales euismod a at diam. Sed in mi porta magna maximus auctor. Mauris non auctor nulla, nec ultricies libero. In odio augue, interdum pharetra molestie quis, facilisis vel lectus. Nullam malesuada magna fringilla erat lobortis, vitae consequat orci dapibus. Curabitur hendrerit condimentum nisl sed eleifend. Praesent iaculis ultrices mattis. Suspendisse potenti. Nulla cursus, ante ac maximus hendrerit, eros massa gravida libero, id lobortis augue orci vel sem. Aenean ornare efficitur urna, id sollicitudin sem. In non dui sit amet neque feugiat facilisis. Maecenas nibh quam, tempus vel dapibus at, sollicitudin non ex. Duis porttitor felis eget vehicula imperdiet. Maecenas vel bibendum leo. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Quisque dui lectus, scelerisque ut nisl quis, faucibus mollis lorem. Praesent id urna lorem. Donec at nulla vel metus pellentesque molestie. Morbi at bibendum est. Suspendisse dolor eros, malesuada id nibh nec, varius varius neque. Nam eu lorem commodo, varius justo non, facilisis magna. Mauris vel elit felis. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi dapibus sodales ante eu fringilla. Etiam vitae sapien a ex ultrices aliquam non sit amet elit. Aenean in pellentesque felis. Cras ut rutrum est. Quisque aliquet congue turpis.',
    status = 0, id_autor = 2)
    projeto.usuarios.append(usuario)
    projeto.usuarios.append(usuario1)
    projeto.usuarios.append(usuario2)

    noticia = Noticia(nome = 'Destaque nacional do projeto', conteudo = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer dapibus mauris sit amet ornare egestas. Proin at purus pulvinar, iaculis metus in, tincidunt diam. In rutrum augue vel porttitor accumsan.'
    , data_publicacao = datetime.datetime(2019, 8, 2), id_usuario = 3, id_projeto=1)
    noticia1 = Noticia(nome = 'Kart utiliza combustivel sustentavel', conteudo = 'Integer dapibus mauris sit amet ornare egestas. Proin at purus pulvinar, iaculis metus in, tincidunt diam. In rutrum augue vel porttitor accumsan.'
    , data_publicacao = datetime.datetime(2019, 8, 2), id_usuario = 2, id_projeto=1)
    noticia2 = Noticia(nome = 'Kart ultrapassa expectativas em testes', conteudo = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer dapibus mauris sit amet ornare egestas. Proin at purus pulvinar, iaculis metus in, tincidunt diam. In rutrum augue vel porttitor accumsan.'
    , data_publicacao = datetime.datetime(2019, 8, 2), id_usuario = 2, id_projeto=1)
    noticia3 = Noticia(nome = 'Veicúlo percorre 400km com 1 litro do combustivel sustentavel', conteudo = 'Proin at purus pulvinar, iaculis metus in, tincidunt diam. In rutrum augue vel porttitor accumsan.'
    , data_publicacao = datetime.datetime(2019, 8, 2), id_usuario = 4, id_projeto=1)
    noticia4 = Noticia(nome = 'Veiculo chega a 180 quilometros por hora', conteudo = 'Proin at purus pulvinar, iaculis metus in, tincidunt diam. In rutrum augue vel porttitor accumsan.'
    , data_publicacao = datetime.datetime(2019, 8, 2), id_usuario = 3, id_projeto=1)
    noticia5 = Noticia(nome = 'Preparação para competição de Eco karts', conteudo = 'In rutrum augue vel porttitor accumsan.'
    , data_publicacao = datetime.datetime(2019, 8, 2), id_usuario = 3, id_projeto=1)

    projeto.noticias.append(noticia)
    projeto.noticias.append(noticia1)
    projeto.noticias.append(noticia2)
    projeto.noticias.append(noticia3)
    projeto.noticias.append(noticia4)
    projeto.noticias.append(noticia5)

    foto = Foto(descricao = 'Visual atual do kart', data_publicacao =  datetime.datetime(2019, 8, 2), id_usuario = 4, 
    id_projeto=1, caminho = 'foto1.jpg')
    projeto.fotos.append(foto)

    foto1 = Foto(descricao = 'Projeto do kart', data_publicacao =  datetime.datetime(2019, 8, 2), id_usuario = 2, 
    id_projeto=1, caminho = 'foto2.jpeg')
    projeto.fotos.append(foto1)
###########################
    projeto1 = Projeto(nome = 'Drone de baixo custo', descricao =  'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer dapibus mauris sit amet ornare egestas. Proin at purus pulvinar, iaculis metus in, tincidunt diam. In rutrum augue vel porttitor accumsan. In eget libero eget arcu aliquet rutrum id sit amet odio. Quisque sed risus mollis, viverra mauris eget, posuere nisi. Maecenas ac congue elit. Vestibulum sed augue vel risus consequat luctus.',
    status = 2, id_autor = 4)
    projeto1.usuarios.append(usuario2)
    projeto1.usuarios.append(usuario3)

    noticia6 = Noticia(nome = 'Drone sendo fabricado com peças de fibra de carbono', conteudo = 'In rutrum augue vel porttitor accumsan. Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
    , data_publicacao = datetime.datetime(2019, 8, 2), id_usuario = 5, id_projeto=2)
    
    tarefa = Tarefa(nome = 'Documentação', prioridade = 2, status = 0, tipo = 0, data_alteracao = datetime.datetime(2019, 8, 2), id_autor = 5, id_projeto=2)
    tarefa.usuarios.append(usuario3)

    tarefa1 = Tarefa(nome = 'Fabricar hélice', prioridade = 0, status = 2, tipo = 2, data_alteracao = datetime.datetime(2019, 8, 2), id_autor = 4, id_projeto=2)
    tarefa1.usuarios.append(usuario2)
    tarefa1.usuarios.append(usuario3)

    repositorio = Repositorio(nome = 'Programação do arduino V4', link = 'www.linkdorepositorio.com', data_publicacao = datetime.datetime(2019, 8, 2),data_alteracao =  datetime.datetime(2019, 8, 5), id_usuario = 4, id_projeto=2)
    projeto1.repositorios.append(repositorio)
    repositorio1 = Repositorio(nome = 'Lib do arduino', link = 'www.linkdorepositorio.com', data_publicacao = datetime.datetime(2019, 8, 2),data_alteracao =  datetime.datetime(2019, 8, 2), id_usuario = 4, id_projeto=2)
    projeto1.repositorios.append(repositorio1)
###########################
    projeto2 = Projeto(nome = 'Defensivo agricola não tóxico', descricao =  'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer dapibus mauris sit amet ornare egestas. Proin at purus pulvinar, iaculis metus in, tincidunt diam. In rutrum augue vel porttitor accumsan. In eget libero eget arcu aliquet rutrum id sit amet odio.',
    status = 1, id_autor = 6)
    projeto2.usuarios.append(usuario4)
    # adicionar ao banco os projetos
###########################
    db.session.add(projeto)
    db.session.add(projeto1)
    db.session.add(projeto2)

    db.session.commit()
    return redirect('/inicio')
