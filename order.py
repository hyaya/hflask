#coding:utf8
#all the import
import sqlite3,os
from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash

#-----------
#all configuration
DATABASE = r"E:\Codes\hflask\tmp\order.py"
DEBUG = True    #开启调试模式，允许执行服务器上的代码
SECRET_KEY = 'order key'    #用于保持客户端的会话安全
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)#from_object()会查看给定的对象，搜索对象中所有变量名称为大写的变量

#通常，从一个配置文件中导入配置是比较好的做法，使用from_envvar()来完成，替换from_object()即可
# app.config.from_envvar('FLASKR_SETTINGS',silent=True)
#silent=True告诉Flask如果没有这个环境变量不要报错
#FLASKR_SETTING，设置一个名为FLASKR_SETTING的环境变量，来指定一个配置文件
@app.route('/')
# def hello_world():
#     return 'Hello World!'
def show_entries():#显示数据库中所有条目，id值最大的在上面
    cur = g.db.execute('select title,text from entries order by id desc')
    entries = [dict(title=row[0],text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html',entries=entries)
@app.route('/add',methods=['POST'])
def add_entry():#条目添加
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('INSERT INTO entries (title,text) VALUES (?,?)',
                 [request.form['title'],request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted.')
    return redirect(url_for('show_entries'))    #重定向到show_entries页面
@app.route('/login',methods=['GET','POST'])
def login():#登陆模块
    error = None
    if request.method=='POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username!'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid passwd!'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html',error=error)
@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
#添加一个方便连接指定数据库的方法
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    return conn

#创建一个用来初始化数据库的函数
from contextlib import closing
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql',mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# 请求数据库连接
@app.before_request
def before_request():
    g.db = connect_db()
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
    g.db.close()
if __name__ == '__main__':
    app.run()
