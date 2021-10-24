#!/usr/bin/python3

import base64
import hashlib
import sys
import os
from Crypto import Random
from Crypto.Cipher import AES
from werkzeug.exceptions import abort
from functools import wraps
from flask import Flask, render_template, request, url_for, flash, redirect, session, make_response, g
import mysql.connector


DB_HOST = os.getenv("MYSQL_HOST", "xxxxxxx")
DB_USER = os.getenv("MYSQL_USER", "xxxxxxx") 
DB_PASS = os.getenv("MYSQL_PASSWORD", "xxxxxxx") 
DB_NAME = os.getenv("MYSQL_DATABASE", "xxxxxxx") 


# input: bytes, output: base64 text
def encrypt(plainbytes, key):
    
    iv = Random.new().read(AES.block_size)
    
    cipher = AES.new(key, AES.MODE_CFB, iv)
    
    cipherbytes = cipher.encrypt(plainbytes)

    ciphertext = base64.b64encode(iv + cipherbytes)

    return ciphertext


# input: base64 text, output: bytes
def decrypt(ciphertext, key):

    cipherbytes = base64.b64decode(ciphertext)

    iv = cipherbytes[:AES.block_size]

    cipher = AES.new(key, AES.MODE_CFB, iv)

    plainbytes = cipher.decrypt(cipherbytes[AES.block_size:])

    return plainbytes

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
    cur.execute('SELECT id, username, password, email, encryptkey, role from users WHERE username = %s AND password = %s',
                    (username, password))
    user = cur.fetchone()
    
    cur.close()
    conn.close()

    return user

def do_register(username, password, email, role):
    key = base64.b64encode(Random.new().read(AES.block_size))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO users (username, password, email, role, encryptkey ) VALUES (%s, %s, %s, %s, %s)',
                    (username, password, email, role, key))
    conn.commit()
    cur.close()
    conn.close()

def get_encryptkey(userid):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT encryptkey from users WHERE id = %s',
                    (userid, ))
    user = cur.fetchone()
    
    cur.close()
    conn.close()

    return base64.b64decode(user[0])

app = Flask(__name__)

app.config['SECRET_KEY'] = 'xxxxxxxxxxxxxxxx'

ROLE_ADMIN = 0
ROLE_USER = 1

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):

        try:
        
            ciphertext = request.cookies.get('authtoken')

            userid = request.cookies.get('userid')

            if not ciphertext or not userid:
                return redirect(url_for('login'))

            encryptkey = get_encryptkey(userid)

            plainbytes = decrypt(ciphertext, encryptkey)

            usernamelen = int.from_bytes(plainbytes[:2], "little")
            usernameencoded = plainbytes[2:usernamelen+2]
            username = usernameencoded.decode("utf-8")
            role = plainbytes[usernamelen+2]
            
            g.username = username
            g.role = role

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
    if g.role == ROLE_ADMIN:
        flag = "xxxxxxxxxxxxxxxxxxxxxxx"
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
                
                userid = user[0]
                username = user[1]
                role = user[5]

                # get key
                key = base64.b64decode(user[4])

                # create authtoken
                usernamebytes = username.encode('utf-8')
                usernamelen = len(usernamebytes)
                plainbytes = len(usernamebytes).to_bytes(2, "little") + usernamebytes + role.to_bytes(1, "little")

                ciphertext = encrypt(plainbytes, key)

                response = make_response(redirect(url_for('index')))

                response.set_cookie('userid', str(userid))
                response.set_cookie('authtoken', ciphertext)

                return response

    return render_template('login.html')

@app.route("/logout")
def logout():
    response = make_response(redirect(url_for('index')))

    response.set_cookie('userid', '0', expires=0)
    response.set_cookie('authtoken', '', expires=0)

    return response

app.run(host="0.0.0.0", port=8080, debug=False)