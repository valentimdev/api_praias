from sqlalchemy import Column, Integer, String, Numeric, Boolean
from db.session import Base


class Praia(Base):
    __tablename__ = "praias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    latitude = Column(Numeric(9, 6), nullable=False)
    longitude = Column(Numeric(9, 6), nullable=False)
    estado = Column(String(2), nullable=False)
    municipio = Column(String, nullable=False)
    comprimento = Column(Integer)
    largura = Column(Integer)
    propria_banho = Column(Boolean, default=True)
    tem_quiosque = Column(Boolean, default=False)
    tem_salvavida = Column(Boolean, default=False)
    rating = Column(Numeric(2, 1))
