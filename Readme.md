# 🌊 Praia API

API REST para gerenciamento de praias e quiosques.  
A documentação interativa é gerada automaticamente usando **OpenAPI/Swagger**.

---

## 📚 Índice
- [Visão Geral](#-visão-geral)
- [Tecnologias](#-tecnologias)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Execução](#-execução)
- [Documentação da API](#-documentação-da-api)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Exemplos de Uso](#-exemplos-de-uso)
- [Contribuição](#-contribuição)
- [Licença](#-licença)

---

## 🚀 Visão Geral
A **Praia API** fornece endpoints para:
- 🏖️ Listagem e gerenciamento de praias
- 🏪 Gerenciamento de quiosques

---

## 🛠 Tecnologias
- [Python 3.11+](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Uvicorn](https://www.uvicorn.org/)
- [OpenAPI 3](https://swagger.io/specification/)

---

## 📦 Pré-requisitos
- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/) 
- Banco de dados PostgreSQL configurado (opcional, necessário caso não use o Docker Compose)

---

## ⚙️ Instalação

Clone o repositório:
```bash
git clone https://github.com/seu-usuario/api_praias.git
cd api_praias
```

Crie um ambiente virtual e instale as dependências:
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

Configure as variáveis de ambiente (por exemplo, no arquivo `.env`):
```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/praia_db
ENV=development
```

---

## ▶️ Execução

### Via Python/Uvicorn
```bash
uvicorn main:app --reload
```

### Via Docker
```bash
docker-compose up --build
```

A API estará disponível em:
```
http://localhost:8000
```

---

## 📜 Documentação da API

A documentação interativa (OpenAPI/Swagger) é gerada automaticamente:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Esquema OpenAPI (JSON):** [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

---

## 📁 Estrutura do Projeto
```
api_praias/
├── api/                # Rotas e controladores da API
├── core/               # Configurações centrais (settings, middlewares)
├── db/                 # Conexão e inicialização do banco de dados
├── models/             # Modelos do SQLAlchemy
├── schemas/            # Schemas do Pydantic
├── seeds/              # Scripts de seed (dados iniciais)
├── docker-compose.yml  # Configuração Docker Compose
├── Dockerfile          # Dockerfile para build da aplicação
├── main.py             # Ponto de entrada da aplicação FastAPI
├── requirements.txt    # Dependências do Python
└── README.md           # Documentação do projeto
```

---

## 📘 Exemplos de Uso

A API segue o padrão REST e retorna **JSON**.  
As URLs assumem que a API está rodando em `http://localhost:8000`.

---

### 🌊 Praias

#### 1. Listar praias com filtros
```bash
curl -X GET "http://localhost:8000/api/v1/praia/?estado=CE&municipio=Fortaleza&min_rating=3"      -H "accept: application/json"
```

**Response (200)**
```json
[
  {
    "id": 1,
    "nome": "Praia do Futuro",
    "estado": "CE",
    "municipio": "Fortaleza",
    "latitude": -3.722,
    "longitude": -38.476,
    "tem_salvavida": true,
    "rating": 4.5,
    "quiosques": []
  }
]
```

#### 2. Criar uma nova praia
```bash
curl -X POST "http://localhost:8000/api/v1/praia/"      -H "Content-Type: application/json"      -d '{
           "nome": "Praia do Cumbuco",
           "estado": "CE",
           "municipio": "Caucaia",
           "latitude": -3.630,
           "longitude": -38.740,
           "propria_banho": true,
           "tem_salvavida": false,
           "rating": 4.2
         }'
```

**Response (201)**
```json
{
  "id": 2,
  "nome": "Praia do Cumbuco",
  "estado": "CE",
  "municipio": "Caucaia",
  "latitude": -3.630,
  "longitude": -38.740,
  "propria_banho": true,
  "tem_salvavida": false,
  "rating": 4.2,
  "quiosques": []
}
```

#### 3. Obter praia por ID
```bash
curl -X GET "http://localhost:8000/api/v1/praia/2"      -H "accept: application/json"
```

#### 4. Atualizar uma praia (PUT)
```bash
curl -X PUT "http://localhost:8000/api/v1/praia/2"      -H "Content-Type: application/json"      -d '{
           "nome": "Praia do Cumbuco Atualizada",
           "estado": "CE",
           "municipio": "Caucaia",
           "latitude": -3.630,
           "longitude": -38.740,
           "propria_banho": false,
           "tem_salvavida": true,
           "rating": 4.7
         }'
```

#### 5. Remover uma praia
```bash
curl -X DELETE "http://localhost:8000/api/v1/praia/2"
```

---

### 🏪 Quiosques

#### 1. Listar quiosques com filtros
```bash
curl -X GET "http://localhost:8000/api/v1/quiosque/?praia_id=1&tem_banheiro=true"      -H "accept: application/json"
```

#### 2. Criar um quiosque
```bash
curl -X POST "http://localhost:8000/api/v1/quiosque/"      -H "Content-Type: application/json"      -d '{
           "nome": "Quiosque Mar Azul",
           "praia_id": 1,
           "latitude": -3.721,
           "longitude": -38.477,
           "tem_acessibilidade": true,
           "tem_banheiro": false,
           "valor": 35
         }'
```

#### 3. Atualizar um quiosque (PATCH)
```bash
curl -X PATCH "http://localhost:8000/api/v1/quiosque/2"      -H "Content-Type: application/json"      -d '{"valor": 40, "tem_banheiro": true}'
```

#### 4. Remover um quiosque
```bash
curl -X DELETE "http://localhost:8000/api/v1/quiosque/2"
```

---

## 🤝 Contribuição
1. Faça um fork do repositório
2. Crie um branch (`git checkout -b feature/minha-feature`)
3. Commit suas mudanças (`git commit -m "feat: nova funcionalidade"`)
4. Envie para o branch (`git push origin feature/minha-feature`)
5. Abra um Pull Request

---

## 📄 Licença
Este projeto está sob a licença MIT.  
Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
