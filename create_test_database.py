"""
Script to create the test database for running unit tests
"""
import mysql.connector

def create_test_database():
    """Create the test database if it doesn't exist"""
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='112233'
        )
        
        cursor = connection.cursor()
        
        # Create test database
        cursor.execute("CREATE DATABASE IF NOT EXISTS mechanic_shop_test")
        print("✓ Test database 'mechanic_shop_test' created successfully")
        
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    create_test_database()
