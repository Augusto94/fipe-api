from api_2.repository.fipe_api2_repository import FipeApi2Repo
from api_2.services.utils import get_modelos
from common.logger import logger

repo = FipeApi2Repo()


async def adicionar_veiculos_service(marca_codigo: str, marca_nome: str, marca_categoria) -> dict:
    """Adiciona veículos ao banco de dados para uma determinada marca.

    Obtém os modelos de veículos para a marca especificada e os adiciona ao banco de dados.
    Cada veículo contém informações como código, marca, modelo, categoria e observações.

    Args:
        marca_codigo: O código da marca.
        marca_nome: O nome da marca.
        marca_categoria: A categoria da marca.

    Returns:
        Um dicionário contendo informações sobre os modelos de veículos adicionados.

    Raises:
        Exception: Caso ocorra um erro durante o processo de adição de veículos.
    """
    modelos = await get_modelos(marca_codigo, marca_categoria)
    for modelo in modelos:
        veiculo = {
            "codigo": str(modelo.get("codigo")),
            "marca": marca_nome,
            "modelo": modelo.get("nome"),
            "categoria": marca_categoria,
            "observacoes": "",
        }
        logger.info(
            f"Salvando no banco os dados do veículo de modelo {modelo.get('nome')} da marca {marca_nome}."
        )
        await repo.salvar_veiculo(veiculo)


async def atualizar_veiculo_service(codigo: str, modelo: str, observacoes: str) -> dict:
    """Atualiza as informações de um veículo.

    Args:
        veiculo: Um objeto VeiculoInputDTO contendo as informações do veículo a ser atualizado.

    Returns:
        Um dicionário contendo as informações atualizadas do veículo.
    """
    item = {"codigo": codigo}
    if modelo is not None:
        item["modelo"] = modelo

    if observacoes is not None:
        item["observacoes"] = observacoes

    await repo.salvar_veiculo(item)

    return await repo.get_veiculo(codigo)
