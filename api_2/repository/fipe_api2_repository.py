from typing import Dict

from common.database import db


class FipeApi2Repo:
    async def salvar_veiculo(self, item: dict):
        """
        Salva um veículo no banco de dados.

        Args:
            item: Um dicionário contendo as informações do veículo a ser salvo.

        Returns:
            O resultado da operação de inserção/atualização no banco de dados.
        """
        db.create_or_update(item=item, key=item.get("codigo"))

    async def get_veiculo(self, codigo: str) -> Dict[str, str]:
        """
        Obtém um veículo do banco de dados pelo código.

        Args:
            codigo: O código do veículo.

        Returns:
            Um dicionário contendo as informações do veículo encontrado.
            Se nenhum veículo for encontrado, retorna um dicionário vazio.
        """
        return db.get_item(field="codigo", value=codigo)
