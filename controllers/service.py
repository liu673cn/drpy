#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : service.py.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/9/6

from base.R import copy_utils
from models.storage import Storage
from utils.cfg import cfg

class storage_service(object):

    @staticmethod
    def query_all():
        # 查询所有
        res = Storage.query.all()
        return copy_utils.obj_to_list(res)

    def __init__(self):
        conf_list = ['LIVE_URL', 'USE_PY', 'PLAY_URL', 'PLAY_DISABLE', 'LAZYPARSE_MODE', 'WALL_PAPER_ENABLE',
                     'WALL_PAPER', 'UNAME', 'PWD', 'LIVE_MODE', 'CATE_EXCLUDE', 'TAB_EXCLUDE','SEARCH_TIMEOUT','MULTI_MODE','ALI_TOKEN']
        for conf in conf_list:
            if not self.hasItem(conf):
                print(f'开始初始化{conf}')
                self.setItem(conf, cfg.get(conf))

    @classmethod
    def getStoreConf(self):
        # MAX_CONTENT_LENGTH 最大上传和端口ip一样是顶级配置,无法外部修改的
        conf_list = ['LIVE_URL', 'LIVE_MODE','PLAY_URL', 'PID_URL','USE_PY', 'PLAY_DISABLE', 'LAZYPARSE_MODE', 'WALL_PAPER_ENABLE',
                     'WALL_PAPER', 'UNAME', 'PWD',  'CATE_EXCLUDE', 'TAB_EXCLUDE','SEARCH_TIMEOUT','MULTI_MODE','ALI_TOKEN']
        conf_name_list = ['直播地址', '直播模式','远程地址', '进程管理链接','启用py源', '禁用免嗅', '免嗅模式', '启用壁纸', '壁纸链接', '管理账号',
                          '管理密码',  '分类排除', '线路排除','聚搜超时','多源模式','阿里tk']
        conf_lists = []
        for i in range(len(conf_list)):
            conf = conf_list[i]
            conf_lists.append({
                'key': conf,
                'value': self.getItem(conf),
                'name': conf_name_list[i]
            })
        return conf_lists

    @classmethod
    def getStoreConfDict(self):
        store_conf = self.getStoreConf()
        store_conf_dict = {}
        for stc in store_conf:
            store_conf_dict[stc['key']] = stc['value']
        return store_conf_dict

    @classmethod
    def getItem(self, key, value=''):
        res = Storage.getItem(key,value)
        if str(res) == '0' or str(res) == 'false' or str(res) == 'False':
            return 0
        return res

    @classmethod
    def hasItem(self, key):
        return Storage.hasItem(key)

    @classmethod
    def setItem(self,key, value):
        return Storage.setItem(key, value)

    @classmethod
    def clearItem(self,key):
        return Storage.clearItem(key)