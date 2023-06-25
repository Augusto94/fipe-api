import aiohttp

from common.constants import FIPE_API_BASE_URL


async def get_modelos(cod_marca: str, categoria: str) -> list:
    """Obtém os modelos de veículos de uma determinada marca e categoria.

    Args:
        cod_marca: O código da marca.
        categoria: A categoria dos veículos (por exemplo: carros, motos, caminhoes).

    Returns:
        Uma lista de modelos de veículos.
    """
    async with aiohttp.ClientSession() as session:
        url = f"{FIPE_API_BASE_URL}/{categoria}/marcas/{cod_marca}/modelos"
        async with session.get(url) as resp:
            response = await resp.json()
            return response.get("modelos")
