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

def runJs(jsPath,before='',after=''):
    # base_path = os.path.dirname(os.path.abspath(__file__)) # 当前文件所在目录
    # base_path = os.path.dirname(os.getcwd()) # 当前主程序所在工作目录
    # base_path = os.path.dirname(os.path.abspath('.')) # 上级目录
    # js_code = 'var rule={}'
    base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))  # 上级目录
    if str(jsPath).startswith('http'):
        js_name = jsPath.split('/')[-1]
        cache_path = os.path.join(base_path, f'cache/{js_name}')
        print('远程规则:',js_name)
        if not os.path.exists(cache_path):
            try:
                js_code = requests.get(jsPath,timeout=2).text
                with open(cache_path,mode='w+',encoding='utf-8') as f:
                    f.write(js_code)
            except Exception as e:
                print('发生了错误:',e)
                return None, ''
        else:
            with open(cache_path, 'r', encoding='UTF-8') as fp:
                js_code = fp.read()
    else:
        js_path = os.path.join(base_path, jsPath)
        with open(js_path, 'r', encoding='UTF-8') as fp:
            js_code = fp.read()
    # print(js_code)
    jscode_to_run = js_code
    if before:
        jscode_to_run = before + jscode_to_run
    if after:
        jscode_to_run += after
    loader = execjs.compile(jscode_to_run)
    return loader,js_code

def toJs(jsPath):
    base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) # 上级目录
    js_path = os.path.join(base_path, f'cache/{jsPath}')
    print(js_path)
    if not os.path.exists(js_path):
        return jsonify({'code': -2, 'msg': f'非法猥亵,文件不存在'})
    with open(js_path, 'r', encoding='UTF-8') as fp:
        js = fp.read()
    response = make_response(js)
    response.headers['Content-Type'] = 'text/javascript; charset=utf-8'
    return response

def toHtml(jsPath):
    base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) # 上级目录
    js_path = os.path.join(base_path, f'cache/{jsPath}')
    with open(js_path, 'r', encoding='UTF-8') as fp:
        js = fp.read()
    response = make_response(js)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

def runPy(pyPath):
    # base_path = os.path.dirname(os.path.abspath(__file__)) # 当前文件所在目录
    # base_path = os.path.dirname(os.getcwd()) # 当前主程序所在工作目录
    # base_path = os.path.dirname(os.path.abspath('.')) # 上级目录
    # js_code = 'var rule={}'
    if pyPath and not str(pyPath).endswith('.py'):
        pyPath += '.py'
    base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))  # 上级目录
    if str(pyPath).startswith('http'):
        py_name = pyPath.split('/')[-1]
        cache_path = os.path.join(base_path, f'cache/{py_name}')
        print('远程免嗅:',py_name)
        if not os.path.exists(cache_path):
            try:
                py_code = requests.get(pyPath,timeout=2).text
                with open(cache_path,mode='w+',encoding='utf-8') as f:
                    f.write(py_code)
            except Exception as e:
                print('发生了错误:',e)
                return None, ''
        else:
            with open(cache_path, 'r', encoding='UTF-8') as fp:
                py_code = fp.read()
    else:
        py_root = os.path.join(base_path, 'py/')
        os.makedirs(py_root,exist_ok=True)
        py_path = os.path.join(py_root, pyPath)
        if not os.path.exists(py_path):
            return ''
        with open(py_path, 'r', encoding='UTF-8') as fp:
            py_code = fp.read()
    # print(js_code)
    return py_code