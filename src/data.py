import psycopg2

# Подключение к PostgreSQL
connection = psycopg2.connect(
    host='localhost',
    port='5432',
    database='hh_database',
    user='postgres',
    password='your_password_here'
)
cursor = connection.cursor()

# Добавление работодателей в таблицу companies
for item in data:
    employer = item['employer']
    cursor.execute(
        """ INSERT INTO companies (external_id, name, alternate_url, site_url, description) VALUES (%s, %s, %s, %s, %s) RETURNING id """,
        (employer['id'], employer['name'], employer['alternate_url'], employer['site'], employer['description'])
    )
    company_id = cursor.fetchone()[0]

    # Добавление вакансий работодателя в таблицу vacancies
    for vacancy in item['vacancies']:
        cursor.execute(
            """ INSERT INTO vacancies (external_id, company_id, name, salary_from, salary_to, currency, alternate_url, area) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """,
            (vacancy['id'], company_id, vacancy['name'],
             vacancy['salary']['from'] if vacancy['salary'] and vacancy['salary'].get('from') else None,
             vacancy['salary']['to'] if vacancy['salary'] and vacancy['salary'].get('to') else None,
             vacancy['salary']['currency'] if vacancy['salary'] else None,
             vacancy['alternate_url'], vacancy['area']['name'])
        )

# Закрываем подключение и коммитим изменения
connection.commit()
cursor.close()
connection.close()