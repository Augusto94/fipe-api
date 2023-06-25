from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api_2.schema import MarcaInputDTO, VeiculoInputDTO
from api_2.utils import get_modelos
from common.database import db
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
    logger.info(f"Buscando os veículos da marca {marca.nome} da categoria {marca.categoria}.")
    modelos = await get_modelos(marca.codigo, marca.categoria)
    for modelo in modelos:
        veiculo = {
            "codigo": str(modelo.get("codigo")),
            "marca": marca.nome,
            "modelo": modelo.get("nome"),
            "categoria": marca.categoria,
            "observacoes": "",
        }
        logger.info(
            f"Salvando no banco os dados do veículo de modelo {modelo.get('nome')} da marca {marca.nome}."
        )
        db.salvar_veiculo(veiculo)

    return {"message": f"Veiculos da marca {marca.nome} salvos com sucesso!"}


@app.put("/veiculo")
async def atualizar_veiculo(veiculo: VeiculoInputDTO) -> dict:
    """Atualiza as informações de um veículo.

    Args:
        veiculo: Um objeto VeiculoInputDTO contendo as informações do veículo a ser atualizado.

    Returns:
        Um dicionário contendo as informações atualizadas do veículo.
    """
    logger.info(f"Atualizando os dados do veículo de código {veiculo.codigo}.")
    item = {"codigo": veiculo.codigo}
    if veiculo.modelo is not None:
        item["modelo"] = veiculo.modelo

    if veiculo.observacoes is not None:
        item["observacoes"] = veiculo.observacoes

    db.salvar_veiculo(item)

    return db.get_veiculo(veiculo.codigo)
