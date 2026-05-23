import time
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Next 3 lines of code is disabled Captcha in Google website
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)

driver.get("https://www.google.com")
driver.maximize_window()
driver.minimize_window()
driver.maximize_window()


print("Test 1: Check Google page Title")
try:
    assert "Google" in driver.title
    print("Test result: Page title is OK, current Title is: ", driver.title)
except AssertionError:
    print("Test result: Page title is different:", driver.title)

print("-------------------------------------")
print("Test 2: Check Google page URL")
try:
    assert "https://www.google.com/" in driver.current_url
    print("Test result: Page URL is OK: ", driver.current_url)
except AssertionError:
    print("Test result: Page URL is different", driver.current_url)

print("-------------------------------------")
print("Test 3: Google image is displayed")
try:
    driver.find_element(By.XPATH, '//img[@alt="Google"]').is_displayed()
    print("Test result: Page has correct Google image")
except NoSuchElementException:
    print("Test result: No Such Google image Element on the page", driver.save_screenshot("googleNOT_OK.png"))

print("-------------------------------------")
print("Test 4: Google Search button is enabled")
try:
    driver.find_element(By.XPATH, "(//input[@name='btnK'])[2]").is_enabled()
    print("Test result: Google Search button is enabled")
except NoSuchElementException:
    print("Test result: Google Search button is Disabled", driver.save_screenshot("googleSearchButtonNOT_OK.png"))

print("-------------------------------------")
print("Test 5: I'm Feeling Lucky button is enabled")
try:
    driver.find_element(By.ID, "gbqfbb").is_enabled()
    print("Test result: Google I'm Feeling Lucky button is enabled")
except NoSuchElementException:
    print("Test result: Google I'm Feeling Lucky button is Disabled", driver.save_screenshot("google_IFL_ButtonNOT_OK"
                                                                                             ".png"))

print("-------------------------------------")
print("Test 6: NASA links is in results")
try:
    driver.find_element(By.ID, "APjFqb").click()
    driver.find_element(By.ID, "APjFqb").send_keys("NASA")
    driver.find_element(By.XPATH, "(//input[@name='btnK'])[1]").click()
    time.sleep(2)
    # find NASA link in results
    driver.find_element(By.XPATH, '//a[@href="https://www.nasa.gov/"]').is_displayed()
    print("Test result: NASA link is displayed")

except NoSuchElementException:
    print("Test result: NASA link is NOT in results")
    # NASA 'Careers' link is in result
try:
    driver.find_element(By.XPATH, "//a[contains(text(),'Careers')]").is_displayed()
    print("Test result: 'Careers' link is displayed")

except NoSuchElementException:
    print("Test result: 'Careers' link is NOT in results")
    # NASA 'Solar System Exploration' link is in result
try:
    driver.find_element(By.XPATH, "//a[contains(text(),'Solar System Exploration')]").is_displayed()
    print("Test result: 'Solar System Exploration' link is displayed")

except NoSuchElementException:
    print("Test result: 'Solar System Exploration' link is NOT in results")
     # 'NASA Live' link is in result
try:
    driver.find_element(By.XPATH, "//a[contains(text(),'NASA Live')]").is_displayed()
    print("Test result: 'NASA Live' link is displayed")

except NoSuchElementException:
    print("Test result: 'NASA Live' link is NOT in results", driver.save_screenshot("NASA_SearchResultBAD.png"))

print("-------------------------------------")
print("Test 7: NASA link is in results and functional")
try:
    driver.find_element(By.XPATH, '//a[@href="https://www.nasa.gov/"]').click()
    # Simulate 2 sec waiting time
    time.sleep(2)

    # Check if NASA logo is displayed
    driver.find_element(By.ID, "header-logo").is_displayed()
    print("NASA logo is displayed")

    driver.find_element(By.XPATH,"//title[contains(text(),'NASA')]").is_displayed()
    print("Title 'NASA'  is displayed")

    driver.find_element(By.XPATH,"(//span[contains(.,'NASA+')])[3]").is_displayed()
    print("'NASA + Live' Logo is displayed")

    # add elements from Documentation to script
    nasa_url = "https://www.nasa.gov/"
    nasa_title = "NASA"

    # Check if elements is in the webpage
    assert nasa_url in driver.current_url
    print("NASA URL is Correct: ", driver.current_url)
    assert nasa_title in driver.title
    print("NASA Title is Correct: ", driver.title)

except AssertionError:
    print("NASA URL is NOT Correct: ", driver.current_url)
    print("NASA Title is NOT Correct: ", driver.title)

print("-------------------------------------")
print("Test 8:'Featured News' links is in results")
    # 'Featured News' link is in result
try:
    driver.find_element(By.XPATH,"(//div[@class='grid-row flex-align-center margin-bottom-3'])[1]").is_displayed()
    print("'Featured News' link is displayed")

except NoSuchElementException:
    print("Test result: 'Featured News' link is NOT in results")
    # 'Featured News' link is in result
try:
    driver.find_element(By.XPATH, "//span[contains(@xpath,'1')]").is_displayed()
    print("'More NASA News' link is displayed")

except NoSuchElementException:
    print("Test result: 'More NASA News' link is NOT in results")

print("-------------------------------------")
print("Test 9:'Earth and Climate' links is in results")
    # 'Earth and Climate' link is in result
try:
    driver.find_element(By.XPATH,"//h2[contains(.,'Earth and Climate')]").is_displayed()
    print("'Earth and Climate' link is displayed")

except NoSuchElementException:
    print("Test result: 'Earth and Climate' link is NOT in results")
    # 'Discover More' link is in result
try:
    driver.find_element(By.XPATH,"//span[contains(.,'Discover More')]").is_displayed()
    print("'Discover More' link is displayed")

except NoSuchElementException:
    print("Test result: 'Discover More' link is NOT in results")


print("-------------------------------------")
print("All Tests is DONE")
driver.quit()
