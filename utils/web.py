#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : web.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/9/6
import os

from flask import request,jsonify
import hashlib
from time import time
# from utils.cfg import cfg
from controllers.service import storage_service

MOBILE_UA = 'Mozilla/5.0 (Linux; Android 11; M2007J3SC Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045714 Mobile Safari/537.36'
PC_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
UA = 'Mozilla/5.0'
UC_UA = 'Mozilla/5.0 (Linux; U; Android 9; zh-CN; MI 9 Build/PKQ1.181121.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.5.1035 Mobile Safari/537.36'
IOS_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
headers = {
        'Referer': 'https://www.baidu.com',
        'user-agent': UA,
}

def getParmas(key=None,value=''):
    """
    获取链接参数
    :param key:
    :return:
    """
    content_type = request.headers.get('Content-Type')
    args = {}
    if request.method == 'POST':
        if 'application/x-www-form-urlencoded' in content_type or 'multipart/form-data' in content_type:
            args = request.form
        elif 'application/json' in content_type:
            args = request.json
        elif 'text/plain' in content_type:
            args = request.data
        else:
            args = request.args
    elif request.method == 'GET':
        args = request.args
    if key:
        return args.get(key,value)
    else:
        return args

def layuiBack(msg:str, data=None,code:int=0,count:int=0):
    if data is None:
        data = []
    return jsonify({
        'msg':msg,
        'code':code,
        'data':data,
        'count':count or len(data)
    })

def md5(str):
    return hashlib.md5(str.encode(encoding='UTF-8')).hexdigest()

def verfy_token(token=None):
    if not token:
        cookies = request.cookies
        token = cookies.get('token', '')
    if not token or len(str(token)) != 32:
        return False
    lsg = storage_service()
    # username = cfg.get('UNAME','')
    username = lsg.getItem('UNAME','')
    # pwd = cfg.get('PWD','')
    pwd = lsg.getItem('PWD','')
    ctoken = md5(f'{username};{pwd}')
    # print(f'username:{username},pwd:{pwd},current_token:{ctoken},input_token:{ctoken}')
    if token != ctoken:
        return False
    return True

def get_interval(t):
    interval = time() - t
    interval = round(interval*1000,2)
    return interval

def getHeaders(url):
    headers = {}
    if url:
        headers["Referer"] = url
    headers["User-Agent"] = UA
    # headers.setdefault("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
    # headers.setdefault("Accept-Language", "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2")
    return headers