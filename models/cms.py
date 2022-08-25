#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : cms.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/8/25
from utils.web import *

class CMS:
    def __init__(self,rule):
        self.url = rule.get('url','')
        self.searchUrl = rule.get('searchUrl','')
        ua = rule.get('ua','')
        if ua == 'MOBILE_UA':
            self.ua = MOBILE_UA
        elif ua == 'PC_UA':
            self.ua = PC_UA
        else:
            self.ua = UA
        self.searchUrl = rule.get('searchUrl','')
        self.class_name = rule.get('class_name','')
        self.class_url = rule.get('class_url','')
        self.一级 = rule.get('一级','')
        self.二级 = rule.get('二级','')
        self.搜索 = rule.get('搜索','')
        self.title = rule.get('title','')

    def getName(self):
        return self.title

if __name__ == '__main__':
    from utils import parser
    js_path = f'js/鸭奈飞.js'
    ctx, js_code = parser.runJs(js_path)
    rule = ctx.eval('rule')
    cms = CMS(rule)
    print(cms.title)