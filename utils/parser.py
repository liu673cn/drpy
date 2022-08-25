#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : parser.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/8/25

import os

import requests
from flask import make_response,jsonify
from functools import partial  # 这玩意儿能锁定一个函数的参数
import subprocess
subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")  # 固定写法
# 解决execjs执行js时产生的乱码报错，需要在导入该模块之前，让Popen的encoding参数锁定为utf-8
import execjs

# os.environ["EXECJS_RUNTIME"] = "JScript"
# print(execjs.get().name)

def runJs(jsPath):
    # base_path = os.path.dirname(os.path.abspath(__file__)) # 当前文件所在目录
    # base_path = os.path.dirname(os.getcwd()) # 当前主程序所在工作目录
    # base_path = os.path.dirname(os.path.abspath('.')) # 上级目录
    if str(jsPath).startswith('http'):
        jscode = requests.get(jsPath).text
    else:
        base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) # 上级目录
        js_path = os.path.join(base_path, jsPath)
        with open(js_path, 'r', encoding='UTF-8') as fp:
            js_code = fp.read()
    # print(js_code)
    loader = execjs.compile(js_code)
    return loader,js_code

def toJs(jsPath):
    base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) # 上级目录
    js_path = os.path.join(base_path, jsPath)
    if not os.path.exists(js_path):
        return jsonify({'code': -2, 'msg': f'非法猥亵,文件不存在'})
    with open(js_path, 'r', encoding='UTF-8') as fp:
        js = fp.read()
    response = make_response(js)
    response.headers['Content-Type'] = 'text/javascript; charset=utf-8'
    return response

def toHtml(jsPath):
    base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) # 上级目录
    js_path = os.path.join(base_path, jsPath)
    with open(js_path, 'r', encoding='UTF-8') as fp:
        js = fp.read()
    response = make_response(js)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response
