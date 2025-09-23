import os

from typing import List, Union

from fastapi import FastAPI, HTTPException, Depends

from pydantic import BaseModel

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

#pegando a url do db 
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/mydatabase")
#criando a engine do sqalchemy orm
engine = create_engine(DATABASE_URL)

#criando uma fabrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#criando classe base que os modelos de tabela vao herdar
Base = declarative_base()


#define os campos da praia, esse base model é do pydantic e aplica umas regrinhas, uma delas é que todos esses campos tem que ser preenchidos a menos que a gente ja atribua um valor default neles
class PraiaBase(BaseModel):
    
    nome:str
    latitude:float
    longitude:float
    estado:str
    municipio:str
    comprimento:int
    largura:int
    propria_banho:bool
    quiosque:bool
    salvavida:bool
    rating:float

#esse aqui é o que vai fazer a criação e ele tem pass dentro pois nao adiciona mais nenhum campo, apenas herda do praia base todos os atributos
#é o objeto que a gente recebe do usuario pelo post

class PraiaCreate(PraiaBase):
    pass 

#modelo de resposta, é o que vai ser cuspido, retorna o objeto completo com o ID
class Praia(PraiaBase):
    id: int 
    class Config:
        orm_mode = True

#define como é a tabela praias no db
class PraiaDB(Base):
    __tablename__ = "praias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    estado = Column(String)
    municipio = Column(String)
    comprimento = Column(Integer)
    largura = Column(Integer)
    propria_banho = Column(Boolean, default=True)
    quiosque = Column(Boolean, default=False)
    salvavida = Column(Boolean, default=False)
    rating = Column(Float)

#cria a tabela do db (se ela ja n existir)
Base.metadata.create_all(bind=engine)


app = FastAPI()

#função para obter a sessao do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Projeto de PA2 API sobre praias"}



#GET GERAL
@app.get("/praias/", response_model=list[Praia])
def get_todas_as_praias(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    praias = db.query(PraiaDB).offset(skip).limit(limit).all();
    return praias;

#GET POR ID
@app.get("/praias/{praia_id}", response_model=Praia)
def get_praia_por_id(praia_id: int, db: Session = Depends(get_db)):
    praia_encontrada = db.query(PraiaDB).filter(PraiaDB.id == praia_id).first()
    if praia_encontrada is None:
        raise HTTPException(status_code=404, detail="Praia nao registrada")
    return praia_encontrada

#POST 
@app.post("/praias/", response_model=Praia, status_code=201)
def create_praia(praia: PraiaCreate, db: Session = Depends(get_db)):
    db_praia = PraiaDB(**praia.dict())
    db.add(db_praia)
    db.commit()
    db.refresh(db_praia)
    
    return db_praia