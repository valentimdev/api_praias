# Use a imagem oficial do Python 3.10 em sua versão slim
FROM python:3.10-slim

# Defina o diretório de trabalho no container.
WORKDIR /app

# Copie apenas o arquivo de dependências para aproveitar o cache
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o seu projeto para o diretório de trabalho do container.
# Isso garante que tudo, incluindo o 'main.py' e as pastas, estejam lá.
COPY . .

# Exponha a porta que a aplicação vai usar
EXPOSE 8000

# A sua importação de 'core' agora está na raiz do projeto, então o comando
# Uvicorn pode ser simples e direto.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
