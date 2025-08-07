# import pytest
# from unittest.mock import patch, MagicMock
# from src.data import connect_to_db, create_tables, save_employers, save_vacancies
# from src.config import DB_NAME, HOST, PORT, companies
#
# # Тестовые данные
# TEST_COMPANY_IDS = [1, 2]
# TEST_VACANCY_IDS = [101, 102]
# TEST_COMPANIES = [
#     {"id": TEST_COMPANY_IDS[0], "name": "Google", "url": "google.com", "open_vacancies": 10},
#     {"id": TEST_COMPANY_IDS[1], "name": "Yandex", "url": "yandex.ru", "open_vacancies": 20},
# ]
#
# # Фикстура для соединения с базой данных
# @pytest.fixture(scope="module")
# def db_connection():
#     conn = connect_to_db()
#     yield conn
#     conn.close()
#
# # Тесты для создания таблиц
# def test_create_tables(db_connection):
#     create_tables(db_connection)
#     with db_connection.cursor() as cur:
#         cur.execute("SELECT relname FROM pg_class WHERE relkind='r';")
#         tables = cur.fetchall()
#         assert any(table[0] == 'employers' for table in tables)
#         assert any(table[0] == 'vacancies' for table in tables)
#
# # Тесты для сохранения данных о работодателях
# @patch("src.api.get_employer_id", return_value=TEST_COMPANIES)
# def test_save_employers(mock_get_employer_id, db_connection):
#     create_tables(db_connection)
#     save_employers(db_connection, TEST_COMPANIES)
#     with db_connection.cursor() as cur:
#         cur.execute("SELECT * FROM employers;")
#         rows = cur.fetchall()
#         assert len(rows) == len(TEST_COMPANIES)
#         assert rows[0][1] == TEST_COMPANIES[0]['name']
#         assert rows[1][1] == TEST_COMPANIES[1]['name']


import pytest
from unittest.mock import MagicMock, patch
from src.data import connect_to_db, create_tables, save_employers, save_vacancies, fill_tables  # Убедитесь, что импортируете функции корректно

@pytest.fixture
def mock_db_connection():
    """Фикстура для имитации подключения к базе данных"""
    with patch('src.data.psycopg2.connect') as mock_conn:
        yield mock_conn

def test_create_tables(mock_db_connection):
    conn = mock_db_connection.return_value
    create_tables(conn)

    conn.cursor.assert_called_once()
    cursor = conn.cursor.return_value.__enter__.return_value
    cursor.execute.assert_called()

def test_save_employers(mock_db_connection):
    conn = mock_db_connection.return_value
    data_employers = [
        {"id": 1, "name": "Company A", "url": "http://companya.com", "open_vacancies": 10},
        {"id": 2, "name": "Company B", "url": "http://companyb.com", "open_vacancies": 5},
    ]

    save_employers(conn, data_employers)

    conn.cursor.assert_called_once()
    cursor = conn.cursor.return_value.__enter__.return_value
    cursor.execute.assert_called()  # Можно добавить дополнительные проверки вставляемых значений

def test_save_vacancies(mock_db_connection):
    conn = mock_db_connection.return_value
    data_employers = [
        {"id": 1},
        {"id": 2},
    ]

    with patch('src.api.get_vacancies') as mock_get_vacancies:
        mock_get_vacancies.return_value = [
            {
                "id": 101,
                "employer": {"name": "Company A", "id": 1},
                "name": "Developer",
                "url": "http://developer.com",
                "salary": {"from": 50000, "to": 70000, "currency": "RUB"},
                "area": {"name": "Remote"},
                "snippet": {"responsibility": "Develop software"},
            }
        ]

        save_vacancies(conn, data_employers)

        conn.cursor.assert_called_once()
        cursor = conn.cursor.return_value.__enter__.return_value
        cursor.execute.assert_called()  # Также можно добавить дополнительные проверки

def test_fill_tables(mock_db_connection):
    conn = mock_db_connection.return_value

    with patch('src.api.get_employer_id') as mock_get_employer_id:
        mock_get_employer_id.return_value = [
            {"id": 1, "name": "Company A", "url": "http://companya.com", "open_vacancies": 10},
            {"id": 2, "name": "Company B", "url": "http://companyb.com", "open_vacancies": 5},
        ]

        fill_tables()
        conn.cursor.assert_called()