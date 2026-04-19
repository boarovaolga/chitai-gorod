from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
import allure


@allure.description("Поиск по автору")
class SearchByAuthorUI:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    @allure.step("Поиск книги по автору '{author_name}'")
    def search_by_author(self, author_name: str) -> None:
        with allure.step(f"Ввести в поиск '{author_name}' и отправить запрос"):
            try:
                search_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "phrase"))
                )
                search_input.clear()
                search_input.send_keys(author_name)
                search_input.submit()
            except Exception as e:
                allure.attach(str(e), name="error",
                              attachment_type=allure.attachment_type.TEXT)
                raise AssertionError(f"Не удалось ввести фразу: {e}")

        with allure.step("Дождаться появления карточек товаров"):
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((
                        By.CSS_SELECTOR, ".product-card"))
                )
            except Exception as e:
                allure.attach(str(e), name="error",
                              attachment_type=allure.attachment_type.TEXT)
                raise AssertionError(
                    f"Не удалось дождаться результатов поиска: {e}")
