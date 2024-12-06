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