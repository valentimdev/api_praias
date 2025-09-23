
FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./main.py /app/main.py

EXPOSE 8000

# Comando para iniciar a aplicação quando o container for executado
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]