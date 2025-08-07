import psycopg2


class DBManager:
    def __init__(self, db_connection_params):
        self.conn = psycopg2.connect(**db_connection_params)

    # Метод для подключения к БД
    def connect(self):
        if not hasattr(self, "conn"):
            raise Exception("Database connection is closed.")

    # Метод получения списка компаний и количества вакансий
    def get_companies_and_vacancies_count(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT c.company_name, COUNT(v.employer_id) AS vacancy_count FROM
                employers c LEFT JOIN vacancies v ON c.employer_id = v.employer_id
                GROUP BY c.employer_id"""
            )
            rows = cur.fetchall()
            for row in rows:
                print(row)

    # Метод получения всех вакансий с информацией о компании
    def get_all_vacancies(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT c.company_name, v.title, v.salary_from, v.salary_to, v.currency,
                 v.url FROM vacancies v INNER JOIN employers c ON v.employer_id = c.employer_id"""
            )
            rows = cur.fetchall()
            for row in rows:
                print(row)

    # Метод расчета средней зарплаты
    def get_avg_salary(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """ SELECT AVG((salary_from + salary_to)/2)::numeric(10,2) AS avg_salary
                FROM vacancies WHERE vacancies.salary_from != 0.0 AND vacancies.salary_to != 0.0"""
            )
            result = cur.fetchone()[0]
            print(f"\n{result} RUB")

    # Метод поиска вакансий с зарплатой выше средней
    def get_vacancies_with_higher_salary(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """ WITH average_salary AS ( SELECT AVG((salary_from + salary_to)/2)::numeric(10,2) AS avg_salary
                FROM vacancies WHERE vacancies.salary_from != 0.0 AND vacancies.salary_to != 0.0)
                SELECT * FROM vacancies WHERE ((salary_from + salary_to)/2 > (SELECT avg_salary FROM average_salary))
                """
            )
            rows = cur.fetchall()
            for row in rows:
                print(f"{row}")

    # Метод поиска вакансий по ключевым словам
    def get_vacancies_with_keyword(self, keyword):
        with self.conn.cursor() as cur:
            cur.execute(
                """ SELECT * FROM vacancies WHERE LOWER(title) LIKE %s """,
                ("%" + keyword.lower() + "%",),
            )
            rows = cur.fetchall()
            for row in rows:
                print(f"{row}")
