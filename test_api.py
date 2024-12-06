import pytest
from fastapi.testclient import TestClient
from app import app, initialize_connection, create_tables, get_connection