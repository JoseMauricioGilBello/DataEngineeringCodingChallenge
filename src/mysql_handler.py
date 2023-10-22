from flask import Flask, render_template, redirect, url_for, jsonify
from flask_mysqldb import MySQL
import pandas as pd
app=Flask(__name__)
conexion = MySQL(app)

class MysqlHandler():

    def process_uploaded_department_csv(file):
        try:
            # Connect to the MySQL database
            cursor = conexion.connection.cursor()

            # Process the uploaded CSV file
            data = pd.read_csv(file, header=None, names=['id', 'department'])
            num_rows = len(data)
            print(num_rows)
            if num_rows <= 1000:
                # Check if the table 'departments' exists in the database
                cursor.execute("SHOW TABLES LIKE 'departments'")
                table_exists = cursor.fetchone()

                if not table_exists:
                    # If the 'departments' table doesn't exist, create it
                    cursor.execute(
                        "CREATE TABLE departments (id INT  PRIMARY KEY, department VARCHAR(100))"
                    )

                # Iterate through the CSV data and perform upserts
                for _, row in data.iterrows():
                    query = (
                        "INSERT INTO departments (id, department) "
                        "VALUES (%s, %s) "
                        "ON DUPLICATE KEY UPDATE id=VALUES(id), department=VALUES(department)"
                    )
                    values = (row['id'], row['department'])
                    cursor.execute(query, values)
                    conexion.connection.commit()
                return {"message": "department CSV data uploaded (upsert) successfully"}
            return {"error": "file CSV contain more than 1000 row. Can not be processed."}
        except Exception as e:
            return {"error": str(e)}
        
    def process_uploaded_employees_csv(file):
        try:
            # Connect to the MySQL database
            cursor = conexion.connection.cursor()
            # Process the uploaded CSV file
            data = pd.read_csv(file, header=None, names=['id', 'name', 'datetime', 'department_id', 'job_id'])
            # validation 
            num_rows = len(data)
            print(num_rows)
            if num_rows <= 1000:
                # replacing null values with no information
                valor_de_reemplazo_str = "no information"
                data['name'] = data['name'].fillna(valor_de_reemplazo_str)
                # create a default value for datetime
                new_date = "1900-01-01T00:00:00Z"
                data['datetime'] = data['datetime'].fillna(new_date)
                # replacing null values with a 0
                valor_de_reemplazo_int = 0
                data['department_id'] = data['department_id'].fillna(valor_de_reemplazo_int)
                data['job_id'] = data['job_id'].fillna(valor_de_reemplazo_int)


                # Check if the table 'departments' exists in the database
                cursor.execute("SHOW TABLES LIKE 'employees'")
                table_exists = cursor.fetchone()

                if not table_exists:
                    # If the 'departments' table doesn't exist, create it
                    cursor.execute(
                        "CREATE TABLE employees (id INT PRIMARY KEY, name VARCHAR(100), datetime VARCHAR(100), department_id INT, job_id INT)"
                    )

                # Iterate through the CSV data and perform upserts
                for _, row in data.iterrows():
                    query = (
                        "INSERT INTO employees (id, name, datetime, department_id, job_id) "
                        "VALUES (%s, %s,%s, %s, %s) "
                        "ON DUPLICATE KEY UPDATE id=VALUES(id), name=VALUES(name), datetime=VALUES(datetime), department_id=VALUES(department_id), job_id=VALUES(job_id)"
                    )
                    values = (row['id'], row['name'], row['datetime'], row['department_id'], row['job_id'])
                    cursor.execute(query, values)
                    conexion.connection.commit()
                return {"message": "Employees CSV data uploaded (upsert) successfully"}
            return {"error": "file CSV contain more than 1000 row. Can not be processed."}
        except Exception as e:
            return {"error": str(e)}
        
    
    def process_uploaded_jobs_csv(file):
        try:
            # Connect to the MySQL database
            cursor = conexion.connection.cursor()
            # Process the uploaded CSV file
            data = pd.read_csv(file, header=None, names=['id', 'job'])
            num_rows = len(data)
            print(num_rows)
            if num_rows <= 1000:            
                # Check if the table 'departments' exists in the database
                cursor.execute("SHOW TABLES LIKE 'jobs'")
                table_exists = cursor.fetchone()

                if not table_exists:
                    # If the 'departments' table doesn't exist, create it
                    cursor.execute(
                        "CREATE TABLE jobs (id INT PRIMARY KEY, job VARCHAR(100))"
                    )

                # Iterate through the CSV data and perform upserts
                for _, row in data.iterrows():
                    query = (
                        "INSERT INTO jobs (id, job) "
                        "VALUES (%s, %s) "
                        "ON DUPLICATE KEY UPDATE id=VALUES(id), job=VALUES(job)"
                    )
                    values = (row['id'], row['job'])
                    cursor.execute(query, values)
                    conexion.connection.commit()
                return {"message": "Jobs CSV data uploaded (upsert) successfully"}
            return {"error": "file CSV contain more than 1000 row. Can not be processed."}
        except Exception as e:
            return {"error": str(e)}
        


    def employees_hired_job_dep(year):
        try:
           query = (
            "SELECT "
                "d.department AS department,"
                "'' AS emptycol, " 
                "j.job AS job,"
                "SUM(IF(MONTH(e.datetime) BETWEEN 1 AND 3, 1, 0)) AS Q1, "
                "SUM(IF(MONTH(e.datetime) BETWEEN 4 AND 6, 1, 0)) AS Q2, "
                "SUM(IF(MONTH(e.datetime) BETWEEN 7 AND 9, 1, 0)) AS Q3, "
                "SUM(IF(MONTH(e.datetime) BETWEEN 10 AND 12, 1, 0)) AS Q4 "
            "FROM employees e "
            "INNER JOIN departments d ON e.department_id = d.id "
            "INNER JOIN jobs j ON e.job_id = j.id "
            "WHERE YEAR(e.datetime) = 2021 "
            "GROUP BY department, job "
            "ORDER BY department, job; "
            )
           print(query)
           cursor = conexion.connection.cursor()
           cursor.execute(query)
           result = cursor.fetchall()
           df = pd.DataFrame(result, columns=['department','','job', 'Q1', 'Q2', 'Q3', 'Q4'])
           df_to_json = df.to_dict(orient='records')
           return df_to_json 

        except Exception as e:
            return {"error": str(e)}

        
    def employees_hired_more_mean_2021(year):
        try:
           query = (
            "SELECT "
                "d.id AS id, "
                "d.department AS department, "
                "COUNT(e.id) AS hired "
            "FROM globant.departments d "
            "INNER JOIN globant.employees e ON d.id = e.department_id "
            "WHERE YEAR(e.datetime) = 2021 "
            "GROUP BY d.id, d.department "
            "HAVING COUNT(e.id) > ( "
                "SELECT AVG(employee_count) "
                "FROM ( "
                    "SELECT d.id AS department_id, COUNT(e.id) AS employee_count "
                    "FROM globant.departments d "
                    "INNER JOIN globant.employees e ON d.id = e.department_id "
                    "WHERE YEAR(e.datetime) = 2021 "
                    "GROUP BY d.id "
                ") AS department_stats "
            ") "
            "ORDER BY hired DESC; "
            )
           print(query)
           cursor = conexion.connection.cursor()
           cursor.execute(query)
           result = cursor.fetchall()
           df = pd.DataFrame(result, columns=['id','department','hired'])
           df_to_json = df.to_dict(orient='records')
           return df_to_json 

        except Exception as e:
            return {"error": str(e)}