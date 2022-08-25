#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : app.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/8/25

from flask import Flask, jsonify, abort,request,redirect,make_response,render_template
from js.rules import rule_list
from utils import error,parser
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False  # jsonify返回的中文正常显示
MOBILE_UA = 'Mozilla/5.0 (Linux; Android 11; M2007J3SC Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045714 Mobile Safari/537.36'
PC_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
UA = 'Mozilla/5.0'
headers = {
        'Referer': 'https://www.baidu.com',
        'user-agent': UA,
}

def getParmas(key=None):
    """
    获取链接参数
    :param key:
    :return:
    """
    args = {}
    if request.method == 'POST':
        args = request.json
    elif request.method == 'GET':
        args = request.args
    if key:
        return args.get(key,'')
    else:
        return args

@app.route('/')
def forbidden():  # put application's code here
    abort(403)

@app.route('/index')
def index():  # put application's code here
    return render_template('index.html')

@app.route('/vod')
def vod():
    rule = getParmas('rule')
    if not rule:
        return jsonify(error.failed('规则字段必填'))
    if not rule in rule_list:
        msg = f'仅支持以下规则:{",".join(rule_list)}'
        return jsonify(error.failed(msg))

    # with open(f'js/{rule}.js',mode='r',encoding='utf-8') as f:
    #     js_code = f.read()
    js_path = f'js/{rule}.js'
    ctx,js_code = parser.runJs(js_path)
    a = ctx.eval('rule')
    print(a)
    print(type(a))
    return jsonify({'rule':rule,'js_code':js_code})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000)