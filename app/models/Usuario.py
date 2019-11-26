from .Base import Base
from sqlalchemy import Boolean,Date,DateTime,Time,ForeignKey,Column, Integer, Numeric, Binary, String, VARCHAR,Float, Sequence
from sqlalchemy.orm import relationship
from .Projeto import Projeto, Usuarios_projeto
from .Tarefa import Tarefa, Usuarios_tarefa


class Usuario(Base):
    __tablename__= 'usuario'
    nome = Column(VARCHAR(60), nullable = False)
    senha = Column(VARCHAR(32), nullable = False)
    email = Column(VARCHAR(100),unique = True, nullable = False)
    data_nascimento = Column(Date(),nullable = False)
    permissoes = Column(Boolean(), nullable = False)
    privado = Column(Boolean(), nullable = False, default=True)

    projetos = relationship('Projeto', cascade="save-update, merge, delete", secondary=Usuarios_projeto, backref ='usuarios_projeto', lazy='dynamic')
    tarefas = relationship('Tarefa', secondary=Usuarios_tarefa, backref ='usuarios_tarefa', lazy='dynamic')
