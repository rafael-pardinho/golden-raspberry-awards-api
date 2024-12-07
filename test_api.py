import pytest
from fastapi.testclient import TestClient
from app import app, initialize_connection, create_tables, get_connection

@pytest.fixture(scope="function")
def setup_database():
    """
    Fixture para configurar um banco de dados limpo antes de cada teste.
    """
    # Inicializar a conexão global
    initialize_connection()

    # Criar tabelas
    create_tables()

    # Preencher com dados de teste
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO movies (year, title, studios, producers, winner)
        VALUES (?, ?, ?, ?, ?)
    """, [
        (2001, "Movie A", "Studio A", "Producer A", 1),
        (2002, "Movie B", "Studio B", "Producer A, Producer B", 1),
        (2005, "Movie C", "Studio C", "Producer B", 1),
    ])
    conn.commit()

    yield  # Passa controle para o teste

    # Limpa o banco após o teste
    cursor.execute("DROP TABLE IF EXISTS movies")
    conn.commit()
    
def test_get_producer_intervals_success(setup_database):
    """
    Testa o endpoint /producers/intervals com dados válidos.
    """
    client = TestClient(app)
    response = client.get("/producers/intervals")
    assert response.status_code == 200

    data = response.json()
    assert "min" in data
    assert "max" in data

    # Verifica os dados mínimos
    min_producer = data["min"][0]
    assert min_producer["producer"] == "Producer A"
    assert min_producer["interval"] == 1

    # Verifica os dados máximos
    max_producer = data["max"][0]
    assert max_producer["producer"] == "Producer B"
    assert max_producer["interval"] == 3

def test_get_producer_intervals_no_data():
    """
    Testa o endpoint /producers/intervals quando não há dados no banco.
    """
    initialize_connection()
    create_tables()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movies")
    conn.commit()

    client = TestClient(app)
    response = client.get("/producers/intervals")
    assert response.status_code == 404
    assert response.json() == {"detail": "Nenhum vencedor encontrado no banco de dados."}