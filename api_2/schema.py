from pydantic import BaseModel


class MarcaInputDTO(BaseModel):
    codigo: str
    nome: str
    categoria: str


class VeiculoInputDTO(BaseModel):
    codigo: str
    modelo: str | None
    observacoes: str | None
