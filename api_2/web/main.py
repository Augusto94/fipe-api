from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api_2.services.veiculo_service import (
    adicionar_veiculos_service,
    atualizar_veiculo_service,
)
from api_2.web.schema import MarcaInputDTO, VeiculoUpdateDTO
from common.logger import logger

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health_check() -> dict:
    """Verifica o estado de saúde do serviço.

    Returns:
        Um dicionário contendo a chave 'status' indicando a saúde do serviço.
    """
    return {"status": "healthy"}


@app.post("/veiculos")
async def add_veiculos(marca: MarcaInputDTO) -> dict:
    """Adiciona veículos de uma marca no banco de dados.

    Args:
        marca: Um objeto MarcaInputDTO contendo as informações da marca.

    Returns:
        Uma lista de modelos de veículos adicionados.
    """
    logger.info(
        f"Buscando e salvando no banco os veículos da marca {marca.nome} da categoria {marca.categoria}."
    )
    await adicionar_veiculos_service(marca.codigo, marca.nome, marca.categoria)

    return {"message": f"Veiculos da marca {marca.nome} salvos com sucesso!"}


@app.put("/veiculo")
async def atualizar_veiculo(veiculo: VeiculoUpdateDTO) -> dict:
    """Atualiza as informações de um veículo.

    Args:
        veiculo: Um objeto VeiculoInputDTO contendo as informações do veículo a ser atualizado.

    Returns:
        Um dicionário contendo as informações atualizadas do veículo.
    """
    logger.info(f"Atualizando os dados do veículo de código {veiculo.codigo}.")
    return await atualizar_veiculo_service(veiculo.codigo, veiculo.modelo, veiculo.observacoes)
