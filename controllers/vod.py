#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : vod.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/9/6

from flask import Blueprint,request,render_template,jsonify,make_response,redirect
from time import time
from utils.web import getParmas,get_interval,cfg
from js.rules import getRuleLists,getJxs
from base.R import R
from utils.log import logger
from utils import parser
from controllers.cms import CMS
from base.database import db
from models.ruleclass import RuleClass
from models.playparse import PlayParse
vod = Blueprint("vod", __name__)

@vod.route('/vod')
def vod_home():
    t0 = time()
    rule = getParmas('rule')
    ext = getParmas('ext')
    if not ext.startswith('http') and not rule:
        return R.failed('规则字段必填')
    rule_list = getRuleLists()
    if not ext.startswith('http') and not rule in rule_list:
        msg = f'服务端本地仅支持以下规则:{",".join(rule_list)}'
        return R.failed(msg)
    # logger.info(f'检验耗时:{get_interval(t0)}毫秒')
    t1 = time()
    js_path = f'js/{rule}.js' if not ext.startswith('http') else ext
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
    cms = CMS(ruleDict,db,RuleClass,PlayParse,cfg)
    wd = getParmas('wd')
    ac = getParmas('ac')
    quick = getParmas('quick')
    play = getParmas('play') # 类型为4的时候点击播放会带上来
    flag = getParmas('flag') # 类型为4的时候点击播放会带上来
    filter = getParmas('filter')
    t = getParmas('t')
    pg = getParmas('pg','1')
    pg = int(pg)
    ids = getParmas('ids')
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

    if ac and t: # 一级
        data = cms.categoryContent(t,pg)
        # print(data)
        return jsonify(data)
    if ac and ids: # 二级
        id_list = ids.split(',')
        # print('app:377',len(id_list))
        # print(id_list)
        data = cms.detailContent(pg,id_list)
        # print(data)
        return jsonify(data)
    if wd: # 搜索
        data = cms.searchContent(wd)
        # print(data)
        return jsonify(data)

    # return jsonify({'rule':rule,'js_code':js_code})
    home_data = cms.homeContent(pg)
    return jsonify(home_data)