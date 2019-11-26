from .Base import Base
from sqlalchemy import Boolean,Date,DateTime,Time,ForeignKey,Column, Integer, Numeric, Binary, String,VARCHAR,Float
from sqlalchemy.orm import relationship

class Noticia(Base):
    __tablename__= 'noticia'
    nome = Column(VARCHAR(200),unique=True, nullable = False)
    conteudo = Column(VARCHAR(10000), nullable = False)
    data_publicacao = Column(Date(),nullable = False)
    id_projeto = Column(ForeignKey('projeto.id'),nullable = False)
    id_usuario = Column(ForeignKey('usuario.id'),nullable = False)
    autor = relationship("Usuario", backref="noticia", lazy="joined")


