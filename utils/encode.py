#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : encode.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/8/29

import base64
import requests
from utils.web import UC_UA

def base64Encode(text):
    return base64.b64encode(text.encode("utf8")).decode("utf-8") #base64编码

def baseDecode(text):
    return base64.b64decode(text).decode("utf-8") #base64解码

def dealObj(obj):
    encoding = obj.get('encoding') or 'utf-8'
    encoding = str(encoding).replace("'", "")
    # print(type(url),url)
    # headers = dict(obj.get('headers')) if obj.get('headers') else {}
    # headers = obj.get('headers').to_dict() if obj.get('headers') else {}
    headers = obj.get('headers') if obj.get('headers') else {}
    new_headers = {}
    # print(type(headers),headers)
    for i in headers:
        new_headers[str(i).replace("'", "")] = str(headers[i]).replace("'", "")
    # print(type(new_headers), new_headers)

    timeout = float(obj.get('timeout').to_int()) if obj.get('timeout') else None
    # print(type(timeout), timeout)
    body = obj.get('body') if obj.get('body') else {}
    new_body = {}
    for i in body:
        new_body[str(i).replace("'", "")] = str(body[i]).replace("'", "")
    return {
        'encoding':encoding,
        'headers':new_headers,
        'timeout':timeout,
        'body': new_body,
    }

def base_request(url,obj,method=None):
    url = str(url).replace("'", "")
    if not method:
        method = 'get'
    # print(obj)
    try:
        # r = requests.get(url, headers=headers, params=body, timeout=timeout)
        if method.lower() == 'get':
            r = requests.get(url, headers=obj['headers'], params=obj['body'], timeout=obj['timeout'])
        else:
            r = requests.post(url, headers=obj['headers'], data=obj['body'], timeout=obj['timeout'])
        # r = requests.get(url, timeout=timeout)
        # r = requests.get(url)
        # print(encoding)
        r.encoding = obj['encoding']
        # print(f'源码:{r.text}')
        return r.text
    except Exception as e:
        print(f'{method}请求发生错误:{e}')
        return ''

def fetch(url,obj,method=None):
    if not method:
        method = 'get'
    obj = dealObj(obj)
    print(method)
    return base_request(url,obj,method)

def post(url,obj):
    obj = dealObj(obj)
    return base_request(url,obj,'post')

def request(url,obj,method=None):
    if not method:
        method = 'get'
    obj = dealObj(obj)
    if not obj.get('headers') or not obj['headers'].get('User-Agent'):
        obj['headers']['User-Agent'] = UC_UA

    return base_request(url, obj, method)