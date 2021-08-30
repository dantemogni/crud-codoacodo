from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app) 

class Employee(db.Model):
    #Employee table
    
    id      = db.Column(db.Integer, primary_key=True)
    name    = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    mail    = db.Column(db.String(255), nullable=False)
    photo   = db.Column(db.String(255), nullable=True)

    def __init__(self, name, surname, mail, photo=None):
        self.name = name
        self.surname = surname
        self.mail = mail
        self.photo = photo