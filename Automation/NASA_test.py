import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# Next 3 lines of code is disabled Captcha in Google website
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)
driver.get("https://www.google.com")
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
    print("Test result: No Such Google image Element on the page", driver.save_screenshot("googleImageNOT_OK.png"))

print("-------------------------------------")
print("Test 4: Google Search button is enabled")
try:
    driver.find_element(By.XPATH, "//div[@class='FPdoLc lJ9FBc']//input[@name='btnK']").is_displayed()
    print("Test result: Page has correct Search button")
except NoSuchElementException:
    print("Test result: No Such Google Button Element on the page", driver.save_screenshot("google_Button_NOT_OK.png"))
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
    # NASA Live is in result
    driver.find_element(By.XPATH, "//a[contains(text(),'Live')]").is_displayed()
    # Next line of code is the same as previous, but different locator search method
    driver.find_element(By.PARTIAL_LINK_TEXT, "Live").is_displayed()
    print("Test result: 'NASA Live' link is displayed")
    # NASA Images link is displayed
    driver.find_element(By.XPATH, "//a[@href='https://www.nasa.gov/images/']").is_displayed()
    print("Test result: 'NASA Images' link is displayed")
    # NASA Careers is displayed
    driver.find_element(By.XPATH, '//a[@href="https://www.nasa.gov/careers/"]').is_displayed()
    print("Test result: 'NASA Careers' link is displayed")
    # NASA+ is displayed
    driver.find_element(By.PARTIAL_LINK_TEXT, 'NASA+').is_displayed()
    print("Test result: 'NASA+' link is displayed")
except NoSuchElementException:
    print("Test result: NASA link is NOT in results", driver.save_screenshot("NASA_SearchResultBAD.png"))

print("-------------------------------------")
print("Test 7: NASA link is in results and functional")
try:
    driver.find_element(By.XPATH, '//a[@href="https://www.nasa.gov/"]').click()
    # Simulate 2 sec waiting time
    time.sleep(2)

    # Check if NASA logo is displayed
    driver.find_element(By.ID, "header-logo").is_displayed()
    print("NASA logo is displayed")

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
print("Test 8: Explore link is in results")
try:
    driver.find_element(By.XPATH, "(//span[contains(.,'Explore')])[1]").is_displayed()
    print("Explore link is displayed")
except NoSuchElementException:
    print("NO Explore link is NOT displayed", driver.save_screenshot("NO Explore link.png"))

print("-------------------------------------")
print("Test 9: Localization Test")
nasa_text_doc = "National Aeronautics and Space Administration"
nasa_text_website = driver.find_element(By.XPATH,"//h3[@class='heading-22 line-height-md']").text
try:
    assert nasa_text_doc in nasa_text_website
    print("Text is OK: ", nasa_text_website)
except AssertionError:
    print("Text NOT OK", nasa_text_website)
    driver.save_screenshot("NO nasa_text_doc.png")

print("-------------------------------------")

print("Test 10: 2nd Localization Test Follow NASA")
follow_nasa_text_doc = "Follow NASA"
follow_nasa_text_website = driver.find_element(By.XPATH,"//h3[contains(.,'Follow NASA')]").text
try:
    assert follow_nasa_text_doc in follow_nasa_text_website
    print("Follow NASA Text is OK: ", follow_nasa_text_website)
except AssertionError:
    print("Follow NASA Text NOT OK", follow_nasa_text_website)
    driver.save_screenshot("NO Follow NASA text.png")

print("-------------------------------------")

print("All Tests are DONE")
driver.quit()
