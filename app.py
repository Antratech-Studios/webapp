
import datetime
import json
import os
import socket
import urllib

import requests

import zcrmsdk
from flask_admin import Admin,BaseView, expose
from flask_admin.menu import MenuLink
from flask import Flask, render_template, url_for, flash, redirect, session, request, jsonify, abort
from flask_login import LoginManager, UserMixin
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from markupsafe import Markup
from wtforms import *
from wtforms.fields.html5 import IntegerRangeField
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
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'business@antratechstudios.com'
app.config['FLASKY_ADMIN'] = 'business@antratechstudios.com'
app.config['MAIL_PASSWORD'] = 'jordan222'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEBUG '] = True
app.config['MAIL_DEFAULT_SENDER'] = 'business@antratechstudios.com'
app.config['FLASKY_ADMIN'] = 'sudomin'


client_id="1000.8JDUVX89OHC16KR3MC2TH9OZQ40PIR"
client_secret="ab36823977ceee9344ce61811798f168d88f9fd2b3"
GRANT_TOKEN = "ba261a78c42e404f327948b5f104e416b752ecb1cb"
# req = requests.get(url='https://accounts.zoho.com/oauth/v2/token?code=1000.fffd2db29875ce359b546d976ca9860a.6d10f93aa6cee77412c94ff26eafb965&redirect_uri=http://7a7335650c61.ngrok.io/callback&client_id=1000.7YU2B14FH318LJCGIMBM2A688Y856T&client_secret=c6debda9f3aaca6623e8575c02ad1450f944530486&grant_type=authorization_code``')
# print(req.status_code)
zoho_config = {
    "client_id":client_id ,
    "client_secret": client_secret,
    "redirect_uri": "http://127.0.0.1/callback",
    'apiBaseUrl': 'https://www.zohoapis.com',
    'apiVersion': 'v2',
    'currentUserEmail': 'business@antratechstudios.com',
    'sandbox': 'False',
    'applicationLogFilePath':'/Users/ASUS/Desktop/AntraTech/Company Website/Codebase',
    'accounts_url': 'https://accounts.zoho.com',
    'token_persistence_path': '/Users/ASUS/Desktop/AntraTech/Company Website/Codebase',
    'access_type': 'offline',
    # 'persistence_handler_class': 'Custom',
    # 'persistence_handler_path': '/Users/Zoho/Desktop/PythonSDK/CustomPersistance.py'

}
leads_url = 'https://www.zohoapis.com/crm/v2/Leads'
access_token = "1000.1f225079a886c73a42adce7fa292da4f.c53f31a202d7003f9696ef2063733ade"
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


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://super:jordan222@antra-db.cv2by5opotk8.us-east-2.rds.amazonaws.com/postgres'
admin = Admin(app, name='Management Panel', template_mode='bootstrap3')
staticPath = op.join(op.dirname(__file__), 'static')


mail = Mail(app)


# zcrmsdk.ZCRMRestClient.initialize(zoho_config)
#
# oauth_client = zcrmsdk.ZohoOAuth.get_client_instance()
# oauth_tokens = oauth_client.generate_access_token(GRANT_TOKEN)

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
    fullname = db.Column(db.VARCHAR)
    budget =db.Column(db.FLOAT)
    phone =db.Column(db.FLOAT)
    company_age = db.Column(db.VARCHAR)
    service = db.Column(db.VARCHAR)
    timeline = db.Column(db.VARCHAR)
    range = db.Column(db.VARCHAR)
    project_summary = db.Column(db.VARCHAR)
    website = db.Column(db.VARCHAR)
    company_name = db.Column(db.VARCHAR)
    source = db.Column(db.VARCHAR)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Work(db.Model):
    __tablename__ = 'work'
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR)
    company_name = db.Column(db.VARCHAR)
    amount =db.Column(db.FLOAT)
    project_summary = db.Column(db.VARCHAR)
    services = db.Column(db.VARCHAR)
    status =db.Column(db.VARCHAR)
    opened =db.Column(db.DateTime)
    closed =db.Column(db.DateTime)
    timeline =db.Column(db.VARCHAR)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class Leads(ModelView):
#    list_template = 'list.html'
    can_delete = True
    details_modal = True
    can_view_details = True
#    form_base_class = SecureForm
    page_size = 50
    column_searchable_list = ['range','service','fullname','budget','source','timeline','company_name','company_age']
    column_filters = ['range','service','fullname','budget','source','timeline','company_name','company_age']
    # column_editable_list = ['role']

    column_hide_backrefs = False
    column_display_all_relations = True
    create_modal = True
    edit_modal = True
    #form_columns = ('email')

    # column_list = ('range','service','fullname','budget','source','timeline','company_name','company_age')
    column_exclude_list = ('project_summary','website')
    form_excluded_columns = ['password','username']
    column_details_exclude_list = ('password','comments','sub_role','lesson','uploads','review','available','cart','roles','followed','bookSchedule','likes','likesEpisode','book','series','episode','posts')


class Works_form(FlaskForm):
    title = StringField('Title')
    company_name = StringField('Company Name')
    amount =FloatField('Amount')
    project_summary = TextAreaField('Project Summary')
    service = MultiCheckboxField(u'service', choices=[('ETED','End-to-end Development'),('Frontend','Front-End Development'),('Backend','Backend Development'),('ShopifyTheme','Shopify Theme Development'),('ShopifyApp','Shopify App Development'),('UI','UI Design'),('Redesign','Website Redesign'),('CustomStore','Custom Ecommerce Store')])
    status =StringField('Status')
    opened =DateField('Opened')
    closed =DateField('Closed')

    timestamp = datetime.datetime.utcnow


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()



class Works(ModelView):
#    list_template = 'list.html'
    form_overrides = dict(text=CKTextAreaField)
    can_delete = True
    details_modal = True
    can_view_details = True
    # form_base_class = SecureForm
    # form   = Works_form
    create_template = 'edit.html'
    edit_template = 'edit.html'
    page_size = 50
    column_searchable_list = ['company_name','services','status']
    column_filters = ['company_name','services','status']
    # column_editable_list = ['role']
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    column_hide_backrefs = False
    column_display_all_relations = True
    create_modal = True
    edit_modal = True
    #form_columns = ('email')

    # column_list = ('range','service','fullname','budget','source','timeline','company_name','company_age')
    column_exclude_list = ('project_summary','website')
    # form_excluded_columns = ['password','username']
    column_details_exclude_list = ('services')


    def project_summary(view, context, model, name):
        if not model.project_summary:
            return ''

        return Markup('<div class="container-fluid"  >' + model.project_summary + '</div>')

    column_formatters_detail = {
        'project_summary': project_summary    }


    form_overrides = {
    'project_summary': CKTextAreaField
}

class ContactForm(FlaskForm):
    email = StringField('email', [validators.Email()])
    fullname = StringField('fullname')
    budget = StringField('budget')
    company_age = StringField('company_age')
    service = MultiCheckboxField(u'service', choices=[('End-to-end Development','End-to-end Development'),('Front-End Development','Front-End Development'),('Backend Development','Backend Development'),('Shopify Theme Development','Shopify Theme Development'),('Shopify App Development','Shopify App Development'),('UI Design','UI Design'),('Website Redesign','Website Redesign'),('Custom Ecommerce Store','Custom Ecommerce Store')])
    timeline = StringField('timeline')
    range = MultiCheckboxField('What is your budget',choices=[('$400-$500','$400-$500'),('$500-$600','$500-$600'),('$600-$700','$600-$700'),('$700-$800','$700-$800'),('$800-$900','$800-$900'),('$1000+','$1000+')])
    project_summary = TextAreaField('project_summary')
    website = StringField('website')
    company_name = StringField('company_name')
    source = StringField('source')
    submit = SubmitField('Submit')

    # def validate_username(self,username):
    #     user = Lead.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValidationError('That username is taken')
    #     elif " " in username.data:
    #         raise ValidationError('Whitespace not allowed')

    # def validate_email(self,email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError('That email already exists')

admin.add_view(Leads(Lead, db.session, category="Leads",name="Leads Management"))
admin.add_view(Works(Work, db.session, category="Works",name="Works Management"))

def insert_records(access_token,url,fname,email,phone,company):



    headers = {
        'Authorization': 'Zoho-oauthtoken %s' % (access_token),
    }

    request_body = dict()
    record_list = list()

    record_object_1 = {
        'Company': company,
        'Email': email,
        'Last_Name': fname,
        'First_Name': '',

    }

    record_list.append(record_object_1)


    request_body['data'] = record_list

    trigger = [
        'approval',
        'workflow',
        'blueprint'
    ]

    request_body['trigger'] = trigger

    response = requests.post(url=url, headers=headers, data=json.dumps(request_body).encode('utf-8'))

    if response is not None:
        print("HTTP Status Code : " + str(response.status_code))

        print(response.json())

    return response.json()
def insert_test():



    headers = {
        'Authorization': 'Zoho-oauthtoken %s' % (access_token),
    }

    request_body = dict()
    record_list = list()

    record_object_1 = {
        'Company': 'company',
        'Email': 'emal@gmail.com',
        'Last_Name': 'fname',
        'First_Name': '',

    }

    record_list.append(record_object_1)


    request_body['data'] = record_list

    trigger = [
        'approval',
        'workflow',
        'blueprint'
    ]

    request_body['trigger'] = trigger

    response = requests.post(url=leads_url, headers=headers, data=json.dumps(request_body).encode('utf-8'))

    if response is not None:
        print("HTTP Status Code : " + str(response.status_code))

        print(response.json())

    return response.json()


# Python program to convert a list to string

# Function to convert
def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

    # return string
    return str1




@app.route('/add')
def add():
    try:
        record_ins_list = list()
        for i in range(0, 2):
            record = zcrmsdk.ZCRMRecord.get_instance('Invoices')  # module API Name
            record.set_field_value('Subject', 'Invoice' + str(i))
            record.set_field_value('Account_Name', 'IIIT')
            user = zcrmsdk.ZCRMUser.get_instance(440872000000175001, 'Python Automation User1')
            record.set_field_value('Owner', user)
            line_item = zcrmsdk.ZCRMInventoryLineItem.get_instance(zcrmsdk.ZCRMRecord.get_instance("Products", 440872000000224005))
            line_item.discount = 10
            line_item.list_price = 8
            line_item.description = 'Product Description'
            line_item.quantity = 100
            line_item.tax_amount = 2.5
            taxIns = zcrmsdk.ZCRMTax.get_instance("Vat")
            taxIns.percentage = 5
            line_item.line_tax.append(taxIns)
            record.add_line_item(line_item)
            record_ins_list.append(record)
        resp = zcrmsdk.ZCRMModule.get_instance('Invoices').create_records(record_ins_list)
        print(resp.status_code)
        print(resp.data)
    except zcrmsdk.ZCRMException as ex:
        print(ex.status_code)
        print(ex.error_message)
        print(ex.error_code)
        print(ex.error_details)
        print(ex.error_content)
@app.route('/test')
def test():

    endpoint = '/auth'
    url = 'https://accounts.zoho.com/oauth/v2'
    params = {
        'client_id': client_id,
        'response_type':'code',
        'scope':'AaaServer.profile.Read,ZohoCRM.modules.ALL',
        'redirect_uri':'http://127.0.0.1:5000/callback',
        'access_type ':'offline',
        'prompt':'consent'

    }
    auth_code = requests.post(url=url+endpoint,params=params)
    print(auth_code.json)
    print(auth_code.url)
    print( auth_code.encoding)


    return auth_code.url


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
    contactForm = ContactForm()
    return render_template('contact.html',contactForm=contactForm)

@app.route('/company')
def company():
    return render_template('company.html')
@app.route('/callback')
def callback():
    endpoint = '/token'
    code = request.args.get('code')
    print(code)
    url = 'https://accounts.zoho.com/oauth/v2'
    params = {
        'client_id': client_id,
        'grant_type': 'authorization_code',
        'client_secret': client_secret,
        'redirect_uri':'http://127.0.0.1:5000/callback',
        'code':code

    }

    token = requests.post(url=url+endpoint,data=params)
    print(token.content)
    print(token.json)
    return token.json()


@app.route('/process')
def process():
    return render_template('process.html')

@app.route('/policy')
def policy():
    return render_template('policy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/form', methods=['POST'])
def process_form():
    form = ContactForm()
    if request.method == 'POST' :
        # email = request.args.get('email')
        # budget = request.args.get('budget')
        # company_age = request.args.get('company_age')
        # service = request.args.get('service')
        # timeline = request.args.get('timeline')
        # range = request.args.get('range')
        # project_summary = request.args.get('project_summary')
        # website = request.args.get('website')
        # source = request.args.get('source')
        # company_name = request.args.get('company_name')
        services_data = request.form.getlist('service')
        services_data = str(services_data)

        lead = Lead(
            email=form.email.data,
            # budget=form.budget.data,
            # company_age=form.company_age.data,
            service=services_data,
            timeline=form.timeline.data,
            range=form.range.data,
            project_summary=form.project_summary.data,
            website=form.website.data,
            source=form.source.data,
            company_name=form.company_name.data)

        db.session.add(lead)
        db.session.commit()

        try:

            headers = {
                'Authorization': 'Zoho-oauthtoken %s' % (access_token),
            }

            request_body = dict()
            record_list = list()
            range_str = listToString(form.range.data)
            service_str = listToString(form.service.data)
            print(service_str)

            record_object_1 = {
                'Company': form.company_name.data,
                'Email': form.email.data,
                'Last_Name': form.fullname.data,
                'First_Name': '',
                'Lead_Source': 'Website',
                'Lead_Status': 'Contact in Future',
                'Budget': form.budget.data,
                'Project_Budget': range_str,
                'Service': form.service.data,
                'Project_Summary': form.project_summary.data,
                'Website': form.website.data,

            }

            record_list.append(record_object_1)

            request_body['data'] = record_list

            trigger = [
                'approval',
                'blueprint'
            ]

            request_body['trigger'] = trigger

            response = requests.post(url=leads_url, headers=headers, data=json.dumps(request_body).encode('utf-8'))

            if response is not None:
                print("HTTP Status Code : " + str(response.status_code))

                print(response.json())

            return redirect(url_for('home'))



            # insert_records(access_token=access_token,url=leads_url,fname=form.fullname.data,email=form.email.data,company=form.company_name.data)
            # print(insert_records)
        except:
            print('fail')
            jsonify('status','A problem occurred while sending the email')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('contact'))




if __name__ == '__main__':
    app.run(debug=True)
