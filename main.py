import os

from dotenv import load_dotenv
from src.dbm import DBManager
from src.config import DB_NAME, HOST, PORT, companies
from src.api import get_employer_id, get_vacancies

load_dotenv()
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")


def main():
    manager = DBManager({
        'dbname': DB_NAME,
        'host': HOST,
        'port': PORT,
        'user': USER,
        'password': PASSWORD
    })

    while True:
        print("\nМеню:")
        print("1. Список компаний и количество вакансий")
        print("2. Все вакансии")
        print("3. Средняя зарплата")
        print("4. Вакансии с зарплатой выше средней")
        print("5. Поиск вакансий по названию")
        print("6. Выход")

        choice = input("Ваш выбор: ")

        if choice == '1':
            manager.get_companies_and_vacancies_count()
        elif choice == '2':
            manager.get_all_vacancies()
        elif choice == '3':
            manager.get_avg_salary()
        elif choice == '4':
            manager.get_vacancies_with_higher_salary()
        elif choice == '5':
            keyword = input("Введите слово для поиска: ")
            manager.get_vacancies_with_keyword(keyword)
        elif choice == '6':
            break
        else:
            print("\nНекорректный ввод!\nВведите пункт меню заново!")


if __name__ == '__main__':
    main()