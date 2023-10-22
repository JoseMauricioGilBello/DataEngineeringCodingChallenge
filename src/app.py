from flask import Flask, render_template, redirect, url_for, jsonify
from config import config, UploadFile, ConfigutationDevelopment #, MAX_NUMBER_OF_ROWS
from mysql_handler import MysqlHandler as msh
from werkzeug.utils import secure_filename
import os
from flask_mysqldb import MySQL

app=Flask(__name__)


conexion = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/upload', methods=['GET', 'POST'])
def uploadcsv():
    form = UploadFile()
    if form.validate_on_submit():
        file = form.file.data
        if file.filename == 'departments.csv':
            result = msh.process_uploaded_department_csv(file)
            print(result)
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
            return "departments csv file has been updated succesfully"
        elif file.filename == 'hired_employees.csv':
            result = msh.process_uploaded_employees_csv(file)
            print(result)
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
            return result
        elif file.filename == 'jobs.csv':
            result = msh.process_uploaded_jobs_csv(file)
            print(result)
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
            return "jobs csv file has been updated succesfully" 
        else:
            return " CSV File should be named: departments.csv o hired_employees.csv o jobs.csv "     
    return render_template('loadcsvfile.html', form= form )

@app.route('/employees_hired_job_dep', methods=['GET'])
def employees_hired_job_dep():
    data = msh.employees_hired_job_dep(2021)
    # print(data)
    return render_template('employees_hired_job_dep.html', results=data)

@app.route('/employees_hired_more_mean_2021', methods=['GET'])
def employees_hired_more_mean_2021():
    data = msh.employees_hired_more_mean_2021(2021)
    # print(data)
    return render_template('employees_hired_more_mean_2021.html', results=data)

def notfound(error):
    # return render_template('404.html'), 404
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404 , notfound)
    app.run()