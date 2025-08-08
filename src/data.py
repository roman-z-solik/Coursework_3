import os

import psycopg2
from dotenv import load_dotenv

from src.api import get_employer_id, get_vacancies
from src.config import DB_NAME, HOST, PORT, companies

load_dotenv()
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")


def connect_to_db():
    conn = psycopg2.connect(
        dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT
    )
    return conn


def create_tables(conn):
    cur = conn.cursor()
    create_tables_sql = """
    DROP TABLE IF EXISTS employers CASCADE;
    DROP TABLE IF EXISTS vacancies CASCADE;
    CREATE TABLE IF NOT EXISTS employers (
    employer_id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    website_url TEXT, open_vacancies INT);
    CREATE TABLE IF NOT EXISTS vacancies (
    vacancies_id INT PRIMARY KEY,
    employer_name VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL, url TEXT,
    salary_from FLOAT, salary_to FLOAT, currency CHAR(3),
    location VARCHAR(255), description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    employer_id INT REFERENCES employers(employer_id) ON DELETE CASCADE );
    """
    cur.execute(create_tables_sql)
    conn.commit()
    cur.close()


def save_employers(conn, data_employers):
    cur = conn.cursor()
    insert_employer_sql = """
    INSERT INTO employers (employer_id, company_name, website_url, open_vacancies)
    VALUES (%s, %s, %s, %s);
    """
    for employer in data_employers:
        cur.execute(
            insert_employer_sql,
            (
                employer["id"],
                employer["name"],
                employer["url"],
                employer["open_vacancies"],
            ),
        )
    conn.commit()
    cur.close()


def save_vacancies(conn, data_employers):
    cur = conn.cursor()
    insert_vacancy_sql = """
    INSERT INTO vacancies (
    vacancies_id, employer_name, title, url, salary_from,
    salary_to, currency, location, description, employer_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    for employer in data_employers:
        vacancies = get_vacancies(employer["id"])
        for vacancy in vacancies:
            salary_from = 0.0
            salary_to = 0.0
            currency = "RUB"
            try:
                if vacancy["salary"]:
                    salary_from = vacancy["salary"]["from"]
                    salary_to = vacancy["salary"]["to"]
                    currency = vacancy["salary"]["currency"]
            except TypeError:
                continue

            new_vacancy = (
                vacancy["id"],
                vacancy["employer"]["name"],
                vacancy["name"],
                vacancy["url"],
                salary_from,
                salary_to,
                currency,
                vacancy["area"]["name"],
                vacancy["snippet"]["responsibility"],
                vacancy["employer"]["id"],
            )
            cur.execute(insert_vacancy_sql, new_vacancy)
    conn.commit()
    cur.close()


def fill_tables():
    conn = connect_to_db()
    create_tables(conn)
    data_employers = get_employer_id(companies)
    save_employers(conn, data_employers)
    save_vacancies(conn, data_employers)
    conn.close()


if __name__ == "__main__":
    fill_tables()
