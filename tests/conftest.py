import os
from unittest.mock import MagicMock, Mock, patch

import pytest
from dotenv import load_dotenv

from src.config import DB_NAME, HOST, PORT
from src.dbm import DBManager

load_dotenv()
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")


@pytest.fixture
def mock_requests_get(monkeypatch):
    def mock_response(status_code, json_data=None):
        resp_mock = Mock()
        resp_mock.status_code = status_code
        resp_mock.json.return_value = json_data
        return resp_mock

    with patch(
        "requests.get",
        side_effect=lambda *args, **kwargs: mock_response(
            kwargs.get("params").get("text"),
            json_data={
                "items": [{"id": "12345", "name": kwargs.get("params").get("text")}]
            },
        ),
    ):
        yield


@pytest.fixture
def db_connection_params():
    return {
        "dbname": DB_NAME,
        "user": USER,
        "password": PASSWORD,
        "host": HOST,
        "port": PORT
    }


@pytest.fixture
def db_manager(db_connection_params):
    manager = DBManager(db_connection_params)
    manager.conn = MagicMock()
    return manager


@pytest.fixture
def mock_db_connection():
    """Фикстура для имитации подключения к базе данных"""
    with patch("src.data.psycopg2.connect") as mock_conn:
        yield mock_conn
