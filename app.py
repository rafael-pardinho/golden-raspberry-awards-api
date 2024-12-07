from fastapi import FastAPI, HTTPException
import csv
import os
import sqlite3

# Configurações do banco de dados SQLite em memória
DATABASE_PATH = ":memory:"

# Conexão global compartilhada
global_connection = None

def initialize_connection():
    global global_connection
    if global_connection is None:
        global_connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        global_connection.row_factory = sqlite3.Row  # Permite acessar colunas por nome

def get_connection():
    return global_connection


# A função create_tables() é responsável por garantir que a tabela movies seja criada no banco de dados
def create_tables():
    print("Inicializando o banco de dados...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Criar tabela se não existir
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
        print("Tabela 'movies' criada ou já existe.")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
        
# A função populate_data() é responsável por inserir os dados do arquivo CSV no banco de dados SQLite
def populate_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Verificar se o arquivo CSV existe
    csv_path = "data/movielist.csv"
    if not os.path.exists(csv_path):
        print(f"Erro: Arquivo CSV não encontrado em {csv_path}")
        return

    try:
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
            print("Banco de dados populado com sucesso.")
    except Exception as e:
        print(f"Erro ao carregar os dados do CSV: {e}")

# Configurar ciclo de vida do FastAPI
async def lifespan(app: FastAPI):
    initialize_connection()
    create_tables()
    populate_data()
    yield
    
app = FastAPI(lifespan=lifespan)


@app.get("/producers/intervals")

#A função get_producer_intervals() implementa a lógica para calcular os intervalos de tempo entre prêmios consecutivos ganhos por produtores na tabela movies
def get_producer_intervals():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Verificar se a tabela existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='movies'")
        if not cursor.fetchone():
            raise HTTPException(status_code=500, detail="Tabela 'movies' não encontrada. Banco não inicializado corretamente.")

        print("Tabela 'movies' encontrada no banco de dados.")

        # Consultar filmes vencedores
        cursor.execute("SELECT * FROM movies WHERE winner = 1")
        winners = cursor.fetchall()

        if not winners:
            # Atualize aqui para retornar 404
            raise HTTPException(status_code=404, detail="Nenhum vencedor encontrado no banco de dados.")

        print(f"{len(winners)} vencedores encontrados no banco de dados.")

        producer_intervals = {}
        for movie in winners:
            producers = [p.strip() for p in movie["producers"].split(",")]
            for producer in producers:
                if producer not in producer_intervals:
                    producer_intervals[producer] = []
                producer_intervals[producer].append(movie["year"])

        # Calcular intervalos
        min_intervals = []
        max_intervals = []
        for producer, years in producer_intervals.items():
            years.sort()
            intervals = [years[i + 1] - years[i] for i in range(len(years) - 1)]
            if intervals:
                min_interval = min(intervals)
                max_interval = max(intervals)
                min_intervals.append({
                    "producer": producer,
                    "interval": min_interval,
                    "previousWin": years[intervals.index(min_interval)],
                    "followingWin": years[intervals.index(min_interval) + 1]
                })
                max_intervals.append({
                    "producer": producer,
                    "interval": max_interval,
                    "previousWin": years[intervals.index(max_interval)],
                    "followingWin": years[intervals.index(max_interval) + 1]
                })

        print(f"Intervalos calculados com sucesso. Min: {len(min_intervals)}, Max: {len(max_intervals)}")

        return {
            "min": sorted(min_intervals, key=lambda x: x["interval"]),
            "max": sorted(max_intervals, key=lambda x: x["interval"], reverse=True)
        }
    except HTTPException as e:
        # Mantenha o comportamento esperado para HTTPException
        raise e
    except Exception as e:
        print(f"Erro ao calcular intervalos: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao calcular intervalos: {e}")
