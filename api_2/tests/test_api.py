import pytest
from fastapi.testclient import TestClient

from api_2.main import app
from api_2.schema import MarcaInputDTO, VeiculoInputDTO


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client


def test_health_check(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_add_veiculos(test_client):
    marca = MarcaInputDTO(codigo="123", nome="Marca 1", categoria="carros")
    response = test_client.post("/veiculos", json=marca.dict())

    assert response.status_code == 200
    assert response.json() == {"message": "Veiculos da marca Marca 1 salvos com sucesso!"}


def test_atualizar_veiculo(test_client):
    veiculo = VeiculoInputDTO(
        codigo="1", modelo="Integra GS 1.8 Turbo", observacoes="Novas Observações"
    )
    response = test_client.put("/veiculo", json=veiculo.dict())

    assert response.status_code == 200
    assert response.json() == {
        "codigo": "1",
        "marca": "Acura",
        "modelo": "Integra GS 1.8 Turbo",
        "categoria": "carros",
        "observacoes": "Novas Observações",
    }
