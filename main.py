import psycopg2
import os

# connection parameters

DATABASE_NAME = "company_db"
DATABASE_USER = "postgres"
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE_HOST = "localhost"
DATABASE_PORT = "5432"

def connect_to_database():
    try:
        connection = psycopg2.connect(
            dbname=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            host=DATABASE_HOST,
            port=DATABASE_PORT
        )
        print(f"Successfully connected to the database: {DATABASE_NAME}")
        return connection
    except Exception as e:
        print(f"Error: {e}")
        return None

def fetch_employees(connection):
    try:
        cursor = connection.cursor() 
        cursor.execute("SELECT * FROM employees;") # normal sql command
        employees = cursor.fetchall() # fetch all rows from the last execution
        
        return employees
    except Exception as e:
        print(f"Error fetching employees: {e}")
        return []
    finally:
        cursor.close()  # frees resources taken up by the cursor

def insert_employees(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO employees (first_name, last_name, email, hire_date, department) VALUES
('John', 'Doe', 'john.doe@exampleFAKE.com', '2022-01-15', 'LalaLand'),
('Jane', 'Smith', 'jane.smith@exampleFAKE.com', '2021-03-20', 'LalaLand'),
('Alice', 'Johnson', 'alice.johnson@exampleFAKE.com', '2022-05-22', 'Sales'),
('Bob', 'Williams', 'bob.williams@exampleFAKE.com', '2020-07-18', 'Engineering'),
('Charlie', 'Brown', 'charlie.brown@exampleFAKE.com', '2019-10-05', 'Finance');
""")
    except Exception as e:
        print(f"Error inserting values in employees: {e}")
    finally:
        cursor.close()

def delete_employees(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM employees WHERE email ilike '%FAKE%';")
    except Exception as e:
        print(f"Error deleting values from employees: {e}")
    finally:
        cursor.close()

def main():
    connection = connect_to_database()
    if connection:
        print("inserting")
        insert_employees(connection)
        employees = fetch_employees(connection)
        for emp in employees:
            print(emp)
            #print(type(emp))
        print("deleting")
        delete_employees(connection)
        employees = fetch_employees(connection)
        for emp in employees:
            print(emp)
            #print(type(emp))
        connection.close()

if __name__ == "__main__":
    main()
