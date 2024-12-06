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

