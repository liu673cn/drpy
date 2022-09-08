#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : files.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/9/6

import os
from utils.system import getHost
from utils.encode import base64Encode
from controllers.service import storage_service

def getPics(path='images'):
    base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))  # 上级目录
    img_path = os.path.join(base_path, f'{path}')
    os.makedirs(img_path,exist_ok=True)
    file_name = os.listdir(img_path)
    # file_name = list(filter(lambda x: str(x).endswith('.js') and str(x).find('模板') < 0, file_name))
    # print(file_name)
    pic_list = [base_path+file for file in file_name]
    # pic_list = file_name
    # print(type(pic_list))
    return pic_list

def get_live_url(new_conf,mode):
    host = getHost(mode)
    lsg = storage_service()
    # t1 = time()
    live_url = host + '/lives' if new_conf.get('LIVE_MODE',1) == 0 else lsg.getItem('LIVE_URL',getHost(2)+'/lives')
    live_url = base64Encode(live_url)
    # print(f'{get_interval(t1)}毫秒')
    return live_url

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

def custom_merge(original:dict,custom:dict):
    """
    合并用户配置
    :param original: 原始配置
    :param custom: 自定义配置
    :return:
    """
    if not custom or len(custom.keys()) < 1:
        return original
    new_keys = custom.keys()
    updateObj = {}
    extend_obj = {}
    for key in ['wallpaper','spider','homepage','lives']:
        if key in new_keys:
            updateObj[key] = custom[key]

    for key in ['drives','sites','flags','ads']:
        if key in new_keys:
            extend_obj[key] = custom[key]

    original.update(updateObj)
    for key in extend_obj.keys():
        original[key].extend(extend_obj[key])
    return original