import pymongo

MONGO_URI = "mongodb://mongo:27017"
MONGO_DATABASE = "fipe"
COLLECTION_NAME = "veiculos"

client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]


def salvar_veiculo(item: dict):
    """Salva um veículo no banco de dados.

    Args:
        item: Um dicionário contendo as informações do veículo a ser salvo.

    Returns:
        O resultado da operação de inserção/atualização no banco de dados.
    """
    keys = {
        "codigo": item.get("codigo"),
    }

    return db[COLLECTION_NAME].update_one(
        keys,
        {"$set": dict(item)},
        upsert=True,
    )


def get_veiculo(codigo: str) -> dict:
    """Obtém um veículo do banco de dados pelo código.

    Args:
        codigo: O código do veículo.

    Returns:
        Um dicionário contendo as informações do veículo encontrado.
        Se nenhum veículo for encontrado, retorna um dicionário vazio.
    """
    veiculo_list = [veiculo for veiculo in db[COLLECTION_NAME].find({"codigo": codigo}, {"_id": 0})]
    return veiculo_list[0] if veiculo_list else {}


def listar_marcas() -> list:
    """Lista todas as marcas de veículos disponíveis no banco de dados.

    Returns:
        Uma lista de marcas de veículos.
    """
    return db[COLLECTION_NAME].distinct("marca")


def listar_veiculos(marca: str) -> list:
    """Lista todos os veículos de uma marca específica.

    Args:
        marca: O nome da marca.

    Returns:
        Uma lista de veículos da marca especificada.
    """
    veiculos = db[COLLECTION_NAME].find({"marca": marca}, {"_id": 0})
    return [veiculo for veiculo in veiculos]
