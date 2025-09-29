from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey
from db.session import Base
from sqlalchemy.orm import relationship


class Quiosque(Base):
    __tablename__ = "quiosques"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    nota = Column(Numeric(2, 1))
    tem_acessibilidade = Column(Boolean, default=False)
    tem_banheiro = Column(Boolean, default=False)
    valor = Column(Numeric(1, 0))
    ocupacao_maxima = Column(Numeric(5, 0))
    latitude = Column(Numeric(9, 6), nullable=False)
    longitude = Column(Numeric(9, 6), nullable=False)
    praia_id = Column(Integer, ForeignKey("praias.id"))
    praia = relationship("Praia", back_populates="quiosques")
