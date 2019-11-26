from .Base import Base
from sqlalchemy import Table,Boolean,Date,DateTime,Time,ForeignKey,Column, Integer, Numeric, Binary, String,VARCHAR,Float
from sqlalchemy.orm import relationship

Usuarios_projeto = Table('usuarios_projeto', Base.metadata,
    Column('id_projeto', Integer, ForeignKey('projeto.id'), primary_key=True),
    Column('id_usuario', Integer, ForeignKey('usuario.id'), primary_key=True),
)

class Projeto(Base):
    __tablename__= 'projeto'
    nome = Column(VARCHAR(200),unique = True, nullable = False)
    descricao = Column(VARCHAR(3000), nullable = False)
    status = Column(Integer(), nullable = False)
    id_autor = Column(ForeignKey('usuario.id'),nullable = False)
    arquivos = relationship("Arquivo",cascade = "all, delete, delete-orphan", backref="projeto", lazy="joined")
    fotos = relationship("Foto",cascade = "all, delete, delete-orphan", backref="projeto", lazy="joined")
    noticias = relationship("Noticia",cascade = "all, delete, delete-orphan", backref="projeto", lazy="joined")
    repositorios = relationship("Repositorio",cascade = "all, delete, delete-orphan", backref="projeto", lazy="joined")
    tarefas = relationship("Tarefa",cascade = "all, delete, delete-orphan", backref="projeto", lazy="joined")
    autor = relationship("Usuario", backref="projeto", lazy="joined")
    pertence = False

    usuarios = relationship('Usuario',cascade="save-update, merge, delete", backref="projeto_usuarios", lazy='joined', secondary=Usuarios_projeto)