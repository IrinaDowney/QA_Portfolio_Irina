from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

try:
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    # - OPEN WEBSITE
    driver.get("https://www.saucedemo.com")
    print("Website opened")

    # -LOGIN 
    wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    wait.until(EC.url_contains("inventory"))
    print("Login successful")

    # - VERIFY PRODUCTS -
    products = wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
    )
    print(f"Products available: {len(products)}")

    assert len(products) > 0

    # - ADD MULTIPLE PRODUCTS -
    add_buttons = driver.find_elements(By.CSS_SELECTOR, "button.btn_inventory")

    for i in range(2):  # add first 2 products
        add_buttons[i].click()
        print(f"Added product {i+1}")

    # -VERIFY CART BADGE -
    cart_badge = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )

    print("Cart badge count:", cart_badge.text)
    assert int(cart_badge.text) == 2

    # - OPEN CART -
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    wait.until(EC.url_contains("cart"))
    print("Cart page opened")

    # - VERIFY CART ITEMS -
    cart_items = wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "cart_item"))
    )

    print(f"Cart items: {len(cart_items)}")
    assert len(cart_items) == 2

    # - REMOVE ONE ITEM -
    remove_buttons = driver.find_elements(By.XPATH, "//button[text()='Remove']")
    remove_buttons[0].click()

    print("One item removed")

    # - VERIFY UPDATED CART -
    updated_items = driver.find_elements(By.CLASS_NAME, "cart_item")
    print(f"Updated cart items: {len(updated_items)}")

    assert len(updated_items) == 1

    # - CHECKOUT FLOW -
    driver.wait.until(EC.url_contains("checkout-step-one"))
    print("Checkout page opened")

    # Fill checkout form
    driver.find_element(By.ID, "first-name").send_keys("John")
    driver.find_element(By.ID, "last-name").send_keys("Doe")
    driver.find_element(By.ID, "postal-code").send_keys("24060")

    driver.find_element(By.ID, "continue").click()

    wait.until(EC.url_contains("checkout-step-two"))
    print("Checkout step 2 opened")

    # Finish order
    driver.find_element(By.ID, "finish").click()

    wait.until(EC.url_contains("checkout-complete"))
    print("Order completed")

    # Verify success message
    success_msg = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
    )

    assert "THANK YOU" in success_msg.text.upper()

    print("ORDER SUCCESSFUL")

    driver.find_element(By.ID, "back-to-products").click()

    wait.until(EC.url_contains("inventory"))
    print("Back to products page")

    # - LOGOUT -
    driver.find_element(By.ID, "react-burger-menu-btn").click()

    logout_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
    )

    logout_btn.click()

    wait.until(EC.url_contains("saucedemo"))
    print("Logout successful")

    print("TEST COMPLETED SUCCESSFULLY")

finally:
    driver.quit()
    print("Browser closed")
