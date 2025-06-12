import pytest
import random
import string
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Automatically install ChromeDriver
chromedriver_autoinstaller.install()

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")  # Comment out this line to see the browser
    options.add_argument("--disable-gpu")
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def test_login_quotes_to_scrape(driver):
    driver.get("http://quotes.toscrape.com/login")  # Target login URL

    # Wait for username field to appear
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))

    # Fill in the username and password with random strings
    driver.find_element(By.ID, "username").send_keys(random_string())
    driver.find_element(By.ID, "password").send_keys(random_string())

    # use javascript to click btn btn-primary class
    driver.execute_script("document.getElementsByClassName('btn btn-primary')[0].click();")
    
    # Wait for page response (e.g. error message or redirect)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # sleep for
    import time
    time.sleep(10)  # Allow time for the page to load


    # Check if login failed (we expect failure with random credentials)
    assert "Quotes to Scrape" in driver.title or "Invalid" in driver.page_source


