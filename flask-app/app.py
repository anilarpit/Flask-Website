from flask import Flask, render_template, request, flash, redirect, url_for, session
from data import Articles
import os
import json


app = Flask(__name__)

app.secret_key='thisissecret'

picfolder = os.path.join('static', 'pics')

app.config['UPLOAD_FOLDER'] = picfolder

class user:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
    
    def __repr__():
        return f'<user: {self.email}>'

Articles = Articles()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'Arpit.jpg')
    return render_template('about.html', user_image = pic1)

@app.route('/articles', methods=['GET', 'POST'])
def article():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        lists = []

        if os.path.exists('content.json'):
            with open('content.json') as cont_file:
                lists = json.load(cont_file)

        for i in lists:
            if((i['email'] == email) and (i['password'] == password)):
                return render_template('articles.html', articles=Articles, name=i['name'])
            elif(i['email'] == email):
                flash('Wrong Password')
                return redirect(url_for('login'))

        flash("You do not have an account. Please Sign Up for one")
        return redirect(url_for('sign_up'))
    else:
        flash('Please sign Up')
        return redirect(url_for('sign_up'))

@app.route('/articles/<string:id>')
def articles(id):
    return render_template('article.html', id=id)

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email=request.form.get('email')
        name=request.form.get('name')
        password=request.form.get('password')
        users = {'name': name, 'email': email, 'password': password}
        lists = []
        
        if os.path.exists('content.json'):
            with open('content.json') as cont_file:
                lists = json.load(cont_file)

        if lists:
            for i in lists:
                if (i['email'] == email):
                    flash('account exists with this email')
                    return redirect(url_for('login'))

        lists.append(users)
        with open('content.json', 'w') as cont_file:
            json.dump(lists, cont_file)
            session[request.form['email']] = True

        flash('Success! Please Login with your credentials')
        return redirect(url_for('login'))
    else:
        return render_template('login.html')
