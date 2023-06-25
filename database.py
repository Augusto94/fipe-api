import os
from typing import Dict, List

import pymongo
from google.cloud import firestore


class FirestoreDatabase:
    def __init__(self):
        self.db = firestore.Client()
        self.collection_name = "veiculos"

    def salvar_veiculo(self, item: Dict[str, str]) -> None:
        """
        Salva um veículo no banco de dados.

        Args:
            item: Um dicionário contendo as informações do veículo a ser salvo.
        """
        doc_ref = self.db.collection(self.collection_name).document(item.get("codigo"))
        doc_ref.update(item)

    def get_veiculo(self, codigo: str) -> Dict[str, str]:
        """
        Obtém um veículo do banco de dados pelo código.

        Args:
            codigo: O código do veículo.

        Returns:
            Um dicionário contendo as informações do veículo encontrado.
            Se nenhum veículo for encontrado, retorna um dicionário vazio.
        """
        doc_ref = self.db.collection(self.collection_name).document(codigo)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        return {}

    def listar_marcas(self) -> List[str]:
        """
        Lista todas as marcas de veículos disponíveis no banco de dados.

        Returns:
            Uma lista de marcas de veículos.
        """
        docs = self.db.collection(self.collection_name).stream()
        marcas = set()
        for doc in docs:
            marcas.add(doc.to_dict().get("marca"))
        return list(marcas)

    def listar_veiculos(self, marca: str) -> List[Dict[str, str]]:
        """
        Lista todos os veículos de uma marca específica.

        Args:
            marca: O nome da marca.

        Returns:
            Uma lista de veículos da marca especificada.
        """
        veiculos = []
        docs = self.db.collection(self.collection_name).where("marca", "==", marca).stream()
        for doc in docs:
            veiculos.append(doc.to_dict())

        return veiculos


class MongoDatabase:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://mongo:27017")
        self.db = self.client["fipe"]
        self.collection_name = "veiculos"

    def salvar_veiculo(self, item: Dict[str, str]) -> pymongo.results.UpdateResult:
        """
        Salva um veículo no banco de dados.

        Args:
            item: Um dicionário contendo as informações do veículo a ser salvo.

        Returns:
            O resultado da operação de inserção/atualização no banco de dados.
        """
        keys = {
            "codigo": item.get("codigo"),
        }
        return self.db[self.collection_name].update_one(
            keys,
            {"$set": dict(item)},
            upsert=True,
        )

    def get_veiculo(self, codigo: str) -> Dict[str, str]:
        """
        Obtém um veículo do banco de dados pelo código.

        Args:
            codigo: O código do veículo.

        Returns:
            Um dicionário contendo as informações do veículo encontrado.
            Se nenhum veículo for encontrado, retorna um dicionário vazio.
        """
        veiculo_list = [
            veiculo
            for veiculo in self.db[self.collection_name].find({"codigo": codigo}, {"_id": 0})
        ]
        return veiculo_list[0] if veiculo_list else {}

    def listar_marcas(self) -> List[str]:
        """
        Lista todas as marcas de veículos disponíveis no banco de dados.

        Returns:
            Uma lista de marcas de veículos.
        """
        return self.db[self.collection_name].distinct("marca")

    def listar_veiculos(self, marca: str) -> List[Dict[str, str]]:
        """
        Lista todos os veículos de uma marca específica.

        Args:
            marca: O nome da marca.

        Returns:
            Uma lista de veículos da marca especificada.
        """
        veiculos = self.db[self.collection_name].find({"marca": marca}, {"_id": 0})
        return [veiculo for veiculo in veiculos]


db = MongoDatabase() if os.getenv("ENVIRONMENT") == "local" else FirestoreDatabase()
