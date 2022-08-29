#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : web.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/8/25

import socket
from werkzeug.utils import import_string
from netifaces import interfaces, ifaddresses, AF_INET
from flask import request
from utils.log import logger
MOBILE_UA = 'Mozilla/5.0 (Linux; Android 11; M2007J3SC Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045714 Mobile Safari/537.36'
PC_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
UA = 'Mozilla/5.0'
UC_UA = 'Mozilla/5.0 (Linux; U; Android 9; zh-CN; MI 9 Build/PKQ1.181121.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.5.1035 Mobile Safari/537.36'
headers = {
        'Referer': 'https://www.baidu.com',
        'user-agent': UA,
}
from time import time

def get_host_ip2(): # 获取局域网ip
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # print('8888')
        s.connect(('8.8.8.8', 80))  # 114.114.114.114也是dns地址
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def get_host_ip(): # 获取局域网ip
    ips = []
    for ifaceName in interfaces():
        addresses = ''.join([i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr': ''}])])
        ips.append(addresses)
    real_ips = list(filter(lambda x:x and x!='127.0.0.1',ips))
    # logger.info(real_ips)
    jyw = list(filter(lambda x:str(x).startswith('192.168'),real_ips))
    return real_ips[-1] if len(jyw) < 1 else jyw[0]

def getHost(mode=0,port=None):
    port = port or request.environ.get('SERVER_PORT')
    # hostname = socket.gethostname()
    # ip = socket.gethostbyname(hostname)
    # ip = request.remote_addr
    # print(ip)
    # mode 为0是本地,1是局域网 2是线上
    if mode == 0:
        host = f'localhost:{port}'
    elif mode == 1:
        REAL_IP = get_host_ip()
        ip = REAL_IP
        host = f'{ip}:{port}'
    else:
        host = 'cms.nokia.press'
    return host

def get_conf(obj):
    new_conf = {}
    if isinstance(obj, str):
        config = import_string(obj)
    for key in dir(obj):
        if key.isupper():
            new_conf[key] = getattr(obj, key)
    # print(new_conf)
    return new_conf

def get_interval(t):
    interval = time() - t
    interval = round(interval*1000,2)
    return interval