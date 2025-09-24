from models.praia import Praia
from db.session import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def seed():
    db = next(get_db())

    praias_data = [
        {
            "nome": "Praia de Iracema",
            "latitude": -3.720235,
            "longitude": -38.528434,
            "estado": "CE",
            "municipio": "Fortaleza",
            "comprimento": 1500,
            "largura": 50,
            "propria_banho": True,
            "tem_quiosque": True,
            "tem_salvavida": True,
            "rating": 4.5,
        },
        {
            "nome": "Praia de Copacabana",
            "latitude": -22.971556,
            "longitude": -43.184306,
            "estado": "RJ",
            "municipio": "Rio de Janeiro",
            "comprimento": 4000,
            "largura": 100,
            "propria_banho": True,
            "tem_quiosque": True,
            "tem_salvavida": True,
            "rating": 4.7,
        },
        {
            "nome": "Praia do Sancho",
            "latitude": -3.855000,
            "longitude": -32.443056,
            "estado": "PE",
            "municipio": "Fernando de Noronha",
            "comprimento": 300,
            "largura": 30,
            "propria_banho": True,
            "tem_quiosque": False,
            "tem_salvavida": False,
            "rating": 5.0,
        },
    ]

    print("Inserindo praias...")
    for data in praias_data:
        praia = Praia(**data)
        db.add(praia)
        print("Adicionado praia: ", praia.nome)

    db.commit()
    print("Seed concluído! As praias foram inseridas.")
