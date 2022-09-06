#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : service.py.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/9/6

from base.R import copy_utils
from models.storage import Storage
from utils.system import cfg

class storage_service(object):

    @staticmethod
    def query_all():
        # 查询所有
        res = Storage.query.all()
        return copy_utils.obj_to_list(res)

    def __init__(self):
        if not self.getItem('LIVE_URL'):
            print('开始初始化lsg')
            self.setItem('LIVE_URL', cfg.get('LIVE_URL'))

    @classmethod
    def getItem(self, key, value=''):
        return Storage.getItem(key,value)

    @classmethod
    def setItem(self,key, value):
        return Storage.setItem(key, value)

    @classmethod
    def clearItem(self,key):
        return Storage.clearItem(key)