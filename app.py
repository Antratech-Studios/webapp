
import datetime
import json
import os
import socket

from flask_admin import Admin,BaseView, expose
from flask_admin.menu import MenuLink
from flask import Flask, render_template, url_for, flash, redirect, session, request, jsonify, abort
from flask_login import LoginManager, UserMixin
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import *
from wtforms.validators import Required
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin

from wtforms.widgets import TextArea
from flask_admin.form import SecureForm
import os.path as op
app = Flask(__name__)



app.config['SECRET_KEY'] = 'Adawug;irwugw79536870635785ty0875y03davvavavdey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'
app.config['WTF_CSRF_ENABLED'] = False
app.config['COMPANY_EMAIL'] = 'business@antratechstudios.com'

app.config['MAIL_SERVER']='mail.privateemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'business@antratechstudios.com'
app.config['FLASKY_ADMIN'] = 'business@antratechstudios.com'
app.config['MAIL_PASSWORD'] = 'jordan222'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'johnoula@icloud.com'
app.config['FLASKY_ADMIN'] = 'sudomin'

csrf = CSRFProtect(app)
# IP address
def get_Host_name_IP(hostname):
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        if host_name == hostname:
            print("Hostname :  ", host_name)
            print("IP : ", host_ip)
            return True
        else:
            return False
    except:
        print("Unable to get Hostname and IP")

if get_Host_name_IP('CJAY') == True:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@qwerty1234!@localhost/antradb'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://power_user:'


mail = Mail(app)

#### MODELS ####

db = SQLAlchemy(app)
db.init_app(app)

migrate = Migrate(app,db)

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(admin_id):
    return Admins.query.get(int(admin_id))
class Admins(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True, nullable=True)
    password = db.Column('password',db.String(500), nullable=True)

class Lead(db.Model):
    __tablename__ = 'lead'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column(db.VARCHAR)
    budget =db.Column(db.FLOAT)
    company_age = db.Column(db.VARCHAR)
    service = db.Column(db.VARCHAR)
    timeline = db.Column(db.VARCHAR)
    range = db.Column(db.VARCHAR)
    project_summary = db.Column(db.VARCHAR)
    website = db.Column(db.VARCHAR)
    company_name = db.Column(db.VARCHAR)
    source = db.Column(db.VARCHAR)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/works')
def works():
    return render_template('works.html')

@app.route('/works/')
def case():
    return render_template('case.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/company')
def company():
    return render_template('company.html')

@app.route('/process')
def process():
    return render_template('process.html')

@app.route('/form', methods=['POST'])
def form():
    data = request.args.to_dict()
    if request.method == 'POST' and data:
        email = request.args.get('email')
        budget = request.args.get('budget')
        company_age = request.args.get('company_age')
        service = request.args.get('service')
        timeline = request.args.get('timeline')
        range = request.args.get('range')
        project_summary = request.args.get('project_summary')
        website = request.args.get('website')
        source = request.args.get('source')
        company_name = request.args.get('company_name')

        lead = Lead(
            email=email,
            budget=budget,
            company_age=company_age,
            service=service,
            timeline=timeline,
            range=range,
            project_summary=project_summary,
            website=website,
            source=source,
            company_name=company_name)

        db.session.add(lead)
        db.session.commit()
        try:
            msg = Message("Testing", sender=email, recipients=[app.config['COMPANY_EMAIL']])
            mail.send(msg)
        except:
            jsonify('status','A problem occurred while sending the email')
        return jsonify('status','submitted successfully')
    else:
        return jsonify('status','Please complete the form')




if __name__ == '__main__':
    app.run()
