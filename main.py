import psycopg2
import os
from flask import Flask
from flask_restful import Resource, Api, reqparse



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

def fetch_employee_details(connection, employee_id):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM employees WHERE id={employee_id}")
        employee = cursor.fetchall() 
        return employee
    except Exception as e:
        print(f"Error fetching employee: {e}")
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

## conversion, so json file can be generated, issues with the "date" data type

def convert_date_to_string(data):
    new_data = []
    for empl in data:
        # convert the date type to a string
        new_empl = (empl[0],empl[1],empl[2],empl[3],empl[4].strftime('%Y-%m-%d'),empl[5])
        new_data.append(new_empl)
    return new_data

#############
### FLASK ###
#############

app = Flask(__name__)
api = Api(app)

class EmployeeList(Resource):
    def get(self):
        connection = connect_to_database()
        employees = fetch_employees(connection)
        employees = convert_date_to_string(employees)
        return employees
    
class Employee(Resource):
    def get(self, employee_id):
        connection = connect_to_database()
        employeeDetails = fetch_employee_details(connection, employee_id)
        employeeDetails = convert_date_to_string(employeeDetails)
        return employeeDetails
    
api.add_resource(EmployeeList, '/employees')
api.add_resource(Employee, '/employees/<int:employee_id>')


def main():
    connection = connect_to_database()
    if connection:
        print("inserting")
        insert_employees(connection)
        employees = fetch_employees(connection)
        employees = convert_date_to_string(employees)
        for emp in employees:
            print(emp)
        print("deleting")
        delete_employees(connection)
        employees = fetch_employees(connection)
        employees = convert_date_to_string(employees)
        for emp in employees:
            print(emp)
        connection.close()

if __name__ == "__main__":
    #main()
    app.run(debug=True)
