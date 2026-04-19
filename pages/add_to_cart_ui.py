
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        TimeoutException)
from selenium.webdriver.remote.webdriver import WebDriver
import allure


@allure.description("Добавление товара в корзину")
class AddToCartUI:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def add_to_cart(self, book_title: str) -> None:
        with allure.step(f"Ввести в поиск '{book_title}' и выполнить поиск"):
            search_input = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.NAME, "phrase"))
            )
            search_input.clear()
            search_input.send_keys(book_title)
            search_input.submit()

            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, ".product-card"))
            )

        with allure.step("Закрыть всплывающее уведомление, если оно есть"):
            try:
                close_btn = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((
                        By.CSS_SELECTOR, ".agreement-notice_button"))
                )
                close_btn.click()

                WebDriverWait(self.driver, 5).until(
                    EC.invisibility_of_element_located((
                        By.CSS_SELECTOR, ".agreement-notice"))
                )
            except TimeoutException:
                pass

        with allure.step("Снять фокус с поля ввода для скрытия подсказок"):
            try:
                self.driver.find_element(By.TAG_NAME, "body").click()

                WebDriverWait(self.driver, 3).until(
                    EC.invisibility_of_element_located((
                            By.CSS_SELECTOR, ".suggests-list"))
                )
            except Exception:
                pass

        with allure.step("Нажать кнопку 'В корзину' для найденного товара"):
            add_button = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, "[data-testid-button-mini-product-card="
                                     "'canBuy']"))
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView("
                "{block: 'center', behavior: 'instant'});",
                add_button)
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid-button-mini-product-card='canBuy']"))
            )

            try:
                add_button.click()
            except ElementClickInterceptedException:
                allure.attach("Обычный клик перехвачен, используем "
                              "JavaScript клик", name="click_info",
                              attachment_type=allure.attachment_type.TEXT)
                self.driver.execute_script("arguments[0].click();", add_button)

        with allure.step("Дождаться появления счётчика корзины"):
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    '[data-testid-indicator-header="cartCounter"]'))
            )
