from src.dbm import DBManager


def main():
    manager = DBManager({
        'dbname': 'hh_database',
        'user': 'postgres',
        'password': '12345'
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
            print("Некорректный ввод!")