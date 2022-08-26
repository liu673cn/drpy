#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : cms.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/8/25
import requests
import re
import math
from utils.web import *
from utils.config import config
from utils.htmlParser import jsoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor  # 引入线程池

class CMS:
    def __init__(self,rule):
        host = rule.get('host','').rstrip('/')
        timeout = rule.get('timeout',5000)
        homeUrl = rule.get('homeUrl','/')
        url = rule.get('url','')
        detailUrl = rule.get('detailUrl','')
        searchUrl = rule.get('searchUrl','')
        headers = rule.get('headers',{})
        limit = rule.get('limit',6)
        encoding = rule.get('编码', 'utf-8')
        self.limit = min(limit,20)
        keys = headers.keys()
        for k in headers.keys():
            if str(k).lower() == 'user-agent':
                v = headers[k]
                if v == 'MOBILE_UA':
                    headers[k] = MOBILE_UA
                elif v == 'PC_UA':
                    headers[k] = PC_UA
        lower_keys = list(map(lambda x:x.lower(),keys))
        if not 'user-agent' in lower_keys:
            headers['User-Agent'] = UA
        self.headers = headers
        self.host = host
        self.homeUrl = urljoin(host,homeUrl) if host and homeUrl else homeUrl
        if url.find('[') >-1 and url.find(']') > -1:
            u1 = url.split('[')[0]
            u2 = url.split('[')[1].split(']')[0]
            self.url = urljoin(host,u1)+'['+urljoin(host,u2)+']' if host and url else url
        else:
            self.url = urljoin(host, url) if host and url else url

        self.detailUrl = urljoin(host,detailUrl) if host and detailUrl else detailUrl
        self.searchUrl = urljoin(host,searchUrl) if host and searchUrl else searchUrl
        self.class_name = rule.get('class_name','')
        self.class_url = rule.get('class_url','')
        self.class_parse = rule.get('class_parse','')
        self.double = rule.get('double',False)
        self.一级 = rule.get('一级','')
        self.二级 = rule.get('二级','')
        self.搜索 = rule.get('搜索','')
        self.推荐 = rule.get('推荐','')
        self.title = rule.get('title','')
        self.encoding = encoding
        self.timeout = round(int(timeout)/1000,2)
        self.filter = rule.get('filter',[])
        self.extend = rule.get('extend',[])

    def getName(self):
        return self.title

    def regexp(self,prule,text,pos=None):
        ret = re.search(prule,text).groups()
        if pos != None and isinstance(pos,int):
            return ret[pos]
        else:
            return ret

    def test(self,text,string):
        searchObj = re.search(rf'{text}', string, re.M | re.I)
        # print(searchObj)
        # global vflag
        if searchObj:
            # vflag = searchObj.group()
            pass
        return searchObj

    def blank(self):
        result = {
            'list': []
        }
        return result

    def blank_vod(self):
        return {
            "vod_id": "",
            "vod_name": "",
            "vod_pic": "",
            "type_name": "",
            "vod_year": "",
            "vod_area": "",
            "vod_remarks": "",
            "vod_actor": "",
            "vod_director": "",
            "vod_content": ""
        }

    def jsoup(self):
        jsp = jsoup(self.url)
        pdfh = jsp.pdfh
        pdfa = jsp.pdfa
        pd = jsp.pd
        pq = jsp.pq
        return pdfh,pdfa,pd,pq

    def homeContent(self,fypage=1):
        # yanaifei
        # https://yanetflix.com/vodtype/dianying.html
        result = {}
        classes = []
        video_result = self.blank()

        if self.class_url and self.class_name:
            class_names = self.class_name.split('&')
            class_urls = self.class_url.split('&')
            cnt = min(len(class_urls), len(class_names))
            for i in range(cnt):
                classes.append({
                    'type_name': class_names[i],
                    'type_id': class_urls[i]
                })
        # print(self.url)
        if self.homeUrl.startswith('http'):
            # print(self.homeUrl)
            # print(self.class_parse)
            try:
                r = requests.get(self.homeUrl,headers=self.headers,timeout=self.timeout)
                r.encoding = self.encoding
                html = r.text
                if self.class_parse:
                    p = self.class_parse.split(';')
                    jsp = jsoup(self.url)
                    pdfh = jsp.pdfh
                    pdfa = jsp.pdfa
                    pd = jsp.pd
                    items = pdfa(html,p[0])
                    for item in items:
                        title = pdfh(item, p[1])
                        url = pd(item, p[2])
                        tag = url
                        if len(p) > 3 and p[3].strip():
                            tag = self.regexp(p[3].strip(),url,0)
                        classes.append({
                            'type_name': title,
                            'type_id': tag
                        })

                video_result = self.homeVideoContent(html,fypage)
            except Exception as e:
                print(e)

        result['class'] = classes
        if self.filter:
            result['filters'] = config['filter']
        result.update(video_result)
        return result

    def homeVideoContent(self,html,fypage=1):
        if not self.推荐:
            return self.blank()

        p = self.推荐.split(';')  # 解析
        if not self.double and len(p) < 5:
            return self.blank()
        if self.double and len(p) < 6:
            return self.blank()
        result = {}
        videos = []
        jsp = jsoup(self.homeUrl)
        pdfh = jsp.pdfh
        pdfa = jsp.pdfa
        pd = jsp.pd
        try:
            if self.double:
                items = pdfa(html, p[0])
                for item in items:
                    items2 = pdfa(item,p[1])
                    for item2 in items2:
                        title = pdfh(item2, p[2])
                        img = pd(item2, p[3])
                        desc = pdfh(item2, p[4])
                        link = pd(item2, p[5])
                        content = '' if len(p) < 7 else pdfh(item2, p[6])
                        videos.append({
                            "vod_id": link,
                            "vod_name": title,
                            "vod_pic": img,
                            "vod_remarks": desc,
                            "vod_content": content,
                            "type_id": 1,
                            "type_name": "首页推荐",
                        })
            else:
                items = pdfa(html, p[0])
                for item in items:
                    title = pdfh(item, p[1])
                    img = pd(item, p[2])
                    desc = pdfh(item, p[3])
                    link = pd(item, p[4])
                    content = '' if len(p) < 6 else pdfh(item, p[5])
                    videos.append({
                        "vod_id": link,
                        "vod_name": title,
                        "vod_pic": img,
                        "vod_remarks": desc,
                        "vod_content": content,
                        "type_id": 1,
                        "type_name": "首页推荐",
                    })
            result['list'] = videos
            result['code'] = 1
            result['msg'] = '数据列表'
            result['page'] = fypage
            result['pagecount'] = math.ceil(len(videos)/self.limit)
            result['limit'] = self.limit
            result['total'] = len(videos)
            return result
        except Exception as e:
            print(f'首页内容获取失败:{e}')
            return self.blank()

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
        if fypage == 1 and self.test('[\[\]]',url):
            url = url.split('[')[1].split(']')[0]
        r = requests.get(url, headers=self.headers,timeout=self.timeout)
        r.encoding = self.encoding
        print(r.url)
        p = self.一级.split(';')  # 解析
        if len(p) < 5:
            return self.blank()

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
        result['limit'] = 9999
        result['total'] = 999999
        return result

    def detailOneVod(self,id):
        detailUrl = str(id)
        vod = {}
        if not detailUrl.startswith('http'):
            url = self.detailUrl.replace('fyid', detailUrl)
        else:
            url = detailUrl
        # print(url)
        r = requests.get(url, headers=self.headers,timeout=self.timeout)
        r.encoding = self.encoding
        html = r.text
        # print(html)
        p = self.二级  # 解析
        if p == '*':
            vod = self.blank_vod()
            vod['vod_play_from'] = '道长在线'
            vod['desc'] = detailUrl
            vod['vod_actor'] = '没有二级,只有一级链接直接嗅探播放'
            vod['content'] = detailUrl
            vod['vod_play_url'] = '嗅探播放$'+detailUrl
            return vod

        if not isinstance(p,dict):
            return vod

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
            "vod_id": detailUrl,
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

        return vod

    def detailContent(self, fypage, array):
        """
        cms二级数据
        :param array:
        :return:
        """
        array = array[(fypage-1)*self.limit:min(self.limit*fypage,len(array))]
        thread_pool = ThreadPoolExecutor(min(self.limit,len(array)))  # 定义线程池来启动多线程执行此任务
        obj_list = []
        for vod_url in array:
            obj = thread_pool.submit(self.detailOneVod, vod_url)
            obj_list.append(obj)
        thread_pool.shutdown(wait=True)  # 等待所有子线程并行完毕
        vod_list = [obj.result() for obj in obj_list]
        result = {
            'list': vod_list
        }
        return result

    def searchContent(self, key, fypage=1):
        pg = str(fypage)
        if not self.searchUrl:
            return self.blank()
        url = self.searchUrl.replace('**', key).replace('fypage',pg)
        print(url)
        r = requests.get(url, headers=self.headers)
        r.encoding = self.encoding
        html = r.text
        if not self.搜索:
            return self.blank()
        p = self.一级.split(';') if self.搜索 == '*' and self.一级 else self.搜索.split(';')  # 解析
        if len(p) < 5:
            return self.blank()

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
    # js_path = f'js/玩偶姐姐.js'
    js_path = f'js/555影视.js'
    ctx, js_code = parser.runJs(js_path)
    rule = ctx.eval('rule')
    cms = CMS(rule)
    print(cms.title)
    print(cms.homeContent())
    # print(cms.categoryContent('20',1))
    # print(cms.categoryContent('latest',1))
    # print(cms.detailContent(['https://hongkongdollvideo.com/video/b22c7cb6df40a3c4.html']))
    # cms.categoryContent('dianying',1)
    # print(cms.detailContent(['67391']))
    # print(cms.searchContent('斗罗大陆'))