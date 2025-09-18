from typing import Union

from fastapi import FastAPI,HTTPException

from pydantic import BaseModel

class Praia(BaseModel):
    id:int
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

app = FastAPI()

praias_mock = {
    1: Praia(id=1, nome="Praia de Iracema", latitude=-3.71, longitude=-38.50, estado="Ceará", municipio="Fortaleza", comprimento=800, largura=50, propria_banho=True, quiosque=True, salvavida=True, rating=4.5),
    2: Praia(id=2, nome="Praia do Futuro", latitude=-3.73, longitude=-38.44, estado="Ceará", municipio="Fortaleza", comprimento=8000, largura=100, propria_banho=True, quiosque=True, salvavida=True, rating=4.8),
    3: Praia(id=3, nome="Copacabana", latitude=-22.97, longitude=-43.18, estado="Rio de Janeiro", municipio="Rio de Janeiro", comprimento=4000, largura=70, propria_banho=False, quiosque=True, salvavida=True, rating=4.9)
}

@app.get("/")
def read_root():
    return {"Hello": "World"}



#GET GERAL
@app.get("/praias/", response_model=list[Praia])
def get_todas_as_praias():
    return list(praias_mock.values())

#GET POR ID
@app.get("/praias/{praia_id}")
def get_praia_id(praia_id: int,praia: Praia):
    praia_encontrada = praias_mock.get(praia_id)
    if not praia_encontrada:
        raise HTTPException(status_code=404, detail="Praia nao registrada")
    return praia_encontrada

#POST 
@app.post("/praias/", response_model=Praia, status_code=201)
def create_praia(praia: Praia):
    novo_id = max(praias_mock.keys()) + 1
    praia.id = novo_id  
    
    praias_mock[novo_id] = praia
    
    print("Praia recebida e salva:", praia)
    
    return praia