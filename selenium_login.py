import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

from db import insert_test_log

chromedriver_autoinstaller.install()

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

def test_login_quotes_to_scrape(driver):
    driver.get("http://quotes.toscrape.com/login")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(5)

    result = "PASS" if "Quotes to Scrape" in driver.title or "Invalid" in driver.page_source else "FAIL"

    # DB logging
    test_name = "Login Test"
    
    insert_test_log(test_name, result)

def randomTestCases():
    import random 
    cases = [{"test_name": "Login Failed", "result": "PASS"},
                {"test_name": "Login Successful", "result": "FAIL"},
                {"test_name": "Page Load", "result": "PASS"},
                {"test_name": "Element Visibility", "result": "FAIL"},
                {"test_name": "Button Click", "result": "PASS"},
                {"test_name": "Form Submission", "result": "FAIL"}]

    newCases = []
    for i in range(10):
        resultSim = random.choice([True, False])
        if  resultSim:
            # pick a random result from the case
            randomCase = random.choice(cases)
            newCases.append({
                "test_name": randomCase["test_name"],
                "result": "PASS"
            })
            insert_test_log(randomCase["test_name"], "PASS")
        else:
            # pick a random result from the case
            randomCase = random.choice(cases)
            newCases.append({
                "test_name": randomCase["test_name"],
                "result": "FAIL"
            })            
            insert_test_log(randomCase["test_name"], "FAIL")
        import time
        time.sleep(2)
        print("Test Case: ", newCases[-1]["test_name"], "Result: ", newCases[-1]["result"])
            
if __name__ == "__main__":    
    # Run random test cases
    randomTestCases()
    
    