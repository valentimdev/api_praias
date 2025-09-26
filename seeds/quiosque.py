from models.quiosque import Quiosque
from db.session import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def seed():
    db = next(get_db())

    quiosques_data = [
        {
            "nome": "Quiosque Sol e Mar",
            "descricao": "Quiosque com drinks e petiscos",
            "praia": 1,
            "nota": 4.5,
            "tem_acessibilidade": True,
            "tem_banheiro": True,
            "valor": 5,
            "ocupacao_maxima": 100,
        },
        {
            "nome": "Quiosque Praia Viva",
            "descricao": "Quiosque familiar",
            "praia": 2,
            "nota": 4.2,
            "tem_acessibilidade": False,
            "tem_banheiro": True,
            "valor": 3,
            "ocupacao_maxima": 80,
        },
        {
            "nome": "Quiosque Mar Azul",
            "descricao": "Quiosque rústico com vista para o mar",
            "praia": 1,
            "nota": 5.0,
            "tem_acessibilidade": True,
            "tem_banheiro": False,
            "valor": 2,
            "ocupacao_maxima": 50,
        },
    ]

    print("Inserindo quiosques...")
    for data in quiosques_data:
        quiosque = Quiosque(**data)
        db.add(quiosque)
        print("Adicionado quiosque: ", quiosque.nome)

    db.commit()
    print("Seed concluído! Os quiosques foram inseridos.")

