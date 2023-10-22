# Globant’s Data Engineering Coding Challenge
Python Deployment Project

This is a Python project that uses Flask and MySQL to manage CSV files and execute database queries. Below, you will find a step-by-step guide for deploying this project.

Steps to Deploy the Project

1. Set Up the Virtual Environment

To isolate the project's dependencies, it is recommended to use a virtual environment. You can create one using the following command:

python -m venv myenv

Activate the virtual environment:

- On Windows:

myenv\Scripts\activate

- On macOS and Linux:

source myenv/bin/activate

2. Download the Project

Download the project from its repository or copy the files and folders to your working directory.

3. Install Dependencies

Within the virtual environment, install the necessary dependencies from the requirements.txt file with the following command:

pip install -r requirements.txt

4. Configure the Database

Ensure you have a MySQL server up and running. You can modify the database configuration in the config.py file if necessary.

MYSQLHOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'admin'
MYSQL_DB = 'globant'

5. Create Database Tables

Execute the following command to create the tables in the database:

python -c "from app import conexion; conexion.create_all()"

6. Run the Application

To run the Flask application, use the following command:

python app.py

The application will be accessible at http://localhost:5000 in your web browser.

7. Upload CSV Files

The application allows you to upload CSV files with data for departments, employees, and jobs. Ensure that the files have the following names:

- departments.csv
- hired_employees.csv
- jobs.csv

You can upload these files from the application's web page.

8. Execute Queries

The application provides the following routes for executing queries:

- http://localhost:5000/employees_hired_job_dep: Query about employees hired by department and job in the year 2021.
- http://localhost:5000/employees_hired_more_mean_2021: Query about departments that hired more employees than the average in 2021.

9. Stop the Application

Once you've finished using the application, you can stop it by pressing Ctrl + C in the terminal.

That's it! You have successfully deployed the Python project using Flask and MySQL. You can access the queries and manage data in your database.
