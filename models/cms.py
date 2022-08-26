#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : cms.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/8/25
import requests

from utils.web import *
from utils.config import config
from utils.htmlParser import jsoup
from urllib.parse import urljoin

class CMS:
    def __init__(self,rule):
        self.url = rule.get('url','').rstrip('/')
        self.detailUrl = rule.get('detailUrl','').rstrip('/')
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
        self.class_parse = rule.get('class_parse','')
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
        result = {
            'list': []
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
        url = self.url.replace('fyclass',fyclass).replace('fypage',pg)
        print(url)
        headers = {'user-agent': self.ua}
        r = requests.get(url, headers=headers)
        p = self.一级.split(';')  # 解析
        jsp = jsoup(self.url)
        pdfh = jsp.pdfh
        pdfa = jsp.pdfa
        pd = jsp.pd
        # print(pdfh(r.text,'body a.module-poster-item.module-item:eq(1)&&Text'))
        # print(pdfh(r.text,'body a.module-poster-item.module-item:eq(0)'))
        # print(pdfh(r.text,'body a.module-poster-item.module-item:first'))
        items = pdfa(r.text, p[0])
        videos = []
        for item in items:
            # print(item)
            title = pdfh(item, p[1])
            img = pd(item, p[2])
            desc = pdfh(item, p[3])
            link = pd(item, p[4])
            content = '' if len(p) < 6 else pdfh(item, p[5])
            # sid = self.regStr(sid, "/video/(\\S+).html")
            videos.append({
                "vod_id": link,
                "vod_name": title,
                "vod_pic": img,
                "vod_remarks": desc,
                "vod_content": content,
            })
        result['list'] = videos
        result['page'] = fypage
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def detailContent(self, array):
        """
        cms二级数据
        :param array:
        :return:
        """
        # video-info-header
        fyid = str(array[0])
        if not fyid.startswith('http'):
            url = self.detailUrl.replace('fyid', fyid)
        else:
            url = fyid
        print(url)
        headers = {'user-agent': self.ua}
        r = requests.get(url, headers=headers)
        html = r.text
        # print(html)
        p = self.二级  # 解析
        jsp = jsoup(self.url)
        pdfh = jsp.pdfh
        pdfa = jsp.pdfa
        pd = jsp.pd
        pq = jsp.pq
        obj = {}
        vod_name = ''
        if p.get('title'):
            p1 = p['title'].split(';')
            vod_name = pdfh(html,p1[0]).replace('\n',' ')
            title = '\n'.join([pdfh(html,i).replace('\n',' ') for i in p1])
            # print(title)
            obj['title'] = title
        if p.get('desc'):
            p1 = p['desc'].split(';')
            desc = '\n'.join([pdfh(html,i).replace('\n',' ') for i in p1])
            obj['desc'] = desc

        if p.get('content'):
            p1 = p['content'].split(';')
            content = '\n'.join([pdfh(html,i).replace('\n',' ') for i in p1])
            obj['content'] = content

        if p.get('img'):
            p1 = p['img'].split(';')
            img = '\n'.join([pdfh(html,i).replace('\n',' ') for i in p1])
            obj['img'] = img

        vod = {
            "vod_id": fyid,
            "vod_name": vod_name,
            "vod_pic": obj.get('img',''),
            "type_name": obj.get('title',''),
            "vod_year": "",
            "vod_area": "",
            "vod_remarks": obj.get('desc',''),
            "vod_actor": "",
            "vod_director": "",
            "vod_content": obj.get('content','')
        }

        vod_play_from = '$$$'
        playFrom = []
        if p.get('tabs'):
            vodHeader = pdfa(html,p['tabs'])
            vodHeader = [pq(v).text() for v in vodHeader]
        else:
            vodHeader = ['道长在线']

        for v in vodHeader:
            playFrom.append(v)
        vod_play_from = vod_play_from.join(playFrom)

        vod_play_url = '$$$'
        vod_tab_list = []
        if p.get('lists'):
            for i in range(len(vodHeader)):
               p1 = p['lists'].replace('#id',str(i))
               vodList = pdfa(html,p1) # 1条线路的选集列表
               vodList = [pq(i).text()+'$'+pd(i,'a&&href') for i in vodList]  # 拼接成 名称$链接
               vlist = '#'.join(vodList) # 拼多个选集
               vod_tab_list.append(vlist)
            vod_play_url = vod_play_url.join(vod_tab_list)
        # print(vod_play_url)
        vod['vod_play_from'] = vod_play_from
        vod['vod_play_url'] = vod_play_url

        result = {
            'list': [
                vod
            ]
        }
        return result

    def searchContent(self, key, fypage=1):
        pg = str(fypage)
        url = self.searchUrl.replace('**', key).replace('fypage',pg)
        if not str(url).startswith('http'):
            url = urljoin(self.url,url)
        print(url)
        headers = {'user-agent': self.ua}
        r = requests.get(url, headers=headers)
        html = r.text
        p = self.搜索.split(';')  # 解析
        jsp = jsoup(self.url)
        pdfh = jsp.pdfh
        pdfa = jsp.pdfa
        pd = jsp.pd
        pq = jsp.pq
        items = pdfa(html, p[0])
        videos = []
        for item in items:
            # print(item)
            title = pdfh(item, p[1])
            img = pd(item, p[2])
            desc = pdfh(item, p[3])
            link = pd(item, p[4])
            content = '' if len(p) < 6 else pdfh(item, p[5])
            # sid = self.regStr(sid, "/video/(\\S+).html")
            videos.append({
                "vod_id": link,
                "vod_name": title,
                "vod_pic": img,
                "vod_remarks": desc,
                "vod_content": content,
            })
        result = {
            'list': videos
        }
        return result

if __name__ == '__main__':
    from utils import parser
    js_path = f'js/玩偶姐姐.js'
    ctx, js_code = parser.runJs(js_path)
    rule = ctx.eval('rule')
    cms = CMS(rule)
    print(cms.title)
    print(cms.homeContent())
    # cms.categoryContent('dianying',1)
    # print(cms.detailContent(['67391']))
    # print(cms.searchContent('斗罗大陆'))