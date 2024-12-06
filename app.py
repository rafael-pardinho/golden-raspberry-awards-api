from fastapi import FastAPI, HTTPException
import csv
import os
import sqlite3

# Configurações do banco de dados SQLite em memória
DATABASE_PATH = ":memory:"

# Conexão global compartilhada
global_connection = None