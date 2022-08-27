#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : app.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/8/25

from flask_sqlalchemy import SQLAlchemy
import config
import warnings
warnings.filterwarnings('ignore')

import os
from flask import Flask, jsonify, abort,request,redirect,make_response,render_template,send_from_directory
from js.rules import getRules
from utils import error,parser
from utils.web import *
import sys
import codecs
from classes.cms import CMS,logger
import json
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

app = Flask(__name__,static_folder='static',static_url_path='/static')

# app.config["JSON_AS_ASCII"] = False # jsonify返回的中文正常显示
app.config.from_object(config) # 单独的配置文件里写了，这里就不用弄json中文显示了
app.logger.name="drLogger"
db = SQLAlchemy(app)

rule_list = getRules()
logger.info(rule_list)
logger.info(f'http://{getHost(1, 5705)}/index\nhttp://localhost:5705/index')

from models import *
from gevent.pywsgi import WSGIServer
# from geventwebsocket.handler import WebSocketHandler

RuleClass = rule_classes.init(db)

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
    # logger.info("进入了首页")
    return render_template('index.html',getHost=getHost)

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
    cms = CMS(rule,db,RuleClass)
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

def getRules(path='cache'):
    base_path = path+'/'  # 当前文件所在目录
    # print(base_path)
    os.makedirs(base_path,exist_ok=True)
    file_name = os.listdir(base_path)
    file_name = list(filter(lambda x: str(x).endswith('.js'), file_name))
    # print(file_name)
    rule_list = [file.replace('.js', '') for file in file_name]
    rules = {'list': rule_list, 'count': len(rule_list)}
    return rules

def getClasses():
    if not db:
        msg = '未提供数据库连接'
        logger.info(msg)
        return []
    res = db.session.query(RuleClass).all()
    return [rc.name for rc in res]

def getClassInfo(cls):
    if not db:
        msg = f'未提供数据库连接,获取{cls}详情失败'
        logger.info(msg)
        return None
    logger.info(f'开始查询{cls}的分类详情')
    res = db.session.query(RuleClass).filter(RuleClass.name == cls).first()
    if res:
        logger.info(str(res))
        return str(res)
    else:
        return f'数据库不存在{cls}的分类缓存'


@app.route('/favicon.ico')  # 设置icon
def favicon():
    return app.send_static_file('img/favicon.svg')
    # 对于当前文件所在路径,比如这里是static下的favicon.ico
    return send_from_directory(os.path.join(app.root_path, 'static'),  'img/favicon.svg', mimetype='image/vnd.microsoft.icon')

@app.route('/cls/<cls>')
def getClassInfoApi(cls):
    info = getClassInfo(cls)
    return jsonify({'msg':info})

@app.route('/clearcls/<cls>')
def clearClassApi(cls):
    logger.info(f'开始查询{cls}的分类详情')
    res = db.session.query(RuleClass).filter(RuleClass.name == cls)
    if res:
        res.delete()
        db.session.commit()
        return jsonify(error.success(f'已清除{cls}的分类缓存'))
    else:
        return jsonify(error.failed(f'数据库不存在{cls}的分类缓存'))

@app.route('/rules')
def rules():
    return render_template('rules.html',rules=getRules(),classes=getClasses())

@app.route('/raw')
def rules_raw():
    return render_template('raw.html',rules=getRules(),classes=getClasses())

@app.route('/config/<int:mode>')
def config_render(mode):
    html = render_template('config.txt',rules=getRules('js'),host=getHost(mode),mode=mode)
    response = make_response(html)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route('/configs')
def config_gen():
    # 生成文件
    set_local = render_template('config.txt',rules=getRules('js'),mode=0,host=getHost(0))
    set_area = render_template('config.txt',rules=getRules('js'),mode=1,host=getHost(1))
    set_online = render_template('config.txt',rules=getRules('js'),mode=1,host=getHost(2))
    with open('pycms0.json','w+',encoding='utf-8') as f:
        set_dict = json.loads(set_local)
        f.write(json.dumps(set_dict,ensure_ascii=False,indent=4))
    with open('pycms1.json','w+',encoding='utf-8') as f:
        set_dict = json.loads(set_area)
        f.write(json.dumps(set_dict,ensure_ascii=False,indent=4))

    with open('pycms2.json','w+',encoding='utf-8') as f:
        set_dict = json.loads(set_online)
        f.write(json.dumps(set_dict,ensure_ascii=False,indent=4))
    files = [os.path.abspath(f'pycms{i}.json') for i in range(3)]
    # print(files)
    return jsonify(error.success('猫配置生成完毕，文件位置在:\n'+'\n'.join(files)))

@app.route("/plugin/<name>",methods=['GET'])
def plugin(name):
    # name=道长影视模板.js
    if not name or not name.split('.')[-1] in ['js','txt','py','json']:
        return jsonify(error.failed(f'非法威胁,未指定文件名。必须包含js|txt|json|py'))
    try:
        return parser.toJs(name)
    except Exception as e:
        return jsonify(error.failed(f'非法猥亵\n{e}'))

def db_test():
    name = '555影视'
    class_name = '电影&连续剧&福利&动漫&综艺'
    class_url = '1&2&124&4&3'
    # data = RuleClass.query.filter(RuleClass.name == '555影视').all()
    res = db.session.query(RuleClass).filter(RuleClass.name == name).first()
    print(res)
    if res:
        res.class_name = class_name
        res.class_url = class_url
        db.session.add(res)
        msg = f'修改成功:{res.id}'
    else:
        res = RuleClass(name=name, class_name=class_name, class_url=class_url)
        db.session.add(res)
        res = db.session.query(RuleClass).filter(RuleClass.name == name).first()
        msg = f'新增成功:{res.id}'

    try:
        db.session.commit()
        return jsonify(error.success(msg))
    except Exception as e:
        return jsonify(error.failed(f'{e}'))

@app.route('/db')
def database():
    return db_test()


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5705)
    # app.run(debug=True, host='0.0.0.0', port=5705)
    # server = WSGIServer(('0.0.0.0', 5705), app, handler_class=WebSocketHandler,log=app.logger)
    server = WSGIServer(('0.0.0.0', 5705), app,log=logger)
    # server = WSGIServer(('0.0.0.0', 5705), app, handler_class=WebSocketHandler,log=None)
    server.serve_forever()
    # WSGIServer(('0.0.0.0', 5705), app,log=None).serve_forever()