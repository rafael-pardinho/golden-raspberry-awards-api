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