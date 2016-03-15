#coding:utf8
#all the import
import sqlite3
from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash
#-----------
#all configuration
DATABASE = 'tmp\order.db'
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
def hello_world():
    return 'Hello World!'

#添加一个方便连接指定数据库的方法
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

#创建一个用来初始化数据库的函数
from contextlib import closing
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql',mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

if __name__ == '__main__':
    app.run()
