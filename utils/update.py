#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : update.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/9/6

import requests
import os

def getLocalVer():
    base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))  # 上级目录
    version_path = os.path.join(base_path, f'js/version.txt')
    if not os.path.exists(version_path):
        with open(version_path,mode='w+',encoding='utf-8') as f:
            version = '1.0.0'
            f.write(version)
    else:
        with open(version_path,encoding='utf-8') as f:
            version = f.read()
    return version

def getOnlineVer():
    ver = '1.0.1'
    try:
        r = requests.get('',timeout=(2,2))
        ver = r.text
    except Exception as e:
        print(f'{e}')
    return ver