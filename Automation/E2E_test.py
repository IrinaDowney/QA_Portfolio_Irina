import pytest
import requests
import time
import random
from faker import Faker

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

fake = Faker()

URL = "https://ecommerce-playground.lambdatest.io/index.php?route=account/register"


def delay():
    time.sleep(random.uniform(1, 2))


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):

    if request.param == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    else:
        options = webdriver.FirefoxOptions()
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference("useAutomationExtension", False)
        options.set_preference("marionette.logging", True)
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

    driver.maximize_window()

    yield driver
    driver.quit()


def test_account_registration(driver):

    wait = WebDriverWait(driver, 20)

    driver.get(URL)
    time.sleep(1)  

    # - API CHECK -
    assert requests.get(URL).status_co--------------de == 200

    # - PAGE CHECK - 
    assert "Register Account" in driver.title

    # - FORM FILL -
    driver.find_element(By.ID, "input-firstname").send_keys(fake.first_name())
    driver.find_element(By.ID, "input-lastname").send_keys(fake.last_name())
    driver.find_element(By.ID, "input-email").send_keys(fake.email())
    driver.find_element(By.ID, "input-telephone").send_keys(fake.phone_number())

    password = fake.password()
    driver.find_element(By.ID, "input-password").send_keys(password)
    driver.find_element(By.ID, "input-confirm").send_keys(password)

    # -CHECKBOXES -
    driver.find_element(By.CSS_SELECTOR, "label[for='input-newsletter-yes']").click()
    driver.find_element(By.CSS_SELECTOR, "label[for='input-agree']").click()

    # - CLICK CONTINUE -
    continue_btn = driver.find_element(By.CSS_SELECTOR, "input.btn.btn-primary")
    driver.execute_script("arguments[0].scrollIntoView(true);", continue_btn)
    delay()
    driver.execute_script("arguments[0].click();", continue_btn)

    # - SUCCESS VALIDATION -
    success_msg = "Congratulations! Your new account has been successfully created!"

    wait.until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), 'Congratulations')]"))
    )

    assert success_msg in driver.page_source

    # - CONTINUE AFTER SUCCESS (STRONG LOCATOR) -
    continue_btn_2 = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(@class,'btn') and contains(text(),'Continue')]")
        )
    )

    driver.execute_script("arguments[0].scrollIntoView(true);", continue_btn_2)
    delay()
    driver.execute_script("arguments[0].click();", continue_btn_2)

    wait.until(EC.title_contains("My Accoun t"))
    assert "My Account" in driver.title

    edit_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Edit Account")))
    edit_link.click()

    wait.until(EC.title_contains("My Account Information"))
