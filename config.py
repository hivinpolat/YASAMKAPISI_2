# -*- coding: utf-8 -*-
from os import environ, path
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:whm@47.x.x.x:3306/artcs_pro"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
   
db = SQLAlchemy(app)  
