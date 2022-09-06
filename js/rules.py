#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : rules.py.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/8/25

import os
from time import time
import js2py
from utils.log import logger
from utils.web import get_interval,UA

def getRuleLists():
    base_path = os.path.dirname(os.path.abspath(__file__)) # 当前文件所在目录
    # print(base_path)
    file_name = os.listdir(base_path)
    file_name = list(filter(lambda x:str(x).endswith('.js') and str(x).find('模板') < 0,file_name))
    # print(file_name)
    rule_list = [file.replace('.js','') for file in file_name]
    # print(rule_list)
    return rule_list

def getRules(path='cache'):
    t1 = time()
    base_path = path+'/'  # 当前文件所在目录
    # print(base_path)
    os.makedirs(base_path,exist_ok=True)
    file_name = os.listdir(base_path)
    file_name = list(filter(lambda x: str(x).endswith('.js') and str(x).find('模板') < 0, file_name))
    # print(file_name)
    rule_list = [file.replace('.js', '') for file in file_name]
    js_path = [f'{path}/{rule}.js' for rule in rule_list]
    with open('js/模板.js', encoding='utf-8') as f:
        before = f.read()
    rule_codes = []
    # for js in js_path:
    #     with open(js,encoding='utf-8') as f:
    #         code = f.read()
    #         rule_codes.append(js2py.eval_js(before+code))

    ctx = js2py.EvalJs()
    codes = []
    for i in range(len(js_path)):
        js = js_path[i]
        with open(js,encoding='utf-8') as f:
            code = f.read()
            codes.append(code.replace('rule',f'rule{i}',1))
    newCodes = before + '\n'+ '\n'.join(codes)
    # print(newCodes)
    ctx.execute(newCodes)
    for i in range(len(js_path)):
        rule_codes.append(ctx.eval(f'rule{i}'))

    # print(rule_codes)
    # print(type(rule_codes[0]),rule_codes[0])
    # print(rule_codes[0].title)
    # print(rule_codes[0].searchable)
    # print(rule_codes[0].quickSearch)
    new_rule_list = []
    for i in range(len(rule_list)):
        new_rule_list.append({
            'name':rule_list[i],
            'searchable':rule_codes[i].searchable or 0,
            'quickSearch':rule_codes[i].quickSearch or 0,
            'filterable':rule_codes[i].filterable or 0,
        })
    # print(new_rule_list)
    rules = {'list': new_rule_list, 'count': len(rule_list)}
    logger.info(f'自动配置装载耗时:{get_interval(t1)}毫秒')
    return rules

def getJxs(path='js'):
    with open(f'{path}/解析.conf',encoding='utf-8') as f:
        data = f.read().strip()
    jxs = []
    for i in data.split('\n'):
        i = i.strip()
        dt = i.split(',')
        if not i.startswith('#'):
            jxs.append({
                'name':dt[0],
                'url':dt[1],
                'type':dt[2] if len(dt) > 2 else 0,
                'ua':dt[3] if len(dt) > 3 else UA,
            })
    # jxs = [{'name':dt.split(',')[0],'url':dt.split(',')[1]} for dt in data.split('\n')]
    # jxs = list(filter(lambda x:not str(x['name']).strip().startswith('#'),jxs))
    # print(jxs)
    print(f'共计{len(jxs)}条解析')
    return jxs

if __name__ == '__main__':
    print(getRuleLists())