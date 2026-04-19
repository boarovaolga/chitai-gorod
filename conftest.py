import pytest
import allure
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from conf import UI_url

@pytest.fixture
def driver(request):
    """Фикстура для запуска браузера, закрытия всплывающих окон и снятия скриншотов при падении."""
    _driver = webdriver.Chrome()
    _driver.maximize_window()
    _driver.get(UI_url)

    # Закрываем куки-баннер
    try:
        cookie_btn = WebDriverWait(_driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".cookie-banner__button, [data-testid='cookie-accept']"))
        )
        cookie_btn.click()
    except:
        pass

    # Закрываем соглашение (agreement-notice)
    try:
        agree_btn = WebDriverWait(_driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".agreement-notice_button"))
        )
        agree_btn.click()
    except:
        pass

    yield _driver
    _driver.quit()