from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired

class ConfigutationDevelopment():
    DEBUG = True
    SECRET_KEY = 'your_secret_key'
    UPLOAD_FOLDER = 'static/files'
    MYSQLHOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'admin'
    MYSQL_DB = 'globant'

config = {
    'development': ConfigutationDevelopment
}

class UploadFile(FlaskForm):
    file = FileField('File', validators= [InputRequired()])
    submit = SubmitField('Upload CSV File')