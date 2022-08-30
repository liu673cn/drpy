#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : cms.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/8/25

import requests
import re
import math
from utils.web import *
from models import *
from utils.config import config
from utils.log import logger
from utils.encode import base64Encode,baseDecode,fetch,post,request,getCryptoJS,getPreJs,buildUrl
from utils.safePython import safePython
from utils.parser import runPy,runJScode
from utils.htmlParser import jsoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor  # 引入线程池
from flask import url_for,redirect
from easydict import EasyDict as edict

py_ctx = {
'requests':requests,'print':print,'base64Encode':base64Encode,'baseDecode':baseDecode,
'log':logger.info,'fetch':fetch,'post':post,'request':request,'getCryptoJS':getCryptoJS,
'buildUrl':buildUrl
}
# print(getCryptoJS())

class CMS:
    def __init__(self, rule, db=None, RuleClass=None, PlayParse=None,new_conf=None):
        if new_conf is None:
            new_conf = {}
        self.title = rule.get('title', '')
        self.id = rule.get('id', self.title)
        self.lazy = rule.get('lazy', False)
        self.play_disable = new_conf.get('PLAY_DISABLE',False)
        self.lazy_mode = new_conf.get('LAZYPARSE_MODE')
        self.vod = redirect(url_for('vod')).headers['Location']
        # if not self.play_disable and self.lazy:
        if not self.play_disable:
            self.play_parse = rule.get('play_parse', False)
            play_url = getHost(self.lazy_mode)
            # play_url = new_conf.get('PLAY_URL',getHost(2))
            if not play_url.startswith('http'):
                play_url = 'http://'+play_url
            if self.play_parse:
                # self.play_url = play_url + self.vod + '?play_url='
                self.play_url = f'{play_url}{self.vod}?rule={self.id}&play_url='
                # logger.info(f'cms重定向链接:{self.play_url}')
            else:
                self.play_url = ''
        else:
            self.play_parse = False
            self.play_url = ''

        self.db = db
        self.RuleClass = RuleClass
        self.PlayParse = PlayParse
        host = rule.get('host','').rstrip('/')
        timeout = rule.get('timeout',5000)
        homeUrl = rule.get('homeUrl','/')
        url = rule.get('url','')
        detailUrl = rule.get('detailUrl','')
        searchUrl = rule.get('searchUrl','')
        headers = rule.get('headers',{})
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
            'headers':self.headers,
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
            cls = res.class_name.split('&')
            cls2 = res.class_url.split('&')
            classes = [{'type_name':cls[i],'type_id':cls2[i]} for i in range(len(cls))]
            # _logger.info(classes)
            logger.info(f"{self.getName()}使用缓存分类:{classes}")
            return classes
        else:
            return []

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
        has_cache = False
        if self.homeUrl.startswith('http'):
            # print(self.homeUrl)
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
                    r.encoding = self.encoding
                    html = r.text
                    if self.class_parse and not has_cache:
                        p = self.class_parse.split(';')
                        print(p)
                        jsp = jsoup(self.url)
                        pdfh = jsp.pdfh
                        pdfa = jsp.pdfa
                        pd = jsp.pd
                        items = pdfa(html,p[0])
                        print(len(items))
                        print(items)
                        for item in items:
                            title = pdfh(item, p[1])
                            url = pd(item, p[2])
                            print(url)
                            tag = url
                            if len(p) > 3 and p[3].strip():
                                tag = self.regexp(p[3].strip(),url,0)
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
            result['filters'] = config['filter']
        result.update(video_result)
        logger.info(f'{self.getName()}获取首页总耗时(包含读取缓存):{get_interval(t1)}毫秒')
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
                        try:
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
                        except:
                            pass
            else:
                items = pdfa(html, p[0])
                for item in items:
                    try:
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
                    except:
                        pass
            result['list'] = videos
            result['code'] = 1
            result['msg'] = '数据列表'
            result['page'] = fypage
            result['pagecount'] = math.ceil(len(videos)/self.limit)
            result['limit'] = self.limit
            result['total'] = len(videos)
            return result
        except Exception as e:
            logger.info(f'首页内容获取失败:{e}')
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

        videos = []
        items = []
        try:
            r = requests.get(url, headers=self.headers, timeout=self.timeout)
            r.encoding = self.encoding
            print(r.url)
            html = r.text
            items = pdfa(html, p[0])
        except:
            pass
        for item in items:
            # print(item)
            try:
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
            except:
                pass
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
        try:
            p = self.二级  # 解析
            if p == '*':
                vod = self.blank_vod()
                vod['vod_play_from'] = '道长在线'
                vod['desc'] = self.play_url+detailUrl
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
            r = requests.get(url, headers=self.headers, timeout=self.timeout)
            r.encoding = self.encoding
            html = r.text
            # print(html)
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
                # print(f'线路列表数:{len((vodHeader))}')
                # print(vodHeader)
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
                   # vodList = [pq(i).text()+'$'+pd(i,'a&&href') for i in vodList]  # 拼接成 名称$链接
                   vodList = [pq(i).text()+'$'+self.play_url+pd(i,'a&&href') for i in vodList]  # 拼接成 名称$链接
                   vlist = '#'.join(vodList) # 拼多个选集
                   vod_tab_list.append(vlist)
                vod_play_url = vod_play_url.join(vod_tab_list)
            # print(vod_play_url)
            vod['vod_play_from'] = vod_play_from
            vod['vod_play_url'] = vod_play_url
        except Exception as e:
            logger.info(f'{self.getName()}获取单个详情页出错{e}')
        print(vod)
        return vod

    def detailContent(self, fypage, array):
        """
        cms二级数据
        :param array:
        :return:
        """
        t1 = time()
        array = array[(fypage-1)*self.limit:min(self.limit*fypage,len(array))]
        thread_pool = ThreadPoolExecutor(min(self.limit,len(array)))  # 定义线程池来启动多线程执行此任务
        obj_list = []
        try:
            for vod_url in array:
                obj = thread_pool.submit(self.detailOneVod, vod_url)
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

    def searchContent(self, key, fypage=1):
        pg = str(fypage)
        if not self.searchUrl:
            return self.blank()
        url = self.searchUrl.replace('**', key).replace('fypage',pg)
        logger.info(f'{self.getName()}搜索链接:{url}')
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
        videos = []
        try:
            r = requests.get(url, headers=self.headers)
            r.encoding = self.encoding
            html = r.text
            items = pdfa(html, p[0])
            # print(items)
            videos = []
            for item in items:
                # print(item)
                try:
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
                except:
                    pass
            # print(videos)
        except Exception as e:
            logger.info(f'搜索{self.getName()}发生错误:{e}')
        result = {
            'list': videos
        }
        return result

    def playContent(self, play_url,jxs=None):
        if not jxs:
            jxs = []
        if self.lazy:
            print(f'{play_url}->开始执行免嗅代码->{self.lazy}')
            t1 = time()
            try:
                if not str(self.lazy).startswith('js:'):
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
                    # jscode = f'var input={play_url};{jscode}'
                    # print(jscode)
                    py_ctx.update({
                        'input': play_url,
                        'd': self.d,
                        'jxs':jxs,
                        'pdfh': self.d.jsp.pdfh,
                        'pdfa': self.d.jsp.pdfa, 'pd': self.d.jsp.pd,
                    })
                    ctx = py_ctx
                    # print(ctx)
                    t1 = time()
                    jscode = getPreJs() + jscode
                    # print(jscode)
                    loader,_ = runJScode(jscode,ctx=ctx)
                    # print(loader.toString())
                    play_url = loader.eval('input')
                    logger.info(f'js免嗅耗时:{get_interval(t1)}毫秒,播放地址:{play_url}')
            except Exception as e:
                logger.info(f'免嗅耗时:{get_interval(t1)}毫秒,并发生错误:{e}')
            return play_url
        else:
            logger.info(f'播放重定向到:{play_url}')
            return play_url

if __name__ == '__main__':
    from utils import parser
    # js_path = f'js/玩偶姐姐.js'
    # js_path = f'js/555影视.js'
    js_path = f'js/cokemv.js'
    ctx, js_code = parser.runJs(js_path)
    rule = ctx.eval('rule')
    cms = CMS(rule)
    print(cms.title)
    print(cms.homeContent())
    # print(cms.categoryContent('5',1))
    # print(cms.categoryContent('latest',1))
    # print(cms.detailContent(['https://www.2345ka.com/v/45499.html']))
    # print(cms.detailContent(1,['https://cokemv.me/voddetail/40573.html']))
    # cms.categoryContent('dianying',1)
    # print(cms.detailContent(['67391']))
    # print(cms.searchContent('斗罗大陆'))