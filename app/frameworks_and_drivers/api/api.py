from fastapi import FastAPI
from app.frameworks_and_drivers.database.sqlite_handler import SQLiteHandler
from app.interface_adapters.repositories.movie_repository import MovieRepository
from app.interface_adapters.controllers.producer_controller import ProducerController

app = FastAPI()

'''
inicializa um servidor FastAPI, configura o banco de dados SQLite, 
cria a tabela de filmes, carrega dados de um CSV e expõe um endpoint 
para calcular intervalos de prêmios de produtores
'''

# Setup Database and Repositories
db_handler = SQLiteHandler()
movie_repository = MovieRepository(db_handler.get_connection())
producer_controller = ProducerController(movie_repository)

# Criar tabela e carregar dados
def initialize_database():
    conn = db_handler.get_connection()
    cursor = conn.cursor()

    # Criar tabela
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER,
        title TEXT,
        studios TEXT,
        producers TEXT,
        winner BOOLEAN
    )
    """)
    conn.commit()

    # Popular com dados do CSV
    import os
    import csv
    csv_path = "data/movielist.csv"
    if os.path.exists(csv_path):
        with open(csv_path, "r") as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                cursor.execute("""
                INSERT INTO movies (year, title, studios, producers, winner)
                VALUES (?, ?, ?, ?, ?)
                """, (
                    int(row["year"]),
                    row["title"],
                    row["studios"],
                    row["producers"],
                    row["winner"].lower() == "yes"
                ))
        conn.commit()

# Inicializar o banco de dados ao iniciar
initialize_database()

@app.get("/producers/intervals")
def get_producer_intervals():
    result, status = producer_controller.get_producer_intervals()
    return result if status == 200 else {"detail": result}, status
