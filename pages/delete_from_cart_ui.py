from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import allure


@allure.description("Удаление товара из корзины")
class DeleteFromCartUI:
    def __init__(self, driver):
        self.driver = driver

    @allure.step("Удалить книгу '{book_title}' из корзины")
    def delete_from_cart(self, book_title: str) -> None:
        with allure.step("Нажать на иконку корзины в хедере"):
            cart_icon = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid-button-header='cart']"))
            )
            cart_icon.click()

        with allure.step("Дождаться загрузки страницы корзины"):
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-title, h1, .cart-page, .basket-page, .cart__title"))
            )

        with allure.step("Нажать на кнопку удаления товара"):
            delete_button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid-button-cart='removeProduct']"))
            )
            delete_button.click()
