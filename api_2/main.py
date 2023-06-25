from fastapi import FastAPI

from api_2.schema import MarcaInputDTO, VeiculoInputDTO
from api_2.utils import get_modelos
from database import db

app = FastAPI()


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
    modelos = await get_modelos(marca.codigo, marca.categoria)
    for modelo in modelos:
        veiculo = {
            "codigo": str(modelo.get("codigo")),
            "marca": marca.nome,
            "modelo": modelo.get("nome"),
            "categoria": marca.categoria,
            "observacoes": "",
        }
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
    item = {"codigo": veiculo.codigo}
    if veiculo.modelo is not None:
        item["modelo"] = veiculo.modelo

    if veiculo.observacoes is not None:
        item["observacoes"] = veiculo.observacoes

    db.salvar_veiculo(item)

    return db.get_veiculo(veiculo.codigo)
