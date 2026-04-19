from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import allure


@allure.description("Поиск книг на латинице")
class SearchByLatinaUi:
    def __init__(self, driver):
        self.driver = driver

    @allure.step("Поиск книги на латинице '{book_title}'")
    def search_by_latina(self, book_title: str) -> None:
        with allure.step(f"Ввести в поиск '{book_title}' и отправить запрос"):
            try:
                search_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "phrase"))
                )
                search_input.clear()
                search_input.send_keys(book_title)
                search_input.submit()
            except Exception as e:
                allure.attach(str(e), name="Ошибка поиска по латинице", attachment_type=allure.attachment_type.TEXT)
                raise AssertionError(f"Не удалось выполнить поиск по латинице: {e}")

        with allure.step("Дождаться появления карточек товаров"):
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".product-card"))
                )
            except Exception as e:
                allure.attach(str(e), name="Ошибка ожидания карточек", attachment_type=allure.attachment_type.TEXT)
                raise AssertionError(f"Не удалось дождаться результатов поиска: {e}")
