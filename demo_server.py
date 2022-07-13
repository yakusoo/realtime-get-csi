#!/usr/bin/env python
# --coding:utf-8--

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from os import path
from urllib.parse import urlparse
import cgi
import configparser
import json
import demo_display
import subprocess

curdir = path.dirname(path.realpath(__file__))
sep = '/'
config = configparser.ConfigParser()
setting = {}
settingfile = 'setting.ini'
settingsection = 'SETTING'
settingoption = [
    'frequency',
    'adress_ap',
    'adress_sta',
    'learning_file_name',
    'learning_file_output',
    'model_file_name',
    'model_file_ouput',
    'loop_time',
    'measurement_time'
    ]
count = 1
loopcount = 1

# MIME-TYPE
mimedic = [
    ('.html', 'text/html'),
    ('.htm', 'text/html'),
    ('.js', 'application/javascript'),
    ('.css', 'text/css'),
    ('.json', 'application/json'),
    ('.png', 'image/png'),
    ('.jpg', 'image/jpeg'),
    ('.gif', 'image/gif'),
    ('.txt', 'text/plain'),
    ('.avi', 'video/x-msvideo'),
]


# 設定画面初期化
def init_setting():
    if path.exists(settingfile):
        value = {}
        config.read(settingfile)
        if config.has_section(settingsection):
            section = config[settingsection];
            for option in settingoption:
                value[option] = section[option]
            return json.dumps(value)
        else:
            config.add_section(settingsection)
            return ''
    else:
        config.add_section(settingsection)
        return ''


# 初期設定
def exec_setting(form):
    # 設定保存
    for option in settingoption:
        config.set(settingsection, option, form[option].value)
        setting[option] = form[option].value
    with open(settingfile, 'w') as file:
        config.write(file)
    # 初期設定実行
    cmd = 'sh mon0_setup.sh {}'.format(setting['frequency'])
    print(cmd)
    result = subprocess.run(cmd, shell=True)
    return result.returncode


# 学習データ作成
def exec_learning(form):
    if setting != {}:
        # 引数取得
        time = form['learning_time'].value
        label = form['learning_label'].value
        outputpath = setting['learning_file_output']
        output = path.join(outputpath, setting['learning_file_name'])
        ap = setting['adress_ap']
        sta = setting['adress_sta']
        if not path.exists(outputpath):
             os.mkdir(outputpath)
        # 学習データ作成実行
        cmd = 'python3 demo_capture.py {} {} {} {} {}'.format(output, time, label, ap , sta)
        print(cmd)
        result = subprocess.run(cmd, shell=True)
        return result.returncode
    else:
        return 1


# モデル作成
def make_model():
    if setting != {} :
        input = path.join(setting['learning_file_output'], setting['learning_file_name'])
        outputpath = setting['model_file_ouput']
        output = path.join(outputpath, setting['model_file_name'])
        if not path.exists(outputpath):
            os.mkdir(outputpath)
        cmd = 'python3 demo_make_model.py {} {}'.format(input, output)
        print(cmd)
        result = subprocess.run(cmd, shell=True)
        return result.returncode
    else:
        return 1


# デモ実行
def exec_demo():
    if setting != {}:
        input = path.join(setting['model_file_ouput'], setting['model_file_name'])
        ap = setting['adress_ap']
        sta = setting['adress_sta']
        time = setting['measurement_time']
        cmd = 'python3 predict_demo.py {} {} {} {}'.format(input, ap, sta, time)
        print(cmd)
        result = subprocess.run(cmd, shell=True)
        return result.returncode
    else:
        return 1


# #ページ開く処理
def open_page(self, filepath):
    sendReply = False
    filename, fileext = path.splitext(filepath)
    for e in mimedic:
        if e[0] == fileext:
            mimetype = e[1]
            sendReply = True
    if sendReply:
        try:
            self.send_response(200)
            self.send_header('Content-type', mimetype)
            self.end_headers()
            f = open(path.realpath(curdir + sep + filepath), 'rb')
            data = f.read()
            self.wfile.write(bytes(data))
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


# HTTP通信
class HTTPServer_RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            global count
            global loopcount
            querypath = urlparse(self.path)
            filepath, query = querypath.path, querypath.query
            # POST されたフォームデータを解析する
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
                         })
            # 結果表示画面初期化
            if filepath.endswith('/initIndex'):
                if os.path.exists('results/snr.txt'):
                    os.remove('results/snr.txt')
                if os.path.exists('results/image.txt'):
                    os.remove('results/image.txt')
                if os.path.exists('results/accuracy.txt'):
                    os.remove('results/accuracy.txt')
                if os.path.exists('results/package.txt'):
                    os.remove('results/package.txt')
                count = 1
                loopcount = 1
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write('OK'.encode())
            # 設定画面へ遷移する
            elif filepath.endswith('/setting.html'):               
                open_page(self, 'setting.html')
            # 設定画面初期化
            elif filepath.endswith('/initSetting'):
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                responsebody = init_setting();
                self.wfile.write(responsebody.encode('UTF-8'))
            # 設定画面の設定を保存する
            elif filepath.endswith('/saveSetting'):
                self.send_response(200)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                if exec_setting(form) == 0:
                    self.wfile.write('OK'.encode())
                else :
                    self.wfile.write('・設定失敗しました。'.encode())
            # 学習データ作成処理を実行する
            elif filepath.endswith('/execLearning'):
                self.send_response(200)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                if exec_learning(form) == 0:
                    self.wfile.write('OK'.encode())
                else:
                    self.wfile.write('・学習データ作成失敗しました。'.encode())
            elif filepath.endswith('/makeModel'):
                self.send_response(200)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                if make_model() == 0:
                    self.wfile.write('OK'.encode())
                else:
                    self.wfile.write('・モデル作成失敗しました。'.encode())
            elif filepath.endswith('/execDemo'):
                self.send_response(200)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                if exec_demo() == 0:
                    self.wfile.write('OK'.encode())
                else:
                    self.wfile.write('・デモ実行失敗しました。'.encode())
            elif filepath.endswith('/updateData'):
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                looptime = max(2, int(setting['loop_time']) + 1)
                if loopcount % looptime == 0:
                    responsebody = json.dumps({'result': 'STOP'})
                    loopcount = 1
                else:
                    try:
                        responsebody = demo_display.update_data(count);
                        count += 1
                        loopcount += 1
                    except:
                        responsebody = json.dumps({'result': 'RETRY'})
                self.wfile.write(responsebody.encode('UTF-8'))
            else:
                self.send_error(404, 'File Not Found: %s' % self.path)
        except Exception:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_GET(self):
        try:
            querypath = urlparse(self.path)
            filepath, query = querypath.path, querypath.query
            if filepath.endswith('/'):
                filepath += 'index.html'
            open_page(self, filepath)
        except:
            self.send_error(404, 'File Not Found: %s' % self.path)


def run():
    port = 8000
    print('starting server, port', port)

    # Server settings
    server_address = ('', port)
    httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


if __name__ == '__main__':
    try:
        run()
    except:
        print('stop server...')
