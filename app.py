#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : app.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/8/25
import os

from flask import Flask, jsonify, abort,request,redirect,make_response,render_template
from js.rules import getRules
from utils import error,parser
import sys
import codecs
from models.cms import CMS
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

app = Flask(__name__,static_folder='static',static_url_path='/static')
app.config["JSON_AS_ASCII"] = False  # jsonify返回的中文正常显示
from utils.web import *
rule_list = getRules()
print(rule_list)

def getParmas(key=None,value=''):
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
        return args.get(key,value)
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
    ext = getParmas('ext')
    if not ext.startswith('http') and not rule:
        return jsonify(error.failed('规则字段必填'))
    if not ext.startswith('http') and not rule in rule_list:
        msg = f'服务端本地仅支持以下规则:{",".join(rule_list)}'
        return jsonify(error.failed(msg))

    js_path = f'js/{rule}.js' if not ext.startswith('http') else ext
    ctx,js_code = parser.runJs(js_path)
    if not js_code:
        return jsonify(error.failed('爬虫规则加载失败'))
    rule = ctx.eval('rule')
    cms = CMS(rule)
    wd = getParmas('wd')
    ac = getParmas('ac')
    quick = getParmas('quick')
    play = getParmas('play')
    flag = getParmas('flag')
    filter = getParmas('filter')
    t = getParmas('t')
    pg = getParmas('pg','1')
    pg = int(pg)
    ids = getParmas('ids')
    q = getParmas('q')

    if ac and t: # 一级
        data = cms.categoryContent(t,pg)
        # print(data)
        return jsonify(data)
    if ac and ids: # 二级
        id_list = ids.split(',')
        # print(len(id_list))
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

@app.route('/clear')
def clear():
    rule = getParmas('rule')
    if not rule:
        return jsonify(error.failed('规则字段必填'))
    cache_path = os.path.abspath(f'cache/{rule}.js')
    if not os.path.exists(cache_path):
        return jsonify(error.failed('服务端没有此规则的缓存文件!'+cache_path))
    os.remove(cache_path)
    return jsonify(error.success('成功删除文件:'+cache_path))

@app.route('/rules')
def rules():
    # base_path = os.path.dirname(os.path.abspath(__file__))+'cache'  # 当前文件所在目录
    base_path = 'cache/'  # 当前文件所在目录
    print(base_path)
    file_name = os.listdir(base_path)
    file_name = list(filter(lambda x: str(x).endswith('.js'), file_name))
    # print(file_name)
    rule_list = [file.replace('.js', '') for file in file_name]
    rules = {'list':rule_list,'count':len(rule_list)}
    # print(rule_list)
    # return jsonify(obj)
    return render_template('rules.html',rules=rules)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5705)
    # app.run(debug=True, host='0.0.0.0', port=5705)