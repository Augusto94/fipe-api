import aiohttp

from api_1.repository.fipe_api1_repository import FipeApi1Repo
from api_1.services.utils import send_to_queue
from common.constants import CATEGORIAS_LIST, FIPE_API_BASE_URL
from common.logger import logger

repo = FipeApi1Repo()


async def atualizar_base_service():
    """Atualiza a base de dados com informações de marcas para cada categoria.

    Faz uma chamada à API externa para obter as marcas de cada categoria.
    Em seguida, envia os dados de cada marca para uma fila.

    Raises:
        Exception: Caso ocorra um erro durante o processo de atualização.
    """
    async with aiohttp.ClientSession() as session:
        for categoria in CATEGORIAS_LIST:
            logger.info(f"Buscando as marcas na api externa para a categoria {categoria}.")
            url = FIPE_API_BASE_URL + f"/{categoria}/marcas"
            async with session.get(url) as resp:
                marcas = await resp.json()
                for marca_info in marcas:
                    logger.info(f"Enviando os dados da marca {marca_info.get('nome')} para fila.")
                    marca_info["categoria"] = categoria
                    await send_to_queue(marca_info)


async def list_marcas_service() -> list:
    """Lista as marcas disponíveis.

    Returns:
        Uma lista de marcas.
    """
    return await repo.listar_marcas()


async def list_veiculos_service(marca: str) -> list:
    """Lista os veículos de uma marca específica.

    Args:
        marca: O nome da marca desejada.

    Returns:
        Uma lista de veículos da marca especificada.
    """
    return await repo.listar_veiculos(marca=marca)
