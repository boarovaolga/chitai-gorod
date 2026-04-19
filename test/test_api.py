import pytest
import allure
from pages.api_client import ChitaiGorodAPI
from conf import Token, Invalid_token


@allure.feature("API Search")
class TestApiSearch:

    @allure.title("Пустой поиск (негативный)")
    @allure.description("Проверка, что при отсутствии"
                        " phrase возвращается 400 Bad Request.")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_empty_search(self):
        api = ChitaiGorodAPI(Token)
        response = api.search_products()

        with allure.step("Статус-код 400"):
            assert response.status_code == 400, (
                f"Ожидался 400, получен {response.status_code}")

    @allure.title("Спецсимволы в поиске (негативный)")
    @allure.description("Поиск по #^ должен вернуть"
                        " 422 Unprocessable Content.")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_search_with_special_characters(self):
        api = ChitaiGorodAPI(Token)
        response = api.search_products(phrase="#^")

        with allure.step("Статус-код 422"):
            assert response.status_code == 422, (
                f"Ожидался 422, получен {response.status_code}")

    @allure.title("Неактуальный токен (негативный)")
    @allure.description("Запрос с просроченным токеном"
                        " должен вернуть 401 Unauthorized.")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    def test_search_with_expired_token(self):
        api = ChitaiGorodAPI(Invalid_token)
        response = api.search_products(phrase="детектив")

        with allure.step("Статус-код 401"):
            assert response.status_code == 401, (
                f"Ожидался 401, получен {response.status_code}")

    @allure.title("Поиск по автору (позитивный)")
    @allure.description("Поиск книги по автору происходит корректно")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    def test_search_by_author(self):
        api = ChitaiGorodAPI(Token)
        response = api.search_products(phrase="самойлова елена", per_page=5)

        with allure.step("Статус-код 200"):
            assert response.status_code == 200, (
                f"Ожидался 200, получен {response.status_code}")

        data = response.json()
        with allure.step("В ответе есть товары"):
            products = data.get("data", {}).get(
                "relationships", {}).get("products", {}).get("data", [])
            assert len(products) > 0, "Список товаров пуст"

    @allure.title("Поиск по жанру (позитивный)")
    @allure.description("Поиск по жанру 'детектив' происходит корректно")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    def test_search_by_genre(self):
        api = ChitaiGorodAPI(Token)
        response = api.search_products(phrase="детектив", per_page=5)

        with allure.step("Статус-код 200"):
            assert response.status_code == 200, (
                f"Ожидался 200, получен {response.status_code}")

        data = response.json()
        with allure.step("В ответе есть товары"):
            products = data.get("data", {}).get(
                "relationships", {}).get("products", {}).get("data", [])
            assert len(products) > 0, "Список товаров пуст"
