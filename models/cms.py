#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : cms.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/8/25
import requests

from utils.web import *
from utils.config import config
from utils.htmlParser import jsoup

class CMS:
    def __init__(self,rule):
        self.url = rule.get('url','').rstrip('/')
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
        self.filter = rule.get('filter',[])
        self.extend = rule.get('extend',[])

    def getName(self):
        return self.title

    def homeContent(self):
        # yanaifei
        # https://yanetflix.com/vodtype/dianying.html
        result = {}
        class_names = self.class_name.split('&')
        class_urls = self.class_url.split('&')
        cnt = min(len(class_urls),len(class_names))
        classes = []
        for i in range(cnt):
            classes.append({
                'type_name': class_names[i],
                'type_id': class_urls[i]
            })
        result['class'] = classes
        if self.filter:
            result['filters'] = config['filter']
        return result

    def homeVideoContent(self):
        rsp = self.fetch("https://www.genmov.com/", headers=self.header)
        root = self.html(rsp.text)
        aList = root.xpath("//div[@class='module module-wrapper']//div[@class='module-item']")
        videos = []
        for a in aList:
            name = a.xpath(".//div[@class='module-item-pic']/a/@title")[0]
            pic = a.xpath(".//div[@class='module-item-pic']/img/@data-src")[0]
            mark = a.xpath("./div[@class='module-item-text']/text()")[0]
            sid = a.xpath(".//div[@class='module-item-pic']/a/@href")[0]
            sid = self.regStr(sid, "/video/(\\S+).html")
            videos.append({
                "vod_id": sid,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks": mark
            })
        result = {
            'list': videos
        }
        return result

    def categoryContent(self, fyclass, fypage):
        """
        一级带分类的数据返回
        :param fyclass: 分类标识
        :param fypage: 页码
        :return: cms一级数据
        """

        result = {}
        # urlParams = ["", "", "", "", "", "", "", "", "", "", "", ""]
        # urlParams = [""] * 12
        # urlParams[0] = tid
        # urlParams[8] = str(pg)
        # for key in self.extend:
        #     urlParams[int(key)] = self.extend[key]
        # params = '-'.join(urlParams)
        # print(params)
        # url = self.url + '/{0}.html'.format(params)
        pg = str(fypage)
        url = self.url.replace('fyclass',fyclass).replace('fypage',fypage)
        print(url)
        headers = {'user-agent': self.ua}
        r = requests.get(url, headers=headers)
        p = self.一级.split(';')  # 解析
        jsp = jsoup(self.url)
        pdfh = jsp.pdfh
        pdfa = jsp.pdfa
        pd = jsp.pd

        items = pdfa(r.text, p[0])
        videos = []
        for item in items:
            # print(item)
            title = pdfh(item, p[1])
            img = pd(item, p[2])
            desc = pdfh(item, p[3])
            link = pd(item, p[4])
            content = ''
            # sid = self.regStr(sid, "/video/(\\S+).html")
            videos.append({
                "vod_id": link,
                "vod_name": title,
                "vod_pic": img,
                "vod_remarks": desc,
                "vod_content": content,
            })
        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

if __name__ == '__main__':
    from utils import parser
    js_path = f'js/鸭奈飞.js'
    ctx, js_code = parser.runJs(js_path)
    rule = ctx.eval('rule')
    cms = CMS(rule)
    print(cms.title)
    print(cms.homeContent())
    cms.categoryContent('dianying',1)