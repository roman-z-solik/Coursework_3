import psycopg2
import os
from config import *
from dotenv import load_dotenv

from src.api import get_employer_id, get_vacancies


load_dotenv()
USER = os.getenv('USER')
PASSWORD = os.getenv("PASSWORD")


try:
    conn = psycopg2.connect(
        dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT
    )
except Exception as err:
    print("Ошибка подключения:", err)
else:
    cur = conn.cursor()

    # Выполняем команду создания таблиц
    create_tables_sql = """ 
    DROP TABLE IF EXISTS employers CASCADE;
    DROP TABLE IF EXISTS vacancies CASCADE;
    CREATE TABLE IF NOT EXISTS employers ( 
    employer_id SERIAL PRIMARY KEY, 
    company_name VARCHAR(255) NOT NULL, 
    website_url TEXT, open_vacancies INT 
    );
    CREATE TABLE IF NOT EXISTS vacancies ( 
    vacancy_id SERIAL PRIMARY KEY,
    id_on_site INT, 
    title VARCHAR(255) NOT NULL, 
    url TEXT,
    salary_from INTEGER, salary_to INTEGER, 
    currency CHAR(3) DEFAULT 'RUB', 
    location VARCHAR(255), description TEXT, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    employer_id INT REFERENCES employers(employer_id) ON DELETE CASCADE ); """

    cur.execute(create_tables_sql)
    conn.commit()

    data_employers = get_employer_id(companies)


    insert_employer_sql = """ INSERT INTO employers(
    employer_id, company_name, website_url, open_vacancies) VALUES 
    (%s, %s, %s, %s); """
    for i in range(0,len(data_employers)):
        new_employer = (
            data_employers[i]['id'],
            data_employers[i]['name'],
            data_employers[i]['url'],
            data_employers[i]['open_vacancies'],
        )
        cur.execute(insert_employer_sql, new_employer)


    conn.commit()

    insert_vacancy_sql = """ INSERT INTO vacancies(
    id_on_site, title, url, salary_from, salary_to, currency, location, description, employer_id) VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s); """
    for n in range(0, len(data_employers)):
        vacancies = get_vacancies(1373)
        for i in range(0, len(vacancies)):
            new_vacancy = (
            vacancies[i]['id'],
            vacancies[i]['name'],
            vacancies[i]['url'],
            # 0 if vacancies[i]['salary']['from'] is None else vacancies[i]['salary']['from'],
            # 0 if vacancies[i]['salary']['to'] is None else vacancies[i]['salary']['to'],
            0,
            0,
            'RUR' if vacancies[i]['salary']['currency'] is None else vacancies[i]['salary']['currency'],
            # vacancies[i]['salary']['currency'],
            # vacancies[i]['address']['city'],
            'Москва',
            vacancies[i]['snippet']['responsibility'],
            vacancies[i]['employer']['id']
            )
            cur.execute(insert_vacancy_sql, new_vacancy)
        conn.commit()

    # Завершаем транзакцию и закрываем соединение
    cur.close()
    conn.close()


if __name__ == "__main__":
    pass