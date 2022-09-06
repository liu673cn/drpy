#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : web.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/8/25
import os
import socket
import hashlib
from werkzeug.utils import import_string
import psutil
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
import config as settings

def get_host_ip2(): # 获取局域网ip
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # print('8888')
        s.connect(('8.8.8.8', 80))  # 114.114.114.114也是dns地址
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def get_host_ip_old(): # 获取局域网ip
    from netifaces import interfaces, ifaddresses, AF_INET
    ips = []
    for ifaceName in interfaces():
        addresses = ''.join([i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr': ''}])])
        ips.append(addresses)
    real_ips = list(filter(lambda x:x and x!='127.0.0.1',ips))
    # logger.info(real_ips)
    jyw = list(filter(lambda x:str(x).startswith('192.168'),real_ips))
    return real_ips[-1] if len(jyw) < 1 else jyw[0]

def get_host_ip(): # 获取局域网ip
    netcard_info,ips = get_wlan_info()
    # print(netcard_info)
    real_ips = list(filter(lambda x: x and x != '127.0.0.1', ips))
    jyw = list(filter(lambda x: str(x).startswith('192.168'), real_ips))
    return real_ips[-1] if len(jyw) < 1 else jyw[0]

def get_wlan_info():
    info = psutil.net_if_addrs()
    # print(info)
    netcard_info = []
    ips = []
    for k, v in info.items():
        for item in v:
            if item[0] == 2:
                netcard_info.append((k, item[1]))
                ips.append(item[1])
    return netcard_info,ips

def getHost(mode=0,port=None):
    port = port or request.environ.get('SERVER_PORT')
    # hostname = socket.gethostname()
    # ip = socket.gethostbyname(hostname)
    # ip = request.remote_addr
    # print(ip)
    # mode 为0是本地,1是局域网 2是线上
    if mode == 0:
        host = f'http://localhost:{port}'
    elif mode == 1:
        REAL_IP = get_host_ip()
        ip = REAL_IP
        host = f'http://{ip}:{port}'
    else:
        host = get_conf(settings).get('PLAY_URL','http://cms.nokia.press')
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

def md5(str):
    return hashlib.md5(str.encode(encoding='UTF-8')).hexdigest()

def verfy_token(token=''):
    if not token or len(str(token))!=32:
        return False
    cfg = get_conf(settings)
    username = cfg.get('UNAME','')
    pwd = cfg.get('PWD','')
    ctoken = md5(f'{username};{pwd}')
    # print(f'username:{username},pwd:{pwd},current_token:{ctoken},input_token:{ctoken}')
    if token != ctoken:
        return False
    return True

def getHeaders(url):
    headers = {}
    if url:
        headers.setdefault("Referer", url)
    headers.setdefault("User-Agent", PC_UA)
    headers.setdefault("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
    headers.setdefault("Accept-Language", "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2")
    return headers

def getAlist():
    base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))  # 上级目录
    alist_path = os.path.join(base_path, 'js/alist.conf')
    with open(alist_path,encoding='utf-8') as f:
        data = f.read().strip()
    alists = []
    for i in data.split('\n'):
        i = i.strip()
        dt = i.split(',')
        if not i.strip().startswith('#'):
            obj = {
                'name': dt[0],
                'server': dt[1],
                'type':"alist",
            }
            if len(dt) > 2:
                obj.update({
                    'password': dt[2]
                })
            alists.append(obj)
    print(f'共计{len(alists)}条alist记录')
    return alists