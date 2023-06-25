import pytest
from fastapi.testclient import TestClient

from api_2.web.main import app
from api_2.web.schema import MarcaInputDTO, VeiculoInputDTO


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client


def test_health_check(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_add_veiculos(test_client):
    marca = MarcaInputDTO(codigo="5", nome="Asia Motors", categoria="carros")
    response = test_client.post("/veiculos", json=marca.dict())

    assert response.status_code == 200
    assert response.json() == {"message": "Veiculos da marca Asia Motors salvos com sucesso!"}


def test_atualizar_veiculo(test_client):
    veiculo = VeiculoInputDTO(
        codigo="24", modelo="AM-825 Luxo 4.0 Diesel", observacoes="Novas Observações Teste"
    )
    response = test_client.put("/veiculo", json=veiculo.dict())

    assert response.status_code == 200
    assert response.json() == {
        "codigo": "24",
        "marca": "Asia Motors",
        "modelo": "AM-825 Luxo 4.0 Diesel",
        "categoria": "carros",
        "observacoes": "Novas Observações Teste",
    }
