To test backend with MySQL (windows)

1. download MySQLInstaller
2. open task manager and go to services tab
3. start MySQL80 if not already running
4. open MySQL workbench and set username and password, then create a database to store the tables from recordbin (CREATE DATABASE database_name_here)
5. run 'pip install mysql-connector-python' NOTE: I use mysqlconnector because the offical SQL Client was not working for me 
6. go to settings.py and navigate to database section, ensure the engine is set to 'mysql.connector.django' and edit username and password to match the credentials you created in MySQL Workbench
7. make sure the database name is one that has already been created in MySQL workbench
8. run command 'python manage.py makemigrations' and then 'python manage.py migrate' if running MySQL for the first time or made changes to models
9. go to MySQL Workbench to view tables

To test user registration backend via Postman

1. run 'python manage.py runserver'
2. open Postman
3. select POST for method with the following url: 'http://localhost:8000/register/'
4. go to headers section and set content type to 'json'
5. go to body section and choose raw, then enter user info to register in the following format
   {
   "username: "testuser",
3   "password": "password"
   }
6. send request

To test user authentication backend via Postman

1. run 'python manage.py runserver'
2. open Postman
3. select POST for method with the following url: http://localhost:8000/login/
4. go to headers section and set content type to 'json'
5. enter an existing users login credentials in the following format:
   {
   "username": "testuser",
   "password": "password123"
   }
6. send request
