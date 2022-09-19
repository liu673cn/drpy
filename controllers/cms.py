#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : cms.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/8/25
import json

import requests
import re
import math
from utils.web import *
from utils.system import getHost
from utils.config import playerConfig
from utils.log import logger
from utils.encode import base64Encode,baseDecode,fetch,post,request,getCryptoJS,getPreJs,buildUrl,getHome
from utils.encode import verifyCode,setDetail,join,urljoin2,parseText
from utils.safePython import safePython
from utils.parser import runPy,runJScode,JsObjectWrapper,PyJsObject
from utils.htmlParser import jsoup
from urllib.parse import urljoin,quote,unquote
from concurrent.futures import ThreadPoolExecutor  # 引入线程池
from flask import url_for,redirect,render_template_string
from easydict import EasyDict as edict
from controllers.service import storage_service

def setItem(key,value):
    lsg = storage_service()
    return lsg.setItem(key,value)

def getItem(key,value=''):
    lsg = storage_service()
    return lsg.getItem(key,value)

def clearItem(key):
    lsg = storage_service()
    return lsg.clearItem(key)

def encodeUrl(url):
    # return base64Encode(quote(url))
    # return base64Encode(url)
    return quote(url)

def stringify(obj):
    if isinstance(obj,PyJsObject):
        # obj = obj.to_dict()
        obj = parseText(str(obj))
    return json.dumps(obj, separators=(',', ':'), ensure_ascii=False)

py_ctx = {
'requests':requests,'print':print,'base64Encode':base64Encode,'baseDecode':baseDecode,
'log':logger.info,'fetch':fetch,'post':post,'request':request,'getCryptoJS':getCryptoJS,
'buildUrl':buildUrl,'getHome':getHome,'setDetail':setDetail,'join':join,'urljoin2':urljoin2,
'PC_UA':PC_UA,'MOBILE_UA':MOBILE_UA,'UC_UA':UC_UA,'IOS_UA':IOS_UA,
'setItem':setItem,'getItem':getItem,'clearItem':clearItem,'stringify':stringify
}
# print(getCryptoJS())

class CMS:
    def __init__(self, rule, db=None, RuleClass=None, PlayParse=None,new_conf=None,ext=''):
        if new_conf is None:
            new_conf = {}
        self.lsg = storage_service()
        self.title = rule.get('title', '')
        self.id = rule.get('id', self.title)
        self.filter_url = rule.get('filter_url', '')
        cate_exclude  = rule.get('cate_exclude','')
        tab_exclude  = rule.get('tab_exclude','')
        self.lazy = rule.get('lazy', False)
        # self.play_disable = new_conf.get('PLAY_DISABLE',False)
        self.play_disable = self.lsg.getItem('PLAY_DISABLE',False)
        self.retry_count = new_conf.get('RETRY_CNT',3)
        # self.lazy_mode = new_conf.get('LAZYPARSE_MODE')
        self.lazy_mode = self.lsg.getItem('LAZYPARSE_MODE',2)
        self.ocr_api = new_conf.get('OCR_API')
        # self.cate_exclude = new_conf.get('CATE_EXCLUDE','')
        self.cate_exclude = self.lsg.getItem('CATE_EXCLUDE','')
        # self.tab_exclude = new_conf.get('TAB_EXCLUDE','')
        self.tab_exclude = self.lsg.getItem('TAB_EXCLUDE','')
        if cate_exclude:
            if not str(cate_exclude).startswith('|') and not str(self.cate_exclude).endswith('|'):
                self.cate_exclude = self.cate_exclude+'|'+cate_exclude
            else:
                self.cate_exclude += cate_exclude
        if tab_exclude:
            if not str(tab_exclude).startswith('|') and not str(self.tab_exclude).endswith('|'):
                self.tab_exclude = self.tab_exclude+'|'+tab_exclude
            else:
                self.tab_exclude += tab_exclude
        # print(self.cate_exclude)
        try:
            self.vod = redirect(url_for('vod')).headers['Location']
        except:
            self.vod = '/vod'
        # if not self.play_disable and self.lazy:
        if not self.play_disable:
            self.play_parse = rule.get('play_parse', False)
            try:
                play_url = getHost(self.lazy_mode)
            except:
                play_url = getHost(1,5705)
            # play_url = new_conf.get('PLAY_URL',getHost(2))
            if not play_url.startswith('http'):
                play_url = 'http://'+play_url
            # print(play_url)
            if self.play_parse:
                # self.play_url = play_url + self.vod + '?play_url='
                self.play_url = f'{play_url}{self.vod}?rule={self.id}&ext={ext}&play_url='
                # logger.info(f'cms重定向链接:{self.play_url}')
            else:
                self.play_url = ''
        else:
            self.play_parse = False
            self.play_url = ''
        logger.info('播放免嗅地址: '+self.play_url)

        self.db = db
        self.RuleClass = RuleClass
        self.PlayParse = PlayParse
        host = rule.get('host','').rstrip('/')
        timeout = rule.get('timeout',5000)
        homeUrl = rule.get('homeUrl','/')
        url = rule.get('url','')
        detailUrl = rule.get('detailUrl','')
        searchUrl = rule.get('searchUrl','')
        default_headers = getHeaders(host)
        self_headers = rule.get('headers',{})
        default_headers.update(self_headers)
        headers = default_headers
        cookie = self.getCookie()
        # print(f'{self.title}cookie:{cookie}')
        self.oheaders = self_headers
        if cookie:
            headers['cookie'] = cookie
            self.oheaders['cookie'] = cookie
        limit = rule.get('limit',6)
        encoding = rule.get('编码', 'utf-8')
        self.limit = min(limit,30)
        keys = headers.keys()
        for k in headers.keys():
            if str(k).lower() == 'user-agent':
                v = headers[k]
                if v == 'MOBILE_UA':
                    headers[k] = MOBILE_UA
                elif v == 'PC_UA':
                    headers[k] = PC_UA
                elif v == 'UC_UA':
                    headers[k] = UC_UA
                elif v == 'IOS_UA':
                    headers[k] = IOS_UA
        lower_keys = list(map(lambda x:x.lower(),keys))
        if not 'user-agent' in lower_keys:
            headers['User-Agent'] = UA
        if not 'referer' in lower_keys:
            headers['Referer'] = host
        self.headers = headers
        # print(headers)
        self.host = host
        self.homeUrl = urljoin(host,homeUrl) if host and homeUrl else homeUrl or host
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
        self.filter_name = rule.get('filter_name', '')
        self.filter_url = rule.get('filter_url', '')
        self.filter_parse = rule.get('filter_parse', '')
        self.double = rule.get('double',False)
        self.一级 = rule.get('一级','')
        self.二级 = rule.get('二级','')
        self.搜索 = rule.get('搜索','')
        self.推荐 = rule.get('推荐','')
        self.encoding = encoding
        self.timeout = round(int(timeout)/1000,2)
        self.filter = rule.get('filter',[])
        self.extend = rule.get('extend',[])
        self.d = self.getObject()

    def getName(self):
        return self.title

    def getObject(self):
        o = edict({
            'jsp':jsoup(self.url),
            'getParse':self.getParse,
            'saveParse':self.saveParse,
            'oheaders':self.oheaders,
            'encoding':self.encoding,
            'name':self.title,
            'timeout':self.timeout,
        })
        return o

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
            "vod_id": "id",
            "vod_name": "片名",
            "vod_pic": "",# 图片
            "type_name": "剧情",
            "vod_year": "年份",
            "vod_area": "地区",
            "vod_remarks": "更新信息",
            "vod_actor": "主演",
            "vod_director": "导演",
            "vod_content": "简介"
        }

    def jsoup(self):
        jsp = jsoup(self.url)
        pdfh = jsp.pdfh
        pdfa = jsp.pdfa
        pd = jsp.pd
        pjfh = jsp.pjfh
        pjfa = jsp.pjfa
        pj = jsp.pj

        pq = jsp.pq
        return pdfh,pdfa,pd,pq

    def getClasses(self):
        if not self.db:
            msg = '未提供数据库连接'
            print(msg)
            return []
        name = self.getName()
        # self.db.metadata.clear()
        # RuleClass = rule_classes.init(self.db)
        res = self.db.session.query(self.RuleClass).filter(self.RuleClass.name == name).first()
        # _logger.info('xxxxxx')
        if res:
            if not all([res.class_name,res.class_url]):
                return []
            cls = res.class_name.split('&')
            cls2 = res.class_url.split('&')
            classes = [{'type_name':cls[i],'type_id':cls2[i]} for i in range(len(cls))]
            # _logger.info(classes)
            logger.info(f"{self.getName()}使用缓存分类:{classes}")
            return classes
        else:
            return []

    def getCookie(self):
        name = self.getName()
        if not self.db:
            msg = f'{name}未提供数据库连接'
            print(msg)
            return False
        res = self.db.session.query(self.RuleClass).filter(self.RuleClass.name == name).first()
        if res:
            return res.cookie or None
        else:
            return None

    def saveCookie(self,cookie):
        name = self.getName()
        if not self.db:
            msg = f'{name}未提供数据库连接'
            print(msg)
            return False
        res = self.db.session.query(self.RuleClass).filter(self.RuleClass.name == name).first()
        if res:
            res.cookie = cookie
            self.db.session.add(res)
        else:
            res = self.RuleClass(name=name, cookie=cookie)
            self.db.session.add(res)
        try:
            self.db.session.commit()
            logger.info(f'{name}已保存cookie:{cookie}')
        except Exception as e:
            return f'保存cookie发生了错误:{e}'

    def saveClass(self, classes):
        if not self.db:
            msg = '未提供数据库连接'
            print(msg)
            return msg
        name = self.getName()
        class_name = '&'.join([cl['type_name'] for cl in classes])
        class_url = '&'.join([cl['type_id'] for cl in classes])
        # data = RuleClass.query.filter(RuleClass.name == '555影视').all()
        # self.db.metadata.clear()
        # RuleClass = rule_classes.init(self.db)
        res = self.db.session.query(self.RuleClass).filter(self.RuleClass.name == name).first()
        # print(res)
        if res:
            res.class_name = class_name
            res.class_url = class_url
            self.db.session.add(res)
            msg = f'{self.getName()}修改成功:{res.id}'
        else:
            res = self.RuleClass(name=name, class_name=class_name, class_url=class_url)
            self.db.session.add(res)
            res = self.db.session.query(self.RuleClass).filter(self.RuleClass.name == name).first()
            msg = f'{self.getName()}新增成功:{res.id}'

        try:
            self.db.session.commit()
            logger.info(msg)
        except Exception as e:
            return f'发生了错误:{e}'

    def getParse(self,play_url):
        if not self.db:
            msg = '未提供数据库连接'
            print(msg)
            return ''
        name = self.getName()
        # self.db.metadata.clear()
        # RuleClass = rule_classes.init(self.db)
        res = self.db.session.query(self.PlayParse).filter(self.PlayParse.play_url == play_url).first()
        # _logger.info('xxxxxx')
        if res:
            real_url = res.real_url
            logger.info(f"{name}使用缓存播放地址:{real_url}")
            return real_url
        else:
            return ''

    def dealJson(self,html):
        try:
            # res = re.search('.*?\{(.*)\}',html,re.M|re.I).groups()[0]
            res = re.search('.*?\{(.*)\}',html,re.M|re.S).groups()[0]
            html = '{' + res + '}'
            return html
        except:
            return html

    def checkHtml(self,r):
        r.encoding = self.encoding
        html = r.text
        if html.find('?btwaf=') > -1:
            btwaf = re.search('btwaf(.*?)"',html,re.M|re.I).groups()[0]
            url = r.url.split('#')[0]+'?btwaf'+btwaf
            # print(f'需要过宝塔验证:{url}')
            cookies_dict = requests.utils.dict_from_cookiejar(r.cookies)
            cookie_str = ';'.join([f'{k}={cookies_dict[k]}' for k in cookies_dict])
            self.headers['cookie'] = cookie_str
            r = requests.get(url, headers=self.headers, timeout=self.timeout)
            r.encoding = self.encoding
            html = r.text
            if html.find('?btwaf=') < 0:
                self.saveCookie(cookie_str)

        # print(html)
        return html

    def saveParse(self, play_url,real_url):
        if not self.db:
            msg = '未提供数据库连接'
            print(msg)
            return msg
        name = self.getName()
        # data = RuleClass.query.filter(RuleClass.name == '555影视').all()
        # self.db.metadata.clear()
        # RuleClass = rule_classes.init(self.db)
        res = self.db.session.query(self.PlayParse).filter(self.PlayParse.play_url == play_url).first()
        # print(res)
        if res:
            res.real_url = real_url
            self.db.session.add(res)
            msg = f'{name}服务端免嗅修改成功:{res.id}'
        else:
            res = self.PlayParse(play_url=play_url, real_url=real_url)
            self.db.session.add(res)
            res = self.db.session.query(self.PlayParse).filter(self.PlayParse.play_url == play_url).first()
            msg = f'{name}服务端免嗅新增成功:{res.id}'

        try:
            self.db.session.commit()
            logger.info(msg)
        except Exception as e:
            return f'{name}发生了错误:{e}'


    def homeContent(self,fypage=1):
        # yanaifei
        # https://yanetflix.com/vodtype/dianying.html
        t1 = time()
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
        print(self.headers)
        has_cache = False
        # print(self.homeUrl)
        if self.homeUrl.startswith('http'):
            # print(self.class_parse)
            try:
                if self.class_parse:
                    t2 = time()
                    cache_classes = self.getClasses()
                    logger.info(f'{self.getName()}读取缓存耗时:{get_interval(t2)}毫秒')
                    if len(cache_classes) > 0:
                        classes = cache_classes
                        # print(cache_classes)
                        has_cache = True
                # logger.info(f'是否有缓存分类:{has_cache}')
                if has_cache and not self.推荐:
                    pass
                else:
                    new_classes = []
                    r = requests.get(self.homeUrl, headers=self.headers, timeout=self.timeout)
                    html = self.checkHtml(r)
                    # print(html)
                    # print(self.headers)
                    if self.class_parse and not has_cache:
                        p = self.class_parse.split(';')
                        # print(p[0])
                        # print(html)
                        jsp = jsoup(self.url)
                        pdfh = jsp.pdfh
                        pdfa = jsp.pdfa
                        pd = jsp.pd
                        items = pdfa(html,p[0])
                        # print(len(items))
                        # print(items)
                        for item in items:
                            title = pdfh(item, p[1])
                            # 过滤排除掉标题名称
                            if self.cate_exclude and jsp.test(self.cate_exclude, title):
                                continue
                            url = pd(item, p[2])
                            # print(url)
                            tag = url
                            if len(p) > 3 and p[3].strip():
                                try:
                                    tag = self.regexp(p[3].strip(),url,0)
                                except:
                                    logger.info(f'分类匹配错误:{title}对应的链接{url}无法匹配{p[3]}')
                                    continue
                            new_classes.append({
                                'type_name': title,
                                'type_id': tag
                            })
                        if len(new_classes) > 0:
                            classes.extend(new_classes)
                            self.saveClass(classes)
                    video_result = self.homeVideoContent(html,fypage)
            except Exception as e:
                logger.info(f'{self.getName()}主页发生错误:{e}')

        result['class'] = classes
        if self.filter:
            if isinstance(self.filter,dict):
                result['filters'] = self.filter
            else:
                result['filters'] = playerConfig['filter']
        result.update(video_result)
        # print(result)
        logger.info(f'{self.getName()}获取首页总耗时(包含读取缓存):{get_interval(t1)}毫秒')
        return result

    def homeVideoContent(self,html,fypage=1):
        p = self.推荐
        if not p:
            return self.blank()

        jsp = jsoup(self.homeUrl)
        result = {}
        videos = []
        is_js = isinstance(p, str) and str(p).strip().startswith('js:')  # 是js
        if is_js:
            headers['Referer'] = getHome(self.host)
            py_ctx.update({
                'input': self.homeUrl,
                'HOST': self.host,
                'TYPE': 'home',  # 海阔js环境标志
                'oheaders':self.d.oheaders,
                'fetch_params': {'headers': self.headers, 'timeout': self.d.timeout, 'encoding': self.d.encoding},
                'd': self.d,
                'getParse': self.d.getParse,
                'saveParse': self.d.saveParse,
                'jsp': jsp, 'setDetail': setDetail,
            })
            ctx = py_ctx
            jscode = getPreJs() + p.strip().replace('js:', '', 1)
            # print(jscode)
            try:
                loader, _ = runJScode(jscode, ctx=ctx)
                # print(loader.toString())
                vods = loader.eval('VODS')
                # print(vods)
                if isinstance(vods, JsObjectWrapper):
                    videos = vods.to_list()
            except Exception as e:
                logger.info(f'首页推荐执行js获取列表出错:{e}')
        else:
            p = p.strip().split(';')  # 解析
            if not self.double and len(p) < 5:
                return self.blank()
            if self.double and len(p) < 6:
                return self.blank()
            jsp = jsoup(self.homeUrl)
            is_json = str(p[0]).startswith('json:')
            if is_json:
                html = self.dealJson(html)
            pdfh = jsp.pjfh if is_json else jsp.pdfh
            pdfa = jsp.pjfa if is_json else jsp.pdfa
            pd = jsp.pj if is_json else jsp.pd
            # print(html)
            try:
                if self.double:
                    items = pdfa(html, p[0])
                    # print(items)
                    # print(len(items))
                    for item in items:
                        items2 = pdfa(item,p[1])
                        # print(items2)
                        for item2 in items2:
                            try:
                                title = pdfh(item2, p[2])
                                try:
                                    img = pd(item2, p[3])
                                except:
                                    img = ''
                                desc = pdfh(item2, p[4])
                                links = [pd(item2, p5) if not self.detailUrl else pdfh(item2, p5) for p5 in p[5].split('+')]
                                link = '$'.join(links)
                                content = '' if len(p) < 7 else pdfh(item2, p[6])
                                videos.append({
                                    "vod_id": link,
                                    "vod_name": title,
                                    "vod_pic": img,
                                    "vod_remarks": desc,
                                    "no_use":{
                                        "vod_content": content,
                                        "type_id": 1,
                                        "type_name": "首页推荐",
                                    },
                                })
                            except:
                                pass
                else:
                    items = pdfa(html, p[0].replace('json:',''))
                    # print(items)
                    for item in items:
                        try:
                            title = pdfh(item, p[1])
                            img = pd(item, p[2])
                            desc = pdfh(item, p[3])
                            # link = pd(item, p[4])
                            links = [pd(item, p5) if not self.detailUrl else pdfh(item, p5) for p5 in p[4].split('+')]
                            link = '$'.join(links)
                            content = '' if len(p) < 6 else pdfh(item, p[5])
                            videos.append({
                                "vod_id": link,
                                "vod_name": title,
                                "vod_pic": img,
                                "vod_remarks": desc,
                                "no_use": {
                                    "vod_content": content,
                                    "type_id": 1,
                                    "type_name": "首页推荐",
                                },
                            })
                        except:
                            pass

            # result['list'] = videos[min((fypage-1)*self.limit,len(videos)-1):min(fypage*self.limit,len(videos))]
            except Exception as e:
                logger.info(f'首页内容获取失败:{e}')
                return self.blank()

        result['list'] = videos
        # print(videos)
        result['no_use'] = {
            'code': 1,
            'msg': '数据列表',
            'page': fypage,
            'pagecount': math.ceil(len(videos) / self.limit),
            'limit': self.limit,
            'total': len(videos),
            'now_count': len(result['list']),
        }
        # print(result)
        return result

    def categoryContent(self, fyclass, fypage, fl=None):
        """
        一级带分类的数据返回
        :param fyclass: 分类标识
        :param fypage: 页码
        :param fl: 筛选
        :return: cms一级数据
        """

        if fl is None:
            fl = {}
        result = {}
        # urlParams = ["", "", "", "", "", "", "", "", "", "", "", ""]
        # urlParams = [""] * 12
        # urlParams[0] = tid
        # urlParams[8] = str(pg)
        # for key in self.extend:
        #     urlParams[int(key)] = self.extend[key]
        # params = '-'.join(urlParams)
        # print(params)
        # url = self.url + '/{0}.html'.format
        t1 = time()
        pg = str(fypage)
        url = self.url.replace('fyclass',fyclass)
        if self.filter_url:
            if not 'fyfilter' in url: # 第一种情况,默认不写fyfilter关键字,视为直接拼接在链接后面当参数
                if not url.endswith('&') and not self.filter_url.startswith('&'):
                    url += '&'
                url += self.filter_url
            else: # 第二种情况直接替换关键字为待拼接的结果后面渲染,适用于 ----fypage.html的情况
                url = url.replace('fyfilter', self.filter_url)
            url = render_template_string(url,fl=fl)

            # fl_url = render_template_string(self.filter_url,fl=fl)
            # if not 'fyfilter' in url: # 第一种情况,默认不写fyfilter关键字,视为直接拼接在链接后面当参数
            #     if not url.endswith('&') and not fl_url.startswith('&'):
            #         url += '&'
            #     url += fl_url
            # else: # 第二种情况直接替换关键字为渲染后的结果,适用于 ----fypage.html的情况
            #     url = url.replace('fyfilter',fl_url)
        if url.find('fypage') > -1:
            if '(' in url and ')' in url:
                # url_rep = url[url.find('('):url.find(')')+1]
                # cnt_page = url.split('(')[1].split(')')[0].replace('fypage',pg)
                # print(url_rep)
                url_rep = re.search('.*?\((.*)\)',url,re.M|re.S).groups()[0]
                cnt_page = url_rep.replace('fypage', pg)
                # print(url_rep)
                # print(cnt_page)
                cnt_ctx = {}
                exec(f'cnt_pg={cnt_page}', cnt_ctx)
                cnt_pg = str(cnt_ctx['cnt_pg']) # 计算表达式的结果
                url = url.replace(url_rep,str(cnt_pg)).replace('(','').replace(')','')
                # print(url)
            else:
                url = url.replace('fypage',pg)
        if fypage == 1 and self.test('[\[\]]',url):
            url = url.split('[')[1].split(']')[0]
        # print(url)
        p = self.一级
        jsp = jsoup(self.url)
        videos = []
        is_js = isinstance(p, str) and str(p).startswith('js:')  # 是js
        if is_js:
            headers['Referer'] = getHome(url)
            py_ctx.update({
                'input': url,
                'TYPE': 'cate',  # 海阔js环境标志
                'oheaders': self.d.oheaders,
                'fetch_params': {'headers': self.headers, 'timeout': self.d.timeout, 'encoding': self.d.encoding},
                'd': self.d,
                'cateID':fyclass, # 分类id
                'MY_CATE':fyclass, # 分类id
                'MY_FL':fl, # 筛选
                'MY_PAGE':fypage,  # 页数
                'detailUrl':self.detailUrl or '', # 详情页链接
                'getParse': self.d.getParse,
                'saveParse': self.d.saveParse,
                'jsp': jsp, 'setDetail': setDetail,
            })
            ctx = py_ctx
            # print(ctx)
            jscode = getPreJs() + p.replace('js:', '', 1)
            # print(jscode)
            loader, _ = runJScode(jscode, ctx=ctx)
            # print(loader.toString())
            vods = loader.eval('VODS')
            # print('vods:',vods)
            if isinstance(vods, JsObjectWrapper):
                videos = vods.to_list()

        else:
            p = p.split(';')  # 解析
            if len(p) < 5:
                return self.blank()

            is_json = str(p[0]).startswith('json:')
            pdfh = jsp.pjfh if is_json else jsp.pdfh
            pdfa = jsp.pjfa if is_json else jsp.pdfa
            pd = jsp.pj if is_json else jsp.pd
            # print(pdfh(r.text,'body a.module-poster-item.module-item:eq(1)&&Text'))
            # print(pdfh(r.text,'body a.module-poster-item.module-item:eq(0)'))
            # print(pdfh(r.text,'body a.module-poster-item.module-item:first'))

            items = []
            try:
                r = requests.get(url, headers=self.headers, timeout=self.timeout)
                html = self.checkHtml(r)
                if is_json:
                    html = self.dealJson(html)
                    html = json.loads(html)
                # print(html)
                items = pdfa(html,p[0].replace('json:','',1))
            except:
                pass
            # print(items)
            for item in items:
                # print(item)
                try:
                    title = pdfh(item, p[1])
                    img = pd(item, p[2])
                    desc = pdfh(item, p[3])
                    links = [pd(item, p4) if not self.detailUrl else pdfh(item, p4) for p4 in p[4].split('+')]
                    link = '$'.join(links)
                    content = '' if len(p) < 6 else pdfh(item, p[5])
                    # sid = self.regStr(sid, "/video/(\\S+).html")
                    videos.append({
                        "vod_id": f'{fyclass}${link}' if self.detailUrl else link,# 分类,播放链接
                        "vod_name": title,
                        "vod_pic": img,
                        "vod_remarks": desc,
                        "vod_content": content,
                    })
                except Exception as e:
                    print(f'发生了错误:{e}')
                    pass
        # print(videos)
        limit = 40
        cnt = 9999 if len(videos) > 0 else 0
        result['list'] = videos
        result['page'] = fypage
        result['pagecount'] = max(cnt,fypage)
        result['limit'] = limit
        result['total'] = cnt
        # print(result)
        logger.info(f'{self.getName()}获取分类{fyclass}第{fypage}页耗时:{get_interval(t1)}毫秒,共计{round(len(str(result)) / 1000, 2)} kb')

        return result

    def detailOneVod(self,id,fyclass='',show_name=False):
        detailUrl = str(id)
        vod = {}
        if not detailUrl.startswith('http') and not '/' in detailUrl:
            url = self.detailUrl.replace('fyid', detailUrl).replace('fyclass',fyclass)
        elif '/' in detailUrl:
            url = urljoin(self.homeUrl,detailUrl)
        else:
            url = detailUrl
        logger.info(f'进入详情页: {url}')
        try:
            p = self.二级  # 解析
            if p == '*':
                vod = self.blank_vod()
                vod['vod_play_from'] = '道长在线'
                vod['vod_remarks'] = detailUrl
                vod['vod_actor'] = '没有二级,只有一级链接直接嗅探播放'
                vod['vod_content'] = url if not show_name else f'({self.id}) {url}'
                vod['vod_play_url'] = '嗅探播放$'+self.play_url+url
                print(vod)
                return vod

            if not p:
                return vod
            if not isinstance(p,dict) and not isinstance(p,str):
                return vod
            if isinstance(p,str) and not str(p).startswith('js:'):
                return vod

            jsp = jsoup(self.url)

            is_json = p.get('is_json',False) if isinstance(p,dict) else False # 二级里加is_json参数
            is_js = isinstance(p,str) and str(p).startswith('js:') # 是js
            if is_js:
                headers['Referer'] = getHome(url)
                py_ctx.update({
                    'input': url,
                    'TYPE': 'detail',  # 海阔js环境标志
                    'cateID': fyclass,  # 当前分类
                    'oheaders': self.d.oheaders,
                    'fetch_params': {'headers': self.headers, 'timeout': self.d.timeout, 'encoding': self.d.encoding},
                    'd': self.d,
                    'getParse': self.d.getParse,
                    'saveParse': self.d.saveParse,
                    'jsp':jsp,'setDetail':setDetail,'play_url':self.play_url
                })
                ctx = py_ctx
                # print(ctx)
                jscode = getPreJs() + p.replace('js:','',1)
                # print(jscode)
                loader, _ = runJScode(jscode, ctx=ctx)
                # print(loader.toString())
                vod = loader.eval('vod')
                if isinstance(vod,JsObjectWrapper):
                    vod = vod.to_dict()
                else:
                    vod = {}
                # print(type(vod))
                # print(vod)
            else:
                pdfh = jsp.pjfh if is_json else jsp.pdfh
                pdfa = jsp.pjfa if is_json else jsp.pdfa
                pd = jsp.pj if is_json else jsp.pd
                pq = jsp.pq
                obj = {}
                vod_name = ''
                r = requests.get(url, headers=self.headers, timeout=self.timeout)
                html = self.checkHtml(r)
                if is_json:
                    html = self.dealJson(html)
                    html = json.loads(html)
                if p.get('title'):
                    p1 = p['title'].split(';')
                    vod_name = pdfh(html,p1[0]).replace('\n',' ')
                    # title = '\n'.join([pdfh(html,i).replace('\n',' ') for i in p1])
                    title = '\n'.join([','.join([pdfh(html, pp1).strip() for pp1 in i.split('+')]) for i in p1])
                    # print(title)
                    obj['title'] = title
                if p.get('desc'):
                    try:
                        p1 = p['desc'].split(';')
                        desc = '\n'.join([pdfh(html,i).replace('\n',' ') for i in p1])
                        obj['desc'] = desc
                    except:
                        pass

                if p.get('content'):
                    p1 = p['content'].split(';')
                    try:
                        content = '\n'.join([pdfh(html,i).replace('\n',' ') for i in p1])
                        obj['content'] = content
                    except:
                        pass

                if p.get('img'):
                    p1 = p['img']
                    try:
                        img = pd(html,p1)
                        obj['img'] = img
                    except Exception as e:
                        logger.info(f'二级图片定位失败,但不影响使用{e}')

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
                if p.get('重定向') and str(p['重定向']).startswith('js:'):
                    headers['Referer'] = getHome(url)
                    py_ctx.update({
                        'input': url,
                        'html': html,
                        'TYPE': 'detail',  # 海阔js环境标志
                        'cateID': fyclass,  # 当前分类
                        'oheaders': self.d.oheaders,
                        'fetch_params': {'headers': self.headers, 'timeout': self.d.timeout, 'encoding': self.d.encoding},
                        'd': self.d,
                        'getParse': self.d.getParse,
                        'saveParse': self.d.saveParse,
                        'jsp': jsp, 'setDetail': setDetail,
                    })
                    ctx = py_ctx
                    # print(ctx)
                    rcode = p['重定向'].replace('js:', '', 1)
                    jscode = getPreJs() + rcode
                    # print(jscode)
                    loader, _ = runJScode(jscode, ctx=ctx)
                    # print(loader.toString())
                    logger.info(f'开始执行二级重定向代码:{rcode}')
                    html = loader.eval('html')
                    if isinstance(vod, JsObjectWrapper):
                        html = str(html)

                if p.get('tabs'):
                    vodHeader = []
                    # print(p['tabs'].split(';')[0])
                    vHeader = pdfa(html,p['tabs'].split(';')[0])
                    # print(f'线路列表数:{len((vodHeader))}')
                    # print(vodHeader)
                    if not is_json:
                        for v in vHeader:
                            # 过滤排除掉线路标题
                            v_title = pq(v).text()
                            if self.tab_exclude and jsp.test(self.tab_exclude, v_title):
                                continue
                            vodHeader.append(v_title)
                    else:
                        vodHeader = vHeader
                else:
                    vodHeader = ['道长在线']

                # print(vodHeader)

                for v in vodHeader:
                    playFrom.append(v)
                vod_play_from = vod_play_from.join(playFrom)

                vod_play_url = '$$$'
                vod_tab_list = []
                if p.get('lists'):
                    for i in range(len(vodHeader)):
                       tab_name = str(vodHeader[i])
                       tab_ext = p['tabs'].split(';')[1] if len(p['tabs'].split(';')) > 1 else ''
                       p1 = p['lists'].replace('#idv',tab_name).replace('#id',str(i))
                       tab_ext = tab_ext.replace('#idv',tab_name).replace('#id',str(i))
                       vodList = pdfa(html,p1) # 1条线路的选集列表
                       # print(vodList)
                       # vodList = [pq(i).text()+'$'+pd(i,'a&&href') for i in vodList]  # 拼接成 名称$链接
                       if self.play_parse: # 自动base64编码
                           vodList = [(pdfh(html,tab_ext) if tab_ext else tab_name)+'$'+self.play_url+encodeUrl(i) for i in vodList] if is_json else\
                               [pq(i).text()+'$'+self.play_url+encodeUrl(pd(i,'a&&href')) for i in vodList]  # 拼接成 名称$链接
                       else:
                           vodList = [(pdfh(html, tab_ext) if tab_ext else tab_name) + '$' + self.play_url + i for i in
                                      vodList] if is_json else \
                               [pq(i).text() + '$' + self.play_url + pd(i, 'a&&href') for i in vodList]  # 拼接成 名称$链接
                       vlist = '#'.join(vodList) # 拼多个选集
                       vod_tab_list.append(vlist)
                    vod_play_url = vod_play_url.join(vod_tab_list)
                # print(vod_play_url)
                vod['vod_play_from'] = vod_play_from
                # print(vod_play_from)
                vod['vod_play_url'] = vod_play_url
                # print(vod_play_url)
        except Exception as e:
            logger.info(f'{self.getName()}获取单个详情页{detailUrl}出错{e}')
        if show_name:
            vod['vod_content'] = f'({self.id}){vod.get("vod_content","")}'
        return vod

    def detailContent(self, fypage, array,show_name=False):
        """
        cms二级数据
        :param array:
        :return:
        """
        t1 = time()
        array = array if len(array) <= self.limit else array[(fypage-1)*self.limit:min(self.limit*fypage,len(array))]
        thread_pool = ThreadPoolExecutor(min(self.limit,len(array)))  # 定义线程池来启动多线程执行此任务
        obj_list = []
        try:
            for vod_url in array:
                # print(vod_url)
                vod_class = ''
                if vod_url.find('$') > -1:
                    tmp = vod_url.split('$')
                    vod_class = tmp[0]
                    vod_url = tmp[1]
                obj = thread_pool.submit(self.detailOneVod, vod_url,vod_class,show_name)
                obj_list.append(obj)
            thread_pool.shutdown(wait=True)  # 等待所有子线程并行完毕
            vod_list = [obj.result() for obj in obj_list]
            result = {
                'list': vod_list
            }
            logger.info(f'{self.getName()}获取详情页耗时:{get_interval(t1)}毫秒,共计{round(len(str(result)) / 1000, 2)} kb')
        except Exception as e:
            result = {
                'list': []
            }
            logger.info(f'{self.getName()}获取详情页耗时:{get_interval(t1)}毫秒,发生错误:{e}')
        # print(result)
        return result

    def searchContent(self, key, fypage=1,show_name=False):
        pg = str(fypage)
        if not self.searchUrl:
            return self.blank()
        url = self.searchUrl.replace('**', key).replace('fypage',pg)
        logger.info(f'{self.getName()}搜索链接:{url}')
        if not self.搜索:
            return self.blank()
        # p = self.一级.split(';') if self.搜索 == '*' and self.一级 else self.搜索.split(';')  # 解析
        p = self.一级 if self.搜索 == '*' and self.一级 else self.搜索
        jsp = jsoup(self.url)
        videos = []
        is_js = isinstance(p, str) and str(p).startswith('js:')  # 是js
        if is_js:
            headers['Referer'] = getHome(url)
            py_ctx.update({
                'input': url,
                'oheaders': self.d.oheaders,
                'fetch_params': {'headers': self.headers, 'timeout': self.d.timeout, 'encoding': self.d.encoding},
                'd': self.d,
                'KEY': key,  # 搜索关键字
                'TYPE': 'search',  # 海阔js环境标志
                'detailUrl': self.detailUrl or '',
                # 详情页链接
                'getParse': self.d.getParse,
                'saveParse': self.d.saveParse,
                'jsp': jsp, 'setDetail': setDetail,
            })
            ctx = py_ctx
            # print(ctx)
            jscode = getPreJs() + p.replace('js:', '', 1)
            # print(jscode)
            loader, _ = runJScode(jscode, ctx=ctx)
            # print(loader.toString())
            vods = loader.eval('VODS')
            # print(len(vods),type(vods))
            if isinstance(vods, JsObjectWrapper):
                videos = vods.to_list()
            # print(videos)
        else:
            p = p.split(';')
            if len(p) < 5:
                return self.blank()
            is_json = str(p[0]).startswith('json:')
            pdfh = jsp.pjfh if is_json else jsp.pdfh
            pdfa = jsp.pjfa if is_json else jsp.pdfa
            pd = jsp.pj if is_json else jsp.pd
            pq = jsp.pq
            try:
                r = requests.get(url, headers=self.headers,timeout=self.timeout)
                html = self.checkHtml(r)
                if is_json:
                    html = self.dealJson(html)
                    html = json.loads(html)
                # print(html)
                if not is_json and html.find('输入验证码') > -1:
                    cookie = verifyCode(url,self.headers,self.timeout,self.retry_count,self.ocr_api)
                    # cookie = ''
                    if not cookie:
                        return {
                            'list': videos
                        }
                    self.saveCookie(cookie)
                    self.headers['cookie'] = cookie
                    r = requests.get(url, headers=self.headers, timeout=self.timeout)
                    r.encoding = self.encoding
                    html = r.text

                items = pdfa(html,p[0].replace('json:','',1))
                # print(len(items),items)
                videos = []
                for item in items:
                    # print(item)
                    try:
                        # title = pdfh(item, p[1])
                        title = ''.join([pdfh(item, i) for i in p[1].split('||')])
                        try:
                            img = pd(item, p[2])
                        except:
                            img = ''
                        try:
                            desc = pdfh(item, p[3])
                        except:
                            desc = ''
                        try:
                            content = '' if len(p) < 6 else pdfh(item, p[5])
                        except:
                            content = ''
                        # link = '$'.join([pd(item, p4) for p4 in p[4].split('+')])
                        links = [pd(item, p4) if not self.detailUrl else pdfh(item, p4) for p4 in p[4].split('+')]
                        link = '$'.join(links)
                        # print(content)
                        # sid = self.regStr(sid, "/video/(\\S+).html")
                        videos.append({
                            "vod_id": link,
                            "vod_name": title,
                            "vod_pic": img,
                            "vod_remarks": desc,
                            "vod_content": content, # 无用参数
                        })
                    except Exception as e:
                        print(e)
                        pass
                # print(videos)
            except Exception as e:
                logger.info(f'搜索{self.getName()}发生错误:{e}')
        if show_name and len(videos) > 0:
            for video in videos:
                video['vod_name'] = self.id + ' '+video['vod_name']
                video['vod_rule'] = self.id
                video['vod_id'] = video['vod_id'] +'#' + self.id
        result = {
            'list': videos
        }
        return result

    def playContent(self, play_url,jxs=None,flag=None):
        # flag参数只有类型为4的时候才有,可以忽略
        # logger.info('播放免嗅地址: ' + self.play_url)
        # 注意:全局flags里的视频没法执行免嗅代码，因为会自动拦截去调用解析: url=yoursite:5705/vod?play_url=xxxx
        if not jxs:
            jxs = []

        # print(play_url)
        if play_url.find('http') == -1: # 字符串看起来被编码的
            try:
                play_url = baseDecode(play_url) # 自动base64解码
            except:
                pass
        # print(unquote(play_url))
        play_url = unquote(play_url)
        if self.lazy:
            print(f'{play_url}->开始执行免嗅代码{type(self.lazy)}->{self.lazy}')
            t1 = time()
            try:
                if type(self.lazy) == JsObjectWrapper:
                    logger.info(f'lazy非纯文本免嗅失败耗时:{get_interval(t1)}毫秒,播放地址:{play_url}')

                elif not str(self.lazy).startswith('js:'):
                    pycode = runPy(self.lazy)
                    if pycode:
                        # print(pycode)
                        pos = pycode.find('def lazyParse')
                        if pos < 0:
                            return play_url
                        pyenv = safePython(self.lazy,pycode[pos:])
                        lazy_url = pyenv.action_task_exec('lazyParse',[play_url,self.d])
                        logger.info(f'py免嗅耗时:{get_interval(t1)}毫秒,播放地址:{lazy_url}')
                        if isinstance(lazy_url,str) and lazy_url.startswith('http'):
                            play_url = lazy_url
                else:
                    jscode = str(self.lazy).split('js:')[1]
                    jsp = jsoup(self.url)
                    # jscode = f'var input={play_url};{jscode}'
                    # print(jscode)
                    headers['Referer'] = getHome(play_url)
                    py_ctx.update({
                        'input': play_url,
                        'oheaders': self.d.oheaders,
                        'fetch_params':{'headers':self.headers,'timeout':self.d.timeout,'encoding':self.d.encoding},
                        'd': self.d,
                        'jxs':jxs,
                        'getParse':self.d.getParse,
                        'saveParse':self.d.saveParse,
                        'jsp': jsp,
                        'pdfh': self.d.jsp.pdfh,
                        'pdfa': self.d.jsp.pdfa, 'pd': self.d.jsp.pd,'play_url':self.play_url
                    })
                    ctx = py_ctx
                    # print(ctx)
                    jscode = getPreJs() + jscode
                    # print(jscode)
                    loader,_ = runJScode(jscode,ctx=ctx)
                    # print(loader.toString())
                    play_url = loader.eval('input')
                    if isinstance(play_url,JsObjectWrapper):
                        play_url = play_url.to_dict()
                    # print(type(play_url))
                    # print(play_url)
                    logger.info(f'js免嗅耗时:{get_interval(t1)}毫秒,播放地址:{play_url}')
            except Exception as e:
                logger.info(f'免嗅耗时:{get_interval(t1)}毫秒,并发生错误:{e}')
            return play_url
        else:
            logger.info(f'播放重定向到:{play_url}')
            return play_url

if __name__ == '__main__':
    print(urljoin('https://api.web.360kan.com/v1/f',
                  '//0img.hitv.com/preview/sp_images/2022/01/28/202201281528074643023.jpg'))
    # exit()
    from utils import parser
    # js_path = f'js/玩偶姐姐.js'
    # js_path = f'js/555影视.js'
    with open('../js/模板.js', encoding='utf-8') as f:
        before = f.read()
    js_path = f'js/360影视.js'
    ctx, js_code = parser.runJs(js_path,before=before)
    ruleDict = ctx.rule.to_dict()
    # lazy = ctx.eval('lazy')
    # print(lazy)
    # ruleDict['id'] = rule  # 把路由请求的id装到字典里,后面播放嗅探才能用

    cms = CMS(ruleDict)
    print(cms.title)
    print(cms.homeContent())
    # print(cms.categoryContent('5',1))
    # print(cms.categoryContent('latest',1))
    # print(cms.detailContent(['https://www.2345ka.com/v/45499.html']))
    # print(cms.detailContent(1,['https://cokemv.me/voddetail/40573.html']))
    # cms.categoryContent('dianying',1)
    # print(cms.detailContent(['67391']))
    # print(cms.searchContent('斗罗大陆'))
    print(cms.searchContent('独行月球'))