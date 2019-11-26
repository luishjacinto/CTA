from .Base import Base
from sqlalchemy import Table, Boolean,Date,DateTime,Time,ForeignKey,Column, Integer, Numeric, Binary, String,VARCHAR,Float
from sqlalchemy.orm import relationship

Usuarios_tarefa = Table('usuarios_tarefa', Base.metadata,
    Column('id_tarefa', Integer, ForeignKey('tarefa.id'), primary_key=True),
    Column('id_usuario', Integer, ForeignKey('usuario.id'), primary_key=True),
)

class Tarefa(Base):
    __tablename__= 'tarefa'
    nome = Column(VARCHAR(60), nullable = False)
    prioridade = Column(Integer, nullable = False)
    status = Column(Integer(), nullable = False)
    data_alteracao = Column(Date(),nullable = False)
    tipo = Column(Integer(), nullable = False)
    id_projeto = Column(ForeignKey('projeto.id'),nullable = False)
    id_autor = Column(ForeignKey('usuario.id'),nullable = False)
    autor = relationship("Usuario", backref="tarefa", lazy="joined")
    pertence = False

    usuarios = relationship('Usuario',cascade="save-update, merge, delete", backref='tarefa_usuarios', lazy='joined', secondary=Usuarios_tarefa)