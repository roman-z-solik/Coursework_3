from dotenv import load_dotenv
import os

load_dotenv()
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

def test_get_companies_and_vacancies_count(db_manager):
    db_manager.conn.cursor.return_value.__enter__.return_value.fetchall.return_value = [
        ('Company A', 10),
        ('Company B', 5)
    ]

    db_manager.get_companies_and_vacancies_count()
    db_manager.conn.cursor.assert_called_once()


def test_get_all_vacancies(db_manager):
    db_manager.conn.cursor.return_value.__enter__.return_value.fetchall.return_value = [
        ('Company A', 'Vacancy A', 50000, 70000, 'RUB', 'http://example.com/vacancy-a')
    ]

    db_manager.get_all_vacancies()
    db_manager.conn.cursor.assert_called_once()


def test_get_avg_salary(db_manager):
    db_manager.conn.cursor.return_value.__enter__.return_value.fetchone.return_value = [60000.00]

    db_manager.get_avg_salary()
    db_manager.conn.cursor.assert_called_once()


def test_get_vacancies_with_higher_salary(db_manager):
    db_manager.conn.cursor.return_value.__enter__.return_value.fetchall.return_value = [
        ('Vacancy H1', 80000, 100000, 'RUB'),
        ('Vacancy H2', 75000, 90000, 'RUB')
    ]

    db_manager.get_vacancies_with_higher_salary()
    db_manager.conn.cursor.assert_called_once()


def test_get_vacancies_with_keyword(db_manager):
    keyword = 'python'
    db_manager.conn.cursor.return_value.__enter__.return_value.fetchall.return_value = [
        ('Vacancy 1', 'Senior Python Developer', 60000, 80000, 'RUB', 'url1'),
    ]

    db_manager.get_vacancies_with_keyword(keyword)
    db_manager.conn.cursor.assert_called_once_with()