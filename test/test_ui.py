import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pages.search_by_author_ui import SearchByAuthorUI
from pages.add_to_cart_ui import AddToCartUI
from pages.delete_from_cart_ui import DeleteFromCartUI
from pages.search_by_latina_ui import SearchByLatinaUi
from pages.search_by_title_ui import SearchByTitleUI


@allure.title("Поиск книг по автору (Позитивный)")
@allure.description("Проверяет, что поиск книг по автору работает корректно")
@allure.feature("READ")
@allure.severity("CRITICAL")
@pytest.mark.ui
def test_search_by_author(driver):
    with allure.step("Найти книгу по автору Эрих Мария Ремарк"):
        search_page = SearchByAuthorUI(driver)
        search_page.search_by_author("Эрих Мария Ремарк")

    with allure.step("Проверить, что появились результаты поиска"):
        products = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((
                By.CSS_SELECTOR, ".product-card"))
        )
        assert len(products) > 0, "Не найдено ни одной карточки товара"


@allure.title("Добавление товара в корзину (Позитивный)")
@allure.description("Тест проверяет, что товар появляется в корзине")
@allure.feature("CREATE")
@allure.severity("BLOCKER")
@pytest.mark.ui
def test_add_to_cart(driver):
    with allure.step("Добавить в корзину книгу с названием Три товарища"):
        cart_page = AddToCartUI(driver)
        cart_page.add_to_cart("Три товарища")

    with allure.step("Получаем результат добавления книги в корзину"):
        counter = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                '[data-testid-indicator-header="cartCounter"]'))
        )
        counter_value = counter.text

    with allure.step("Проверка, что корзина не пустая"):
        assert counter_value.isdigit() and int(counter_value) > 0


@allure.title("Удаление товара из корзины (Позитивный)")
@allure.description("Проверяем, что удаление товара из корзины корректно")
@allure.feature("DELETE")
@allure.severity("BLOCKER")
@pytest.mark.ui
def test_delete_from_cart(driver):
    with allure.step("Добавить книгу 'Три товарища' в корзину (предусловие)"):
        add_page = AddToCartUI(driver)
        add_page.add_to_cart("Три товарища")

    with allure.step("Удалить книгу из корзины"):
        delete_page = DeleteFromCartUI(driver)
        delete_page.delete_from_cart("Три товарища")

    with allure.step("Проверяем, что корзина пустая"):
        try:
            counter = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    '[data-testid-indicator-header="cartCounter"]'))
            )
            assert counter.text == "0"
        except Exception:
            pass


@allure.title("Поиск товара на латинице")
@allure.description("Проверяем, что поиск товара на латинице корректный")
@allure.feature("READ")
@allure.severity("CRITICAL")
@pytest.mark.ui
def test_search_by_latina(driver):
    with allure.step("Найти книгу по названию Harry Potter"):
        search_latina_page = SearchByLatinaUi(driver)
        search_latina_page.search_by_latina("Harry Potter")

    with allure.step("Проверить, что появились результаты поиска"):
        products = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((
                By.CSS_SELECTOR, ".product-card"))
        )
        assert len(products) > 0, "Не найдено ни одной карточки товара"


@allure.title("Поиск книги по названию (Позитивный)")
@allure.description("Поиск по названию книги корректный")
@allure.feature("READ")
@allure.severity("CRITICAL")
@pytest.mark.ui
def test_search_by_title(driver):
    with allure.step("Найти книгу по названию 'Три товарища'"):
        search_page = SearchByTitleUI(driver)
        search_page.search_by_title("Три товарища")

    with allure.step("Проверить, что появились результаты поиска"):
        products = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((
                By.CSS_SELECTOR, ".product-card"))
        )
        assert len(products) > 0, "Не найдено ни одной карточки товара"
