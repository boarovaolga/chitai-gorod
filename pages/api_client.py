import requests
import allure
from conf import API_base_url
from requests import Response


@allure.description("Клиент для работы с поисковым API Читай-город (v2)")
class ChitaiGorodAPI:
    def __init__(self, token: str | None = None) -> None:
        self.base_url = API_base_url
        self.token = token
        self.session = requests.Session()
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    @allure.step("Поиск товаров по фразе '{phrase}'")
    def search_products(self, phrase: str | None = None,
                        page: int = 1, per_page: int = 2, city_id: int = 2) -> Response:
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
