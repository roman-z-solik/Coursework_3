import psycopg2

class DBManager:
    def __init__(self, db_config):
        self.connection = psycopg2.connect(**db_config)
        self.cursor = self.connection.cursor()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой"""
        self.cursor.execute(''' SELECT c.name, COUNT(v.id) as vacancies_count FROM companies c LEFT JOIN vacancies v ON c.id = v.company_id GROUP BY c.name ''')
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, вакансии, зарплаты и ссылки на вакансию"""
        self.cursor.execute(''' SELECT c.name, v.name, v.salary_from, v.salary_to, v.currency, v.alternate_url FROM vacancies v JOIN companies c ON v.company_id = c.id ''')
        return self.cursor.fetchall()

    def get_avg_salary(self):
        """Средняя заработная плата среди всех вакансий"""
        self.cursor.execute(''' SELECT AVG((salary_from + salary_to) / 2) FROM vacancies WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL ''')
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_vacancies_with_higher_salary(self):
        """Список вакансий с заработной платой выше средней"""
        average_salary = self.get_avg_salary()
        if average_salary is None:
            return []
        self.cursor.execute(''' SELECT c.name, v.name, v.salary_from, v.salary_to, v.currency, v.alternate_url FROM vacancies v JOIN companies c ON v.company_id = c.id WHERE (v.salary_from + v.salary_to) / 2 >= %s ''', (average_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Получает список вакансий, название которых содержит указанное ключевое слово"""
        self.cursor.execute(''' SELECT c.name, v.name, v.salary_from, v.salary_to, v.currency, v.alternate_url FROM vacancies v JOIN companies c ON v.company_id = c.id WHERE v.name ILIKE %s ''', ('%' + keyword + '%',))
        return self.cursor.fetchall()

    def close(self):
        """Закрывает соединение с базой данных"""
        self.cursor.close()
        self.connection.close()