#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : 干饭.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/8/28

import requests
import re
import json
from urllib.parse import urljoin,quote,unquote
import base64

def lazyParse(input,jsp,getParse,saveParse,headers,encoding):
    cacheUrl = getParse(input)
    print(f'cacheUrl:{cacheUrl}')
    if cacheUrl:
        return cacheUrl
    r = requests.get(input, headers=headers)
    r.encoding = encoding
    html = r.text
    # print(html)
    # js = jsp.pdfh(html,'.stui-player__video script:eq(0)&&Html')
    # print(js)
    try:
        ret = re.search('var player_(.*?)=(.*?)<', html, re.M | re.I).groups()[1]
        ret = json.loads(ret)
        url = ret.get('url','')
        if len(url) > 10:
            real_url = 'https://player.buyaotou.xyz/?url='+url
            saveParse(input,real_url)
            return real_url
        else:
            return input
    except Exception as e:
        print(f'错误:{e}')
    return input