from typing import Dict, List

from common.database import db


class FipeApi1Repo:
    async def listar_marcas(self) -> List[str]:
        """
        Lista todas as marcas de veículos disponíveis no banco de dados.

        Returns:
            Uma lista de marcas de veículos.
        """
        return db.list_by_field(field="marca")

    async def listar_veiculos(self, marca: str) -> List[Dict[str, str]]:
        """
        Lista todos os veículos de uma marca específica.

        Args:
            marca: O nome da marca.

        Returns:
            Uma lista de veículos da marca especificada.
        """
        return db.list_items(field="marca", value=marca)
