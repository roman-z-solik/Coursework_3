import requests

from src.config import companies


def get_employer_id(companies):
    """Функция для получения ID работодателя"""
    url = "https://api.hh.ru/employers"
    employers_table = []
    for company_name in companies:
        params = {"text": company_name}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data and data.get("items"):
                for employer in data["items"]:
                    if employer["name"].lower() == company_name.lower():
                        employers_table.append(employer)
                        break
        else:
            print(f"Ошибка при запросе: {response.status_code}")
            return None
    return employers_table


def get_vacancies(employer_id):
    """Функция для получения вакансий по ID работодателя"""
    url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['items']
    return []


if __name__ == "__main__":
    result = get_employer_id(companies)
    for res in result:
        print(res)
    # result = get_vacancy(1373)
    # # for res in result:
    # #     print(res)
    # print(result)
    # employer_id = companies
    vacancies = get_vacancies(3529)
    print(len(vacancies))
    for i in vacancies:
        print(i)
