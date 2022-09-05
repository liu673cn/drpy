#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : update.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/9/6
from time import time as getTime

import requests
import os
import zipfile
import shutil # https://blog.csdn.net/weixin_33130113/article/details/112336581
from utils.log import logger
from utils.web import get_interval

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
        r = requests.get('https://gitcode.net/qq_32394351/dr_py/-/raw/master/js/version.txt',timeout=(2,2))
        ver = r.text
    except Exception as e:
        # print(f'{e}')
        logger.info(f'{e}')
    return ver

def checkUpdate():
    local_ver = getLocalVer()
    online_ver = getOnlineVer()
    if local_ver != online_ver:
        return True
    return False


def del_file(filepath):
    """
    删除execl目录下的所有文件或文件夹
    :param filepath: 路径
    :return:
    """
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)

def force_copy_files(from_path,to_path):
    # print(f'开始拷贝文件{from_path}=>{to_path}')
    logger.info(f'开始拷贝文件{from_path}=>{to_path}')
    shutil.copytree(from_path, to_path, dirs_exist_ok=True)

def copy_to_update():
    base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))  # 上级目录
    tmp_path = os.path.join(base_path, f'tmp')
    dr_path = os.path.join(tmp_path, f'dr_py-master')
    if not os.path.exists(dr_path):
        # print(f'升级失败,找不到目录{dr_path}')
        logger.info(f'升级失败,找不到目录{dr_path}')
        return False
    force_copy_files(os.path.join(dr_path, f'js'),os.path.join(base_path, f'js'))
    force_copy_files(os.path.join(dr_path, f'classes'),os.path.join(base_path, f'classes'))
    force_copy_files(os.path.join(dr_path, f'templates'),os.path.join(base_path, f'templates'))
    force_copy_files(os.path.join(dr_path, f'utils'),os.path.join(base_path, f'utils'))
    return True

def download_new_version():
    t1 = getTime()
    base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))  # 上级目录
    tmp_path = os.path.join(base_path, f'tmp')
    os.makedirs(tmp_path,exist_ok=True)
    url = 'https://gitcode.net/qq_32394351/dr_py/-/archive/master/dr_py-master.zip'
    # tmp_files = os.listdir(tmp_path)
    # for tp in tmp_files:
    #     print(f'清除缓存文件:{tp}')
    #     os.remove(os.path.join(tmp_path, tp))
    del_file(tmp_path)
    headers = {
        'Referer': 'https://gitcode.net/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
    }
    msg = ''
    try:
        # print(f'开始下载:{url}')
        logger.info(f'开始下载:{url}')
        r = requests.get(url,headers=headers,timeout=(20,20))
        rb = r.content
        download_path = os.path.join(tmp_path, 'dr_py.zip')
        with open(download_path,mode='wb+') as f:
            f.write(rb)
        # print(f'开始解压文件:{download_path}')
        logger.info(f'开始解压文件:{download_path}')
        f = zipfile.ZipFile(download_path, 'r')  # 压缩文件位置
        for file in f.namelist():
            f.extract(file, tmp_path)  # 解压位置
        f.close()
        # print('解压完毕,开始升级')
        logger.info('解压完毕,开始升级')
        ret = copy_to_update()
        logger.info(f'升级完毕,结果为:{ret}')
        # print(f'升级完毕,结果为:{ret}')
        msg = '升级成功'
    except Exception as e:
        msg = f'升级失败:{e}'
    logger.info(f'参数检验js读取共计耗时:{get_interval(t1)}毫秒')
    return msg