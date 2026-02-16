from unittest.mock import Mock, patch

from src.api import get_employer_id, get_vacancies


def test_get_employer_id_failure(mock_requests_get):
    with patch("requests.get", return_value=Mock(status_code=404)):
        result = get_employer_id(["Компании нет"])
        assert result is None


@patch("requests.get")
def test_get_vacancies_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [{"id": "1", "name": "Вакансия A"}, {"id": "2", "name": "Вакансия B"}]
    }
    mock_get.return_value = mock_response
    result = get_vacancies("12345")
    assert len(result) == 2
    assert all(isinstance(item, dict) for item in result)


@patch("requests.get")
def test_get_vacancies_failure(mock_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    result = get_vacancies("12345")
    assert result == []
