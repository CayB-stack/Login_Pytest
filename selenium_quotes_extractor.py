from selenium import webdriver
from selenium.webdriver.common.by import By
import pyodbc

# SQL Server DB connection setup
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost,1433;'
    'DATABASE=CayTestRequests;'
    'UID=sa;'
    'PWD=Cheese89!@'
)
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Quotes' AND xtype='U')
CREATE TABLE Quotes (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    QuoteText NVARCHAR(MAX),
    Author NVARCHAR(255)
)
''')
conn.commit()

# Launch browser
driver = webdriver.Chrome()
driver.get("http://quotes.toscrape.com/login")

# Login
driver.find_element(By.NAME, "username").send_keys("admin")
driver.find_element(By.NAME, "password").send_keys("admin")
driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

# Scrape quotes and authors
quotes = driver.find_elements(By.CLASS_NAME, "quote")

for q in quotes:
    text = q.find_element(By.CLASS_NAME, "text").text.strip()
    author = q.find_element(By.CLASS_NAME, "author").text.strip()

    print(f"Quote: {text} | Author: {author}")

    # Insert into SQL
    cursor.execute(
        "INSERT INTO Quotes (QuoteText, Author) VALUES (?, ?)",
        text, author
    )
    conn.commit()

# Clean up
driver.quit()
cursor.close()
conn.close()
