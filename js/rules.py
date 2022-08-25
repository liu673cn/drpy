#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : rules.py.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/8/25

import os

def getRules():
    base_path = os.path.dirname(os.path.abspath(__file__)) # 当前文件所在目录
    # print(base_path)
    file_name = os.listdir(base_path)
    file_name = list(filter(lambda x:str(x).endswith('.js'),file_name))
    # print(file_name)
    rule_list = [file.replace('.js','') for file in file_name]
    # print(rule_list)
    return rule_list

if __name__ == '__main__':
    print(getRules())