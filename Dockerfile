# Imagem base para construir a aplicação FastAPI
FROM python:3.11-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie os arquivos de configuração e código-fonte da aplicação para o diretório de trabalho
COPY pyproject.toml .
COPY . .

# Instale as dependências
RUN pip install poetry==1.5.1
RUN poetry config virtualenvs.create false
RUN poetry install

# Defina a porta em que a aplicação estará escutando
EXPOSE 8000
EXPOSE 8001

# Argumento para selecionar a aplicação a ser iniciada
ARG APP_NAME
ARG GCP_AUTH

# Execute o comando para iniciar a aplicação
CMD ["bash", "-c", "if [ \"$APP_NAME\" = \"api1\" ]; then uvicorn api_1.web.main:app --host 0.0.0.0 --port 8000; elif [ \"$APP_NAME\" = \"api2\" ]; then uvicorn api_2.web.main:app --host 0.0.0.0 --port 8001; fi"]
