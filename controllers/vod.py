#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : vod.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/9/6
import json

from flask import Blueprint,request,render_template,jsonify,make_response,redirect
from time import time
from utils.web import getParmas,get_interval
from utils.cfg import cfg
from js.rules import getRuleLists,getJxs
from base.R import R
from utils.log import logger
from utils import parser
from controllers.cms import CMS
from base.database import db
from models.ruleclass import RuleClass
from models.playparse import PlayParse
from js.rules import getRules
from controllers.service import storage_service
from concurrent.futures import ThreadPoolExecutor,as_completed,thread  # 引入线程池
vod = Blueprint("vod", __name__)


def search_one(rule, wd, before: str = ''):
    t1 = time()
    if not before:
        with open('js/模板.js', encoding='utf-8') as f:
            before = f.read()
    js_path = f'js/{rule}.js'
    try:
        ctx, js_code = parser.runJs(js_path, before=before)
        if not js_code:
            return None
        ruleDict = ctx.rule.to_dict()
        ruleDict['id'] = rule  # 把路由请求的id装到字典里,后面播放嗅探才能用
        logger.info(f'规则{rule}装载耗时:{get_interval(t1)}毫秒')
        cms = CMS(ruleDict, db, RuleClass, PlayParse, cfg)
        data = cms.searchContent(wd, show_name=True)
        return data
    except Exception as e:
        print(f'{rule}发生错误:{e}')
        return None

def multi_search2(wd):
    t1 = time()
    lsg = storage_service()
    try:
        timeout = round(int(lsg.getItem('SEARCH_TIMEOUT', 5000)) / 1000, 2)
    except:
        timeout = 5
    rules = getRules('js')['list']
    rule_names = list(map(lambda x: x['name'], rules))
    rules_exclude = ['drpy']
    new_rules = list(filter(lambda x: x.get('searchable', 0) and x.get('name', '') not in rules_exclude, rules))
    search_sites = [new_rule['name'] for new_rule in new_rules]
    nosearch_sites = set(rule_names) ^ set(search_sites)
    nosearch_sites.remove('drpy')
    # print(nosearch_sites)
    logger.info(f'开始聚搜{wd},共计{len(search_sites)}个规则,聚搜超时{timeout}秒')
    logger.info(f'不支持聚搜的规则,共计{len(nosearch_sites)}个规则:{",".join(nosearch_sites)}')
    # print(search_sites)
    res = []
    with open('js/模板.js', encoding='utf-8') as f:
        before = f.read()
    logger.info(f'聚搜准备工作耗时:{get_interval(t1)}毫秒')
    t2 = time()
    thread_pool = ThreadPoolExecutor(len(search_sites))  # 定义线程池来启动多线程执行此任务
    obj_list = []
    try:
        for site in search_sites:
            obj = thread_pool.submit(search_one, site, wd, before)
            obj_list.append(obj)
        thread_pool.shutdown(wait=True)  # 等待所有子线程并行完毕
        vod_list = [obj.result() for obj in obj_list]
        for vod in vod_list:
            if vod and isinstance(vod, dict) and vod.get('list') and len(vod['list']) > 0:
                res.extend(vod['list'])
        result = {
            'list': res
        }
        logger.info(f'drpy聚搜{len(search_sites)}个源耗时{get_interval(t2)}毫秒,含准备共计耗时{get_interval(t1)}毫秒')
    except Exception as e:
        result = {
            'list': []
        }
        logger.info(f'drpy聚搜{len(search_sites)}个源耗时{get_interval(t2)}毫秒,含准备共计耗时:{get_interval(t1)}毫秒,发生错误:{e}')
    return jsonify(result)


def multi_search(wd):
    lsg = storage_service()
    t1 = time()
    try:
        timeout = round(int(lsg.getItem('SEARCH_TIMEOUT',5000))/1000,2)
    except:
        timeout = 5
    rules = getRules('js')['list']
    rule_names = list(map(lambda x:x['name'],rules))
    rules_exclude = ['drpy']
    new_rules = list(filter(lambda x: x.get('searchable', 0) and x.get('name', '') not in rules_exclude, rules))
    search_sites = [new_rule['name'] for new_rule in new_rules]
    nosearch_sites = set(rule_names) ^ set(search_sites)
    nosearch_sites.remove('drpy')
    # print(nosearch_sites)
    logger.info(f'开始聚搜{wd},共计{len(search_sites)}个规则,聚搜超时{timeout}秒')
    logger.info(f'不支持聚搜的规则,共计{len(nosearch_sites)}个规则:{",".join(nosearch_sites)}')
    # print(search_sites)
    res = []
    with open('js/模板.js', encoding='utf-8') as f:
        before = f.read()
    with ThreadPoolExecutor(max_workers=len(search_sites)) as executor:
        to_do = []
        for site in search_sites:
            future = executor.submit(search_one, site, wd, before)
            to_do.append(future)
        try:
            for future in as_completed(to_do, timeout=timeout):  # 并发执行
                ret = future.result()
                # print(ret)
                if ret and isinstance(ret,dict) and ret.get('list'):
                    res.extend(ret['list'])
        except Exception as e:
            print(f'发生错误:{e}')
            import atexit
            atexit.unregister(thread._python_exit)
            executor.shutdown = lambda wait: None
    logger.info(f'drpy聚搜{len(search_sites)}个源共计耗时{get_interval(t1)}毫秒')
    return jsonify({
        "list": res
    })

@vod.route('/vod')
def vod_home():
    t0 = time()
    rule = getParmas('rule')
    ac = getParmas('ac')
    ids = getParmas('ids')
    if ac and ids and ids.find('#') > -1:  # 聚搜的二级
        id_list = ids.split(',')
        rule = id_list[0].split('#')[1]
        # print(rule)

    ext = getParmas('ext')
    filters = getParmas('f')
    tp = getParmas('type')
    # print(f'type:{tp}')
    # if not ext.startswith('http') and not rule:
    if not rule:
        return R.failed('规则字段必填')
    rule_list = getRuleLists()
    # if not ext.startswith('http') and not rule in rule_list:
    if not ext and not rule in rule_list:
        msg = f'服务端本地仅支持以下规则:{",".join(rule_list)}'
        return R.failed(msg)
    # logger.info(f'检验耗时:{get_interval(t0)}毫秒')
    t1 = time()
    # js_path = f'js/{rule}.js' if not ext.startswith('http') else ext
    js_path = f'js/{rule}.js' if not ext else ext
    with open('js/模板.js', encoding='utf-8') as f:
        before = f.read()
    # logger.info(f'js读取耗时:{get_interval(t1)}毫秒')
    logger.info(f'参数检验js读取共计耗时:{get_interval(t0)}毫秒')
    t2 = time()
    ctx, js_code = parser.runJs(js_path,before=before)
    if not js_code:
        return R.failed('爬虫规则加载失败')

    # rule = ctx.eval('rule')
    # print(type(ctx.rule.lazy()),ctx.rule.lazy().toString())
    ruleDict = ctx.rule.to_dict()
    ruleDict['id'] = rule  # 把路由请求的id装到字典里,后面播放嗅探才能用
    # print(ruleDict)
    # print(rule)
    # print(type(rule))
    # print(ruleDict)
    logger.info(f'js装载耗时:{get_interval(t2)}毫秒')
    # print(ruleDict)
    # print(rule)
    cms = CMS(ruleDict,db,RuleClass,PlayParse,cfg,ext)
    wd = getParmas('wd')
    quick = getParmas('quick')
    play = getParmas('play') # 类型为4的时候点击播放会带上来
    flag = getParmas('flag') # 类型为4的时候点击播放会带上来
    # myfilter = getParmas('filter')
    t = getParmas('t')
    pg = getParmas('pg','1')
    pg = int(pg)
    q = getParmas('q')
    play_url = getParmas('play_url')

    if play:
        jxs = getJxs()
        play_url = play.split('play_url=')[1]
        play_url = cms.playContent(play_url, jxs,flag)
        if isinstance(play_url, str):
            # return redirect(play_url)
            # return jsonify({'parse': 0, 'playUrl': play_url, 'jx': 0, 'url': play_url})
            # return jsonify({'parse': 0, 'playUrl': play_url, 'jx': 0, 'url': ''})
            return jsonify({'parse': 0, 'playUrl': '', 'jx': 0, 'url': play_url})
        elif isinstance(play_url, dict):
            return jsonify(play_url)
        else:
            return play_url

    if play_url:  # 播放
        jxs = getJxs()
        play_url = cms.playContent(play_url,jxs)
        if isinstance(play_url,str):
            return redirect(play_url)
        elif isinstance(play_url,dict):
            return jsonify(play_url)
        else:
            return play_url

    if ac and t:  # 一级
        fl = {}
        if filters and filters.find('{') > -1 and filters.find('}') > -1:
            fl = json.loads(filters)
        # print(filters,type(filters))
        # print(fl,type(fl))
        data = cms.categoryContent(t,pg,fl)
        # print(data)
        return jsonify(data)
    if ac and ids: # 二级
        id_list = ids.split(',')
        show_name = False
        if ids.find('#') > -1:
            id_list = list(map(lambda x:x.split('#')[0],id_list))
            show_name = True
        # print('app:377',len(id_list))
        # print(id_list)
        data = cms.detailContent(pg,id_list,show_name)
        # print(data)
        return jsonify(data)
    if wd: # 搜索
        if rule == 'drpy':
            # print(f'准备单独处理聚合搜索:{wd}')
            return multi_search(wd)
            # return multi_search2(wd)
        else:
            data = cms.searchContent(wd)
            # print(data)
            return jsonify(data)
    # return jsonify({'rule':rule,'js_code':js_code})
    home_data = cms.homeContent(pg)
    return jsonify(home_data)