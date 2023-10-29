# Project to learn using postgresql and python


Guided by ChatGPT --> list of things to learn to get familiar with this

## Get porsgres running
1. create a new DB in postgres called "company_db"
2. install pgAdmin4 to get familiar with a gui for postgres
3. create a table in psql 

## write pyhton script to manipulate the DB

1. install psycopg2 and SQLAlchemy
2. connect with the database
3. Fetch entries
4. Add, delete, change entries

## write a RESTful API with Flask

1. install flask and flask_restful
2. setup a flask server (application) with enpoints for employees and and employee
selected by id
3. test this by going to http://127.0.0.1:5000/employees 
or http://127.0.0.1:5000/employees/2 to test the id

--> learned: pay attention to the data types so that data can be converted to json
(I had the problem that the query gave for the date a datetime.date type which leads to an error when converting the datastructure to json)

To Do:
- refactor the methods and functions so that there is not that much repition. 
- write more query functions
- Can I manipulate the data over the webpage? --> How?