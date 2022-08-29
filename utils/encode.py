#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : encode.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/8/29

import base64
import requests

def base64Encode(text):
    return base64.b64encode(text.encode("utf8")).decode("utf-8") #base64编码

def baseDecode(text):
    return base64.b64decode(text).decode("utf-8") #base64解码

def base_request(url,obj,method='get'):
    url = str(url).replace("'", "")
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
    # print(type(new_body), new_body)
    try:
        # r = requests.get(url, headers=headers, params=body, timeout=timeout)
        if method.lower() == 'get':
            r = requests.get(url, headers=new_headers, params=new_body, timeout=timeout)
        else:
            r = requests.post(url, headers=new_headers, data=new_body, timeout=timeout)
        # r = requests.get(url, timeout=timeout)
        # r = requests.get(url)
        # print(encoding)
        r.encoding = encoding
        # print(f'源码:{r.text}')
        return r.text
    except Exception as e:
        print(f'{method}请求发生错误:{e}')
        return ''

def fetch(url,obj):
    return base_request(url,obj)

def post(url,obj):
    return base_request(url,obj,'post')