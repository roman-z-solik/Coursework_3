import requests

# Список ID выбранных вами компаний
interesting_employers = [
    '15478',  # Yandex
    '763',    # VK (бывший Mail.ru Group)
    '786',    # СберБанк
    '1276',   # Газпром нефть
    '403059', # Лаборатория Касперского
    '132130', # Тинькофф Банк
    '3529',   # МТС
    '3776',   # РЖД
    '2180',   # Ростелеком
    '15479'   # Ozon
]

# Функция для получения информации о работодателе
def get_employer_info(employer_id):
    url = f'https://api.hh.ru/employers/{employer_id}'
    response = requests.get(url)
    return response.json()

# Функция для получения вакансий работодателя
def get_vacancies(employer_id):
    url = f'https://api.hh.ru/vacancies?employer_id={employer_id}&page=0&per_page=100'
    response = requests.get(url)
    return response.json().get('items', [])

# Сохраняем информацию о работодателях и вакансиях
data = []
for employer_id in interesting_employers:
    employer_info = get_employer_info(employer_id)
    vacancies = get_vacancies(employer_id)
    data.append({
        'employer': employer_info,
        'vacancies': vacancies
    })