from flask import url_for, escape
from flask import Flask
app = Flask(__name__)

@app.route('/')
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