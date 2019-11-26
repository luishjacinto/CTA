from .Base import Base
from sqlalchemy import Boolean,Date,DateTime,Time,ForeignKey,Column, Integer, Numeric, Binary, String,VARCHAR,Float
from sqlalchemy.orm import relationship

class Foto(Base):
    __tablename__= 'foto'
    caminho = Column(VARCHAR(500), nullable = False)
    descricao = Column(VARCHAR(1000), nullable = False)
    data_publicacao = Column(Date(),nullable = False)
    id_projeto = Column(ForeignKey('projeto.id'),nullable = False)
    id_usuario = Column(ForeignKey('usuario.id'),nullable = False)
    autor = relationship("Usuario", backref="foto", lazy="joined")


