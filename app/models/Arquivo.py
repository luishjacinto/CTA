from app.models.Base import Base
from sqlalchemy import Boolean,Date,DateTime,Time,ForeignKey,Column, Integer, Numeric, Binary, String,VARCHAR,Float
from sqlalchemy.orm import relationship

class Arquivo(Base):
    __tablename__= 'arquivo'
    caminho = Column(VARCHAR(500), nullable = False)
    nome = Column(VARCHAR(100), nullable = False)
    data_publicacao = Column(Date(),nullable = False)
    id_projeto = Column(ForeignKey('projeto.id'),nullable = False)
    id_usuario = Column(ForeignKey('usuario.id'),nullable = False)
    autor = relationship("Usuario",backref="arquivo", lazy="joined")

