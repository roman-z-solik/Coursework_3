import requests

# Список компаний
companies = [
    "Яндекс",
    "Сбер",
    "МТС",
    "T2",
    "VK",
    "Газпром нефть",
    "Ростелеком",
    "Альфа-Банк",
    "Лаборатория Касперского",
    "Аэрофлот",
]


def get_employer_id(companies):
    "Функция для получения ID работодателя"
    url = "https://api.hh.ru/employers"
    id_table = []
    for company_name in companies:
        params = {"text": company_name}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            ext_company = company_name
            data = response.json()
            if data and data.get("items"):
                for employer in data["items"]:
                    if employer["name"].lower() == ext_company.lower():
                        id_table.append(employer["id"])
                        break
        else:
            print(f"Ошибка при запросе: {response.status_code}")
            return None
    return id_table


# функция получения вакансий по работодателям
def get_vacancy(employer_id):
    """Функция ищет вакансии по ID работодателя.
    Список вакансий"""
    vacancies = {}
    url = "https://api.hh.ru/vacancies"
    params = {"employer_id": employer_id}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Ошибка при выполнении запроса: {response.text}")
    else:
        for emp_id in employer_id:
            vacancies["employer"] = emp_id
            vacancies["vacancy"] = response.json()
    return vacancies


# if __name__ == "__main__":
#     id_employer_table = get_employer_id(companies)
# print(id_employer_table)
# vacancy = get_vacancy('80')
# print(vacancy)
# for i in range (0, len(vacancy)):
#     print(f'emp_id: {vacancy['items'][i]['employer']['name']}
#     id: {vacancy['items'][i]['id']} name: {vacancy['items'][i]['name']}')
# vac = get_vacancy(get_employer_id(companies))
# print(vac)
