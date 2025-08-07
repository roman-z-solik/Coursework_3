import os

import psycopg2
from dotenv import load_dotenv

from config import DB_NAME, HOST, PORT, companies
from src.api import get_employer_id, get_vacancies

load_dotenv()
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")


try:
    conn = psycopg2.connect(
        dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT
    )
except Exception as err:
    print("Ошибка подключения:", err)
else:
    cur = conn.cursor()


def fill_tables():
    create_tables_sql = """
    DROP TABLE IF EXISTS employers CASCADE;
    DROP TABLE IF EXISTS vacancies CASCADE;
    CREATE TABLE IF NOT EXISTS employers (
    employer_id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    website_url TEXT, open_vacancies INT
    );
    CREATE TABLE IF NOT EXISTS vacancies (
    vacancies_id INT PRIMARY KEY,
    employer_name VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    url TEXT,
    salary_from FLOAT, salary_to FLOAT,
    currency CHAR(3), location VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    employer_id INT REFERENCES employers(employer_id) ON DELETE CASCADE );
    """

    cur.execute(create_tables_sql)
    conn.commit()

    data_employers = get_employer_id(companies)

    insert_employer_sql = """
    INSERT INTO employers(
    employer_id, company_name, website_url, open_vacancies) VALUES
    (%s, %s, %s, %s);
    """
    for i in range(0, len(data_employers)):
        new_employer = (
            data_employers[i]["id"],
            data_employers[i]["name"],
            data_employers[i]["url"],
            data_employers[i]["open_vacancies"],
        )
        cur.execute(insert_employer_sql, new_employer)

    conn.commit()

    insert_vacancy_sql = """
    INSERT INTO vacancies(
    vacancies_id, employer_name, title, url, salary_from, salary_to, currency,
    location, description, employer_id) VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    for employer in data_employers:
        vacancies = get_vacancies(int(employer["id"]))
        for vacancy in vacancies:
            salary_from = 0.0
            salary_to = 0.0
            currency = "RUB"
            city = ""
            try:
                if vacancy["salary"]:
                    salary_from = vacancy["salary"]["from"]
                    salary_to = vacancy["salary"]["to"]
                    currency = vacancy["salary"]["currency"]
            except TypeError:
                continue
            new_vacancy = (
                vacancy["id"],
                employer["name"],
                vacancy["name"],
                vacancy["url"],
                salary_from,
                salary_to,
                currency,
                vacancy["area"]["name"],
                vacancy["snippet"]["responsibility"],
                employer["id"],
            )
            cur.execute(insert_vacancy_sql, new_vacancy)
    conn.commit()

    cur.close()
    conn.close()


if __name__ == '__main__':
    if fill_tables():
        print('Все прошло успешно')
