# Cross-Browser test with Chrome - 3 tests for different window sizes
from selenium.webdriver.chrome.options import Options
import unittest
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def search_weather(driver, width=None, height=None, label="Chrome"):
    """
    Shared helper: open Google, search for Weather San Jose,
    wait for title to load (fixes timing issues), click weather widget buttons.
    """
    if width and height:
        driver.set_window_size(width, height)

    driver.get("http://www.google.com")
    wait = WebDriverWait(driver, 10)  # FIX: was 2 seconds — too short, raised TimeoutException

    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@name='q']")))
    time.sleep(1)

    search = driver.find_element(By.NAME, "q")
    search.clear()
    search.send_keys("Weather San Jose")
    search.submit()

    # FIX: wait for title to contain expected text instead of sleeping 1 second
    # On slow machines time.sleep(1) is not enough and title assertion fails
    wait.until(EC.title_contains("Weather San Jose"))

    assert "No results found." not in driver.page_source, f"No results found in {label}"
    assert "Weather San Jose - Google Search" in driver.title, \
        f"Unexpected title in {label}: {driver.title}"

    size = f"{width}x{height}" if width else "maximized"
    print(f"Page title in {label} ({size}): {driver.title}")

    # Weather widget interactions
    wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="wob_wc"]')))

    wait.until(EC.visibility_of_element_located((By.ID, "wob_rain")))
    print("Precipitation button is visible")
    wait.until(EC.element_to_be_clickable((By.ID, "wob_rain")))
    print("Precipitation button is clickable")
    driver.find_element(By.ID, "wob_rain").click()
    time.sleep(1)

    wait.until(EC.visibility_of_element_located((By.ID, "wob_wind")))
    print("Wind button is visible")
    wait.until(EC.element_to_be_clickable((By.ID, "wob_wind")))
    print("Wind button is clickable")
    driver.find_element(By.ID, "wob_wind").click()
    time.sleep(1.5)

    wait.until(EC.visibility_of_element_located((By.ID, "wob_temp")))
    print("Temperature button is visible")
    wait.until(EC.element_to_be_clickable((By.ID, "wob_temp")))
    print("Temperature button is clickable")
    driver.find_element(By.ID, "wob_temp").click()


class ChromeSearch(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()

    def test_search_weather_chrome(self):
        """Full screen - maximized window"""
        search_weather(self.driver, label="Chrome")

    def test_search_weather_chrome_1120x850(self):
        """Window size 1120x850"""
        search_weather(self.driver, 1120, 850, "Chrome")

    def test_search_weather_chrome_1120x950(self):
        """Window size 1120x950"""
        search_weather(self.driver, 1120, 950, "Chrome")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
