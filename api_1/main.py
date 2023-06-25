import json

import aiohttp
import redis
from fastapi import FastAPI

from database import db

app = FastAPI()

# Conectar-se ao Redis
redis_client = redis.Redis(host="redis", port=6379, db=0)


@app.get("/")
async def health_check() -> dict:
    """Verifica o estado de saúde do serviço.

    Returns:
        Um dicionário contendo a chave 'status' indicando a saúde do serviço.
    """
    return {"status": "healthy"}


@app.get("/atualizar-dados")
async def update_data() -> dict:
    """Atualiza os dados das marcas no Redis.

    Faz uma solicitação assíncrona para cada categoria e armazena as marcas no Redis.

    Returns:
        Um dicionário com uma mensagem informando que as marcas foram enviadas para a fila.
    """
    url_marcas = "https://parallelum.com.br/fipe/api/v1/{categoria}/marcas".format
    categorias_list = ["carros", "motos", "caminhoes"]
    async with aiohttp.ClientSession() as session:
        for categoria in categorias_list:
            url = url_marcas(categoria=categoria)
            async with session.get(url) as resp:
                marcas = await resp.json()
                for marca in marcas:
                    marca["categoria"] = categoria
                    redis_client.rpush("marcas-queue", json.dumps(marca))

    return {"message": "Marcas enviadas para a fila."}


@app.get("/marcas/")
async def list_marcas() -> list:
    """Lista as marcas disponíveis.

    Returns:
        Uma lista de marcas.
    """
    return db.listar_marcas()


@app.get("/veiculos/{marca}")
async def list_veiculos(marca: str) -> list:
    """Lista os veículos de uma marca específica.

    Args:
        marca: O nome da marca desejada.

    Returns:
        Uma lista de veículos da marca especificada.
    """
    return db.listar_veiculos(marca)
