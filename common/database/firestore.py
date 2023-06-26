from typing import Dict, List

from google.cloud import firestore


class FirestoreDatabase:
    def __init__(self):
        self.db = firestore.Client()
        self.collection_name = "veiculos"
        self.collection = self.db.collection(self.collection_name)

    def create_or_update(self, item: dict, key: str) -> None:
        """
        Salva um item no banco de dados.

        Args:
            item: Um dicionário contendo as informações do veículo a ser salvo.
            key: Chave do processo. Será usada para criar o ID e atualizar objetos.
        """
        doc_ref = self.collection.document(key)
        try:
            doc_ref.update(item)
        except Exception:
            doc_ref.set(item)

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
        doc_ref = self.collection.document(value)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()

        return {}

    def list_by_field(self, field: str) -> List[str]:
        """
        Lista todas as valores distintos de field específico.

        Returns:
            Uma lista com os valores distintos no banco para o field específicado.
        """
        docs = self.collection.stream()
        marcas = set()
        for doc in docs:
            if doc.to_dict().get(field):
                marcas.add(doc.to_dict().get(field))

        return sorted(list(marcas))

    def list_items(self, field: str, value: str) -> List[Dict[str, str]]:
        """
        Lista todos os items de um valor de um campo específico.

        Args:
            field: O campo que será usado na busca.
            value: O valor do campo que será buscado no banco.

        Returns:
            Uma lista contendo as informações encontradas.
        """
        veiculos = []
        docs = self.collection.where(field, "==", value).stream()
        for doc in docs:
            veiculos.append(doc.to_dict())

        return veiculos
