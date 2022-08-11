import pymysql
from flask import Flask, render_template, request

import random
import threading
import time

""" Open Flask and Run ( Make Website)"""
test_db_conn = pymysql.connect(
    user='root',
    passwd='mysql',
    host='192.168.0.5',
    db='TESTDB',
    charset='utf8'
)
try:
    cursor = test_db_conn.cursor()
    #Flask 객체 인스턴스 생성
    app = Flask(__name__)
    @app.route('/') # 접속하는 url
    def index():
        sql = "SELECT * from tb"
        print(sql)
        cursor.execute(sql)
        data_list = cursor.fetchall()
        return render_template('index2.html',data_list=data_list)
except:
    test_db_conn.close()
if __name__=="__main__":
    app.run(debug=True)