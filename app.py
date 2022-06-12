# -*- coding: utf-8-*-
from flask import url_for, escape
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/hello')
def hello():
    return '<h1>hello!</h1>'

@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % escape(name)

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name = 'zcx'))
    print(url_for('user_page', name = 'zzz'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num = 2))
    return 'Test page'

name = 'zcxhhh'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]

@app.route('/')
def index():
    return render_template('index.html',name=name,movies=movies)