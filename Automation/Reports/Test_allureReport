import time
import allure
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(params=["chrome", "firefox"])

def driver(request):

    browser = request.param

    # - CHROME -
    if browser == "chrome":

        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument("--start-maximized")

        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        driver = webdriver.Chrome(options=chrome_options)

        # hide webdriver flag
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

    # -FIREFOX -
    else:

        firefox_options = webdriver.FirefoxOptions()

        driver = webdriver.Firefox(options=firefox_options)

        driver.maximize_window()

    # implicit wait
    driver.implicitly_wait(5)

    yield driver

    time.sleep(2)

    driver.quit()

@allure.feature("Cross Browser Search Testing")
class TestGoogleSearch:

    @allure.story("Search Weather San Jose")
    @allure.severity(allure.severity_level.CRITICAL)

    def test_google_weather_search(self, driver):

        with allure.step("Open Google homepage"):

            driver.get("https://www.google.com")

            time.sleep(2)

        with allure.step("Accept cookies if popup appears"):

            try:

                accept = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//button//*[contains(text(),'Accept')]"
                        )
                    )
                )

                accept.click()

                print("Cookies popup accepted")

            except:
                print("Cookies popup not displayed")

        with allure.step("Locate search input field"):

            search_box = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.NAME, "q"))
            )

            assert search_box.is_displayed()

        with allure.step("Enter search query"):

            search_box.clear()

            # slower typing helps avoid captcha
            query = "Weather San Jose"

            for letter in query:
                search_box.send_keys(letter)
                time.sleep(0.08)

            time.sleep(1)

            search_box.send_keys(Keys.ENTER)

        with allure.step("Wait for search results page"):

            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            time.sleep(3)

        with allure.step("Validate search URL"):

            current_url = driver.current_url

            print("\nCurrent URL:")
            print(current_url)

            assert "Weather" in current_url or "weather" in current_url

        with allure.step("Validate page title"):

            title = driver.title

            print("\nPage Title:")
            print(title)

            assert "Weather" in title or "Google" in title

        with allure.step("Take screenshot for Allure report"):

            screenshot = driver.get_screenshot_as_png()

            allure.attach(
                screenshot,
                name="Search_Result_Page",
                attachment_type=allure.attachment_type.PNG
            )

        with allure.step("Pause for browser observation"):

            time.sleep(5)
