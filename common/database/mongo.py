from typing import Dict, List

import pymongo


class MongoDatabase:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://mongo:27017")
        self.db = self.client["fipe"]
        self.collection_name = "veiculos"

    def create_or_update(self, item: dict, key: str) -> pymongo.results.UpdateResult:
        """
        Salva um item no banco de dados.

        Args:
            item: Um dicionário contendo as informações do veículo a ser salvo.
            key: Chave do processo. Será usada para criar o ID e atualizar objetos.

        Returns:
            O resultado da operação de inserção/atualização no banco de dados.
        """
        keys = {
            "codigo": key,
        }
        return self.db[self.collection_name].update_one(
            keys,
            {"$set": dict(item)},
            upsert=True,
        )

    def get_item(self, field: str, value: str) -> Dict[str, str]:
        """
        Obtém um item do banco de dados pelo valor passado.

        Args:
            field: O campo que será usado na busca.
            value: O valor do campo que será buscado no banco.

        Returns:
            Um dicionário contendo as informações encontradas.
            Se nenhum item for encontrado, retorna um dicionário vazio.
        """
        items_list = [
            items for items in self.db[self.collection_name].find({field: value}, {"_id": 0})
        ]
        return items_list[0] if items_list else {}

    def list_by_field(self, field: str) -> List[str]:
        """
        Lista todas as valores distintos de field específico.

        Returns:
            Uma lista com os valores distintos no banco para o field específicado.
        """
        return sorted(self.db[self.collection_name].distinct(field))

    def list_items(self, field: str, value: str) -> List[Dict[str, str]]:
        """
        Lista todos os items de um valor de um campo específico.

        Args:
            field: O campo que será usado na busca.
            value: O valor do campo que será buscado no banco.

        Returns:
            Uma lista contendo as informações encontradas.
        """
        veiculos = self.db[self.collection_name].find({field: value}, {"_id": 0})
        return [veiculo for veiculo in veiculos]
