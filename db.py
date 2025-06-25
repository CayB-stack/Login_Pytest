import datetime
import pyodbc

DB_CONFIG = {
    'DRIVER': '{ODBC Driver 17 for SQL Server}',
    'SERVER': 'localhost',
    'DATABASE': 'CayTestRequests',
    'UID': 'sa',
    'PWD': 'Cheese89!@'
}

def get_db_connection():
    connection_string = ';'.join(f'{key}={value}' for key, value in DB_CONFIG.items())
    return pyodbc.connect(connection_string)

def insert_test_log(test_name, result):
    result_str = "PASS" if result else "FAIL"
    timestamp = datetime.datetime.now()
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO SeleniumTestLogs (TestName, Result, Timestamp) VALUES (?, ?, ?)",
            test_name, result_str, timestamp
        )
        conn.commit()
    print("Data inserted successfully.")

def return_test_logs():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SeleniumTestLogs")
        return cursor.fetchall()

if __name__ == "__main__":
    pass
    #insert_test_log("DemoTest", True)
    #insert_test_log("DemoTest", False)
    #
    #logs = return_test_logs()
    #for log in logs:
    #    print(log)
