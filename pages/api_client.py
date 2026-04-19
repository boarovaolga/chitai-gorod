import requests
import allure
from conf import API_base_url


@allure.description("Клиент для работы с поисковым API Читай-город (v2)")
class ChitaiGorodAPI:
    def __init__(self, token: str = None):
        self.base_url = API_base_url
        self.token = token
        self.session = requests.Session()
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    @allure.step("Поиск товаров по фразе '{phrase}'")
    def search_products(self, phrase: str = None,
                        page: int = 1, per_page: int = 2, city_id: int = 2):
        url = f"{self.base_url}/product"
        params = {
            "customerCityId": city_id,
            "products[page]": page,
            "products[per-page]": per_page,
            "abTestGroup": 1
        }
        if phrase is not None:
            params["phrase"] = phrase
        response = self.session.get(url, params=params)
        return response

    @allure.step("Получение подсказок поиска для фразы '{phrase}'")
    def search_suggests(self, phrase: str, page: int = 1, per_page: int = 5):
        url = f"{self.base_url}/search-phrase-suggests"
        params = {
            "suggests[page]": page,
            "suggests[per-page]": per_page,
            "phrase": phrase,
            "abTestProductsLimitGroup": 1,
            "include": "authors,bookCycles,"
                       "categories,publishers,publisherSeries,products"
        }
        response = self.session.get(url, params=params)
        return response
