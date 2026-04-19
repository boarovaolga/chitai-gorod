from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import allure


@allure.description("Поиск по названию")
class SearchByTitleUI:
    def __init__(self, driver):
        self.driver = driver

    @allure.step("Поиск книги по названию '{book_title}'")
    def search_by_title(self, book_title: str) -> None:
        with allure.step(f"Ввести в поиск '{book_title}'"):
            try:
                search_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "phrase"))
                )
                search_input.clear()
                search_input.send_keys(book_title)
            except Exception as e:
                allure.attach(str(e), name="error",
                              attachment_type=allure.attachment_type.TEXT)
                raise AssertionError(f"Не удалось ввести название: {e}")

        with allure.step("Нажать кнопку поиска"):
            try:
                search_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((
                        By.CSS_SELECTOR, "button[aria-label='Найти']"))
                )
                search_button.click()
            except Exception as e:
                allure.attach(str(e), name="error",
                              attachment_type=allure.attachment_type.TEXT)
                raise AssertionError(f"Не удалось нажать кнопку поиска: {e}")

        with allure.step("Дождаться появления карточек товаров"):
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((
                        By.CSS_SELECTOR, ".product-card"))
                )
            except Exception as e:
                allure.attach(str(e), name="error",
                              attachment_type=allure.attachment_type.TEXT)
                raise AssertionError(f"Результаты поиска не загрузились: {e}")
