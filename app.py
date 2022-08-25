#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : app.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/8/25

from flask import Flask, jsonify, abort,request,redirect,make_response,render_template
from js.rules import rule_list
from utils import error,parser
import sys
import codecs
from models.cms import CMS
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False  # jsonify返回的中文正常显示
from utils.web import *

def getParmas(key=None):
    """
    获取链接参数
    :param key:
    :return:
    """
    args = {}
    if request.method == 'POST':
        args = request.json
    elif request.method == 'GET':
        args = request.args
    if key:
        return args.get(key,'')
    else:
        return args

@app.route('/')
def forbidden():  # put application's code here
    abort(403)

@app.route('/index')
def index():  # put application's code here
    return render_template('index.html')

@app.route('/vod')
def vod():
    rule = getParmas('rule')
    if not rule:
        return jsonify(error.failed('规则字段必填'))
    if not rule in rule_list:
        msg = f'仅支持以下规则:{",".join(rule_list)}'
        return jsonify(error.failed(msg))

    js_path = f'js/{rule}.js'
    ctx,js_code = parser.runJs(js_path)
    rule = ctx.eval('rule')
    cms = CMS(rule)
    wd = getParmas('wd')
    ac = getParmas('ac')
    quick = getParmas('quick')
    play = getParmas('play')
    flag = getParmas('flag')
    filter = getParmas('filter')
    t = getParmas('t')
    pg = getParmas('pg')
    ext = getParmas('ext')
    ids = getParmas('ids')
    q = getParmas('q')

    if ac and t: # 一级
        data = cms.categoryContent(t,pg)
        # print(data)
        return jsonify(data)
    if ac and ids: # 二级
        data = cms.detailContent(ids.split(','))
        # print(data)
        return jsonify(data)
    if wd: # 搜索
        data = cms.searchContent(wd)
        # print(data)
        return jsonify(data)

    # return jsonify({'rule':rule,'js_code':js_code})
    home_data = cms.homeContent()
    return jsonify(home_data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000)