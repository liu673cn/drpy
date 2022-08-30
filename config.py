#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : config.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/8/27

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'gp'
PASSWORD = '123456'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'pira'
# DB_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
DB_URI = 'sqlite:///models/rules.db?charset=utf8&check_same_thread=False'
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False # 打印sql语句
JSON_AS_ASCII = False # jsonify返回的中文正常显示
PLAY_URL = 'http://cms.nokia.press' # 匹配远程解析服务器链接 远程接口主页地址，后面不能有/
PLAY_URL = PLAY_URL.rstrip('/')
PLAY_DISABLE = False  # 全局禁用播放解析
LAZYPARSE_MODE = 1  # 播放解析模式(0 本地 1 局域网 2远程 仅在全局禁用为False的时候生效)
WALL_PAPER_ENABLE = True  # 启用自定义壁纸
WALL_PAPER = "https://picsum.photos/1280/720/?blur=10"  # 自定义壁纸,可注释
SUP_PORT = 9001  # supervisord 服务端口
RETRY_CNT = 3 # 验证码重试次数
# OCR_API = 'http://192.168.3.224:9000/api/ocr_img' # 验证码识别接口,传参数data
OCR_API = 'http://dm.mudery.com:10000' # 验证码识别接口,传参数data
# {% if config.WALL_PAPER %}"wallpaper":"{{ config.WALL_PAPER }}",{% endif %}