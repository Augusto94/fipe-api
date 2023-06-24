import pytest
from fastapi.testclient import TestClient

from api_1.main import app


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client


def test_health_check(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_update_data(test_client):
    response = test_client.get("/atualizar-dados")
    assert response.status_code == 200
    assert response.json() == {"message": "Marcas enviadas para a fila."}


def test_list_marcas(test_client):
    response = test_client.get("/marcas/")
    assert response.status_code == 200
    # Verifique se a resposta é uma lista (opcional)
    assert isinstance(response.json(), list)


def test_list_veiculos(test_client):
    # Primeiro, atualize os dados para garantir que haja marcas disponíveis
    response = test_client.get("/atualizar-dados")
    assert response.status_code == 200

    # Obtenha a lista de marcas disponíveis
    response = test_client.get("/marcas/")
    assert response.status_code == 200
    marcas = response.json()
    assert isinstance(marcas, list)
    assert len(marcas) > 0

    # Teste a função list_veiculos para cada marca disponível
    for marca in marcas:
        response = test_client.get(f"/veiculos/{marca}")
        assert response.status_code == 200
        # Verifique se a resposta é uma lista (opcional)
        assert isinstance(response.json(), list)