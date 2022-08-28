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
# PLAY_URL = 'http://localhost:5705' # 匹配远程解析服务器链接
# PLAY_URL = PLAY_URL.rstrip('/')
PLAY_DISABLE = False  # 全局禁用播放解析