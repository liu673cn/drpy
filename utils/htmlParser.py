#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : htmlParser.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/8/25

from pyquery import PyQuery as pq
from urllib.parse import urljoin

class jsoup:
    def __init__(self,MY_URL=''):
        self.MY_URL = MY_URL

    def pdfh(self,html,parse,pd=False):
        doc = pq(html)
        option = None
        if parse.find('&&') > -1:
            option = parse.split('&&')[1]
            parse = parse.split('&&')[0]

        ret = doc(parse)
        if option:
            if option == 'Text':
                ret = ret.text()
            elif option == 'Html':
                ret = ret.html()
            else:
                ret = ret.attr(option)
                if pd and option in ['url','src','href','data-original']:
                    ret = urljoin(self.MY_URL,ret)
        else:
            ret = ret.next()
            print(ret)
            ret = str(ret('fisrt'))
        return ret

    def pdfa(self,html,parse):
        doc = pq(html)
        # print(doc(parse)[0])
        # return [item.html() for item in doc(parse).items()]
        return [str(item) for item in doc(parse).items()]

    def pd(self,html,parse):
        return self.pdfh(html,parse,True)