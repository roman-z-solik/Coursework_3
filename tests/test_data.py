from unittest.mock import patch

from src.data import (  # Убедитесь, что импортируете функции корректно
    create_tables,
    fill_tables,
    save_employers,
    save_vacancies,
)


def test_create_tables(mock_db_connection):
    conn = mock_db_connection.return_value
    create_tables(conn)
    conn.cursor.assert_called_once()


def test_save_employers(mock_db_connection):
    conn = mock_db_connection.return_value
    data_employers = [
        {
            "id": 1,
            "name": "Company A",
            "url": "http://companya.com",
            "open_vacancies": 10,
        },
        {
            "id": 2,
            "name": "Company B",
            "url": "http://companyb.com",
            "open_vacancies": 5,
        },
    ]

    save_employers(conn, data_employers)

    conn.cursor.assert_called_once()


def test_save_vacancies(mock_db_connection):
    conn = mock_db_connection.return_value
    data_employers = [
        {"id": 1},
        {"id": 2},
    ]

    with patch("src.api.get_vacancies") as mock_get_vacancies:
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


def test_fill_tables(mock_db_connection):
    conn = mock_db_connection.return_value

    with patch("src.api.get_employer_id") as mock_get_employer_id:
        mock_get_employer_id.return_value = [
            {
                "id": 1,
                "name": "Company A",
                "url": "http://companya.com",
                "open_vacancies": 10,
            },
            {
                "id": 2,
                "name": "Company B",
                "url": "http://companyb.com",
                "open_vacancies": 5,
            },
        ]

        fill_tables()
        conn.cursor.assert_called()
