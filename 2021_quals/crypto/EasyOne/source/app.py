#!/usr/bin/python3

import base64
import hashlib
from logging import NullHandler, root
import sys
import os
from Crypto import Random
from Crypto.Cipher import AES
from werkzeug.exceptions import abort
from functools import wraps
from flask import Flask, render_template, request, url_for, flash, redirect, session, make_response, g
import mysql.connector
import werkzeug
import ssl
import OpenSSL
from OpenSSL import crypto
from certutils import CertInfo, verify_certificate_chain


DB_HOST = os.getenv("MYSQL_HOST", "xxxxxx")
DB_USER = os.getenv("MYSQL_USER", "xxxxxx") 
DB_PASS = os.getenv("MYSQL_PASSWORD", "xxxxxx") 
DB_NAME = os.getenv("MYSQL_DATABASE", "xxxxxx") 


def get_db_connection():
    conn = mysql.connector.connect(host = DB_HOST, user = DB_USER, passwd = DB_PASS, database = DB_NAME, auth_plugin='mysql_native_password')
    conn.autocommit = True
    return conn

def get_post(post_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute('SELECT * FROM posts WHERE id = %s',
                        (post_id,))
    post = cur.fetchone()
    cur.close()
    conn.close()
    
    if post is None:
        abort(404)
    return post

def verify_login(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, username, password, email, role from users WHERE username = %s AND password = %s',
                    (username, password))
    user = cur.fetchone()
    
    cur.close()
    conn.close()

    return user

def do_register(username, password, email, role):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO users (username, password, email, role) VALUES (%s, %s, %s, %s)',
                    (username, password, email, role))
    conn.commit()
    cur.close()
    conn.close()



def validate_certificate(file):
    
    trusted_certs = ['./ca.crt', './app.crt']

    for root_cert in trusted_certs:
        if not os.path.isfile(root_cert):
            raise Exception("Cannot found root certs")

    clientcert = file.stream.read()

    return verify_certificate_chain(clientcert, trusted_certs)


app = Flask(__name__)

app.config['SECRET_KEY'] = 'xxxxxxxxxxxxxxxx'

ROLE_ADMIN = 0
ROLE_USER = 1

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):

        try:
            if "username" not in session or session["username"] == "" or session["username"] is None:
                abort(401)
            print(session["username"])
        except:
            abort(401)
        
        return f(*args, **kwargs)
   
    return wrap


@app.route("/index")
@login_required
def index():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute('SELECT * FROM posts')
    posts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route("/flag")
@login_required
def flag():
    flag = "You are not admin"
    if session["role"] == ROLE_ADMIN:
        flag = "ASCIS{xxxxxx}"
    return render_template('flag.html', flag=flag)


@app.route('/<int:post_id>')
@login_required
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route("/about")
@login_required
def about():
    return render_template('about.html')

@app.route("/register", methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role = ROLE_USER

        if not username or not password:
            flash('Username and Password is required!')
        else:
            do_register(username, password, email, role)

            return redirect(url_for('login'))

    return render_template('register.html')


@app.route("/", methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Username and Password is required!')
        else:
            # verify login
            user = verify_login(username, password)

            if not user:
                flash('Username and Password is not correct!')
            else:
                session["username"] = user[1]
                session["role"] = user[4]

                return redirect(url_for('index'))

    return render_template('login.html')

# This function only for admin
@app.route("/logincert", methods=('GET', 'POST'))
def logincert():
    if request.method == 'POST':
        username = None
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            split_tup = os.path.splitext(uploaded_file.filename)
            if split_tup[1] != ".pem":
                flash('Cert file is invalid')
                return render_template('logincert.html')
            else:    
                username = validate_certificate(uploaded_file)

        if username is None:
            flash('Login cert is invalid!')
            return render_template('logincert.html')
        else:    
            session["username"] = username
            session["role"] = ROLE_ADMIN

            return redirect(url_for('index'))

    return render_template('logincert.html')

@app.route("/logout")
def logout():
    session["username"] = None
    session["role"] = None
    session.clear()
    return redirect(url_for('login'))

app.run(host="0.0.0.0", port=8100, debug=False)
