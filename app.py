from flask import Flask, render_template, url_for, flash, redirect, session, request, jsonify, abort

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/works')
def worsk():
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

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
