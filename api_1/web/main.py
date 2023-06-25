from fastapi import FastAPI

from api_1.services.marca_service import (
    atualizar_base_service,
    list_marcas_service,
    list_veiculos_service,
)
from common.logger import logger

app = FastAPI()


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
    await atualizar_base_service()
    return {"message": "Marcas enviadas para a fila."}


@app.get("/marcas/")
async def list_marcas() -> list:
    """Lista as marcas disponíveis.

    Returns:
        Uma lista de marcas.
    """
    logger.info("Listando todas as marcas dos veículos.")
    return await list_marcas_service()


@app.get("/veiculos/{marca}")
async def list_veiculos(marca: str) -> list:
    """Lista os veículos de uma marca específica.

    Args:
        marca: O nome da marca desejada.

    Returns:
        Uma lista de veículos da marca especificada.
    """
    logger.info(f"Listando as informações dos veículos da marca {marca}.")
    return await list_veiculos_service(marca)
