# -*- coding: utf-8 -*-

from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

import click
from flask import current_app, g
from flask.cli import with_appcontext
import sqlite3



db = SQLAlchemy()
app = Flask(__name__)
app.secret_key = 'blog'
def create_app(self, reference_app=None):
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        
        db.create_all()  # Create database tables for our data models

    if reference_app is not None:
            return reference_app

    if self.app is not None:
            return self.app

    if current_app:
       return current_app._get_current_object()   


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    dogumtarihi=db.Column(db.String(80), unique=False, nullable=False)
    birim=db.Column(db.String(80), unique=False, nullable=False)
    telefon=db.Column(db.String(80), unique=False, nullable=False)
    tc=db.Column(db.Integer, unique=False, nullable=False)# -*- coding: utf-8 -*-

    def __repr__(self):
        return '<User {}>'.format(self.username)

 #LOGINNNN  
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Bu sayfayı görüntülemek için giriş yapın', 'danger')
            return redirect(url_for('login'))
    return decorated_function


   
    
class RegisterForm(Form):
    name = StringField('İsim Soyisim', validators=[validators.Length(min=5, max=15)])
    username =  StringField('Kullanıcı Adı', validators=[validators.Length(min=3, max=15)])
    email = StringField('Mail',validators=[validators.Email(message='Gecerli bir email adresi giriniz')])
    dogumtarihi=StringField('Doğum Tarihi',validators=[validators.Length(min=10,max=15)])
    birim=StringField('Birim',validators=[validators.Length(min=5,max=15)])
    tc=StringField('TC',validators=[validators.Length(max=11)])
    telefon=StringField('Telefon',validators=[validators.Length(max=12)])
    password = PasswordField('Password', validators = [
        validators.DataRequired(message='Lütfen bir parola belirleyiniz'),
        validators.EqualTo(fieldname='confirm', message='Parolanız uyuşmuyor')
    ])
    confirm = PasswordField('Parola Doğrula')
    

class LoginForm(Form):
    username =  StringField('Kullanıcı Adı')
    password = PasswordField('Password')
  
@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        username = form.username.data
        passwordEntered = form.password.data

        user = User.query.filter_by(username=username).first()

        if user is not None:
            realPassword = user.password
            if sha256_crypt.verify(passwordEntered, realPassword):
                flash('Basarı ile giris yaptınız', 'success')
                
                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('index'))
            else:
                flash('Parola yanlış', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Kullanıcı bulunamadı', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        tc=form.tc.data
        telefon=form.telefon.data
        birim=form.birim.data
        dogumtarihi=form.dogumtarihi.data
        password = sha256_crypt.encrypt(form.password.data)
        
        newUser = User(name= name, username= username, email= email,tc=tc,telefon=telefon,dogumtarihi=dogumtarihi,birim=birim, password= password)
        
        db.session.add(newUser)
        db.session.commit()
        flash('Başarı ile kayıt oldunuz', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('register.html', form=form)
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if(__name__) == '__main__':
  
    app.run(debug=True)
     

   
  