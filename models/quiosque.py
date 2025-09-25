from sqlalchemy import Column, Integer, String, Numeric, Boolean
from db.session import Base


class Quiosque(Base):
    __tablename__ = "quiosques"

    nome = Column(String, nullable=False)
    descricao = Column(Boolean, default=True)
    praia = Column(Integer)
    nota = Column(Numeric(2, 1))
    tem_acessibilidade = Column(Boolean, default=False)
    tem_banheiro = Column(Boolean, default=False)
    valor = Column(Numeric(1, 0), nullable=False)
    ocupacao_maxima = Column(Numeric(5, 0), nullable=False)
