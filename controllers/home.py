#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : index.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/9/6
import json
import os

from flask import Blueprint,abort,render_template,url_for,redirect,make_response
from controllers.service import storage_service
from controllers.classes import getClasses,getClassInfo
from utils.web import getParmas
from utils.files import getPics
from js.rules import getRules
from base.R import R
from utils.system import cfg,getHost,is_linux
from utils import parser
from utils.log import logger
from utils.files import getAlist,get_live_url
from utils.update import getLocalVer
from js.rules import getJxs
import random

home = Blueprint("home", __name__,static_folder='/static')

@home.route('/')
def forbidden():  # put application's code here
    abort(403)

@home.route('/favicon.ico')  # 设置icon
def favicon():
    # return home.send_static_file('img/favicon.svg')
    return redirect('/static/img/favicon.svg')
    # 对于当前文件所在路径,比如这里是static下的favicon.ico
    # return send_from_directory(os.path.join(app.root_path, 'static'),  'img/favicon.svg', mimetype='image/vnd.microsoft.icon')

@home.route('/index')
def index():
    sup_port = cfg.get('SUP_PORT', False)
    manager0 = ':'.join(getHost(0).split(':')[0:2])
    manager1 = ':'.join(getHost(1).split(':')[0:2])
    manager2 = ':'.join(getHost(2).split(':')[0:2]).replace('https','http')
    if sup_port:
        manager0 += f':{sup_port}'
        manager1 += f':{sup_port}'
        manager2 += f':{sup_port}'
    ver = getLocalVer()
    return render_template('index.html',ver=ver,getHost=getHost,manager0=manager0,manager1=manager1,manager2=manager2,is_linux=is_linux())

@home.route('/rules/clear')
def rules_to_clear():
    return render_template('rules_to_clear.html',rules=getRules(),classes=getClasses())

@home.route('/rules/view')
def rules_to_view():
    return render_template('rules_to_view.html',rules=getRules(),classes=getClasses())

@home.route('/pics')
def random_pics():
    id = getParmas('id')
    # print(f'id:{id}')
    pics = getPics()
    print(pics)
    if len(pics) > 0:
        if id and f'images/{id}.jpg' in pics:
            pic = f'images/{id}.jpg'
        else:
            pic = random.choice(pics)
        file = open(pic, "rb").read()
        response = make_response(file)
        response.headers['Content-Type'] = 'image/jpeg'
        return response
    else:
        return redirect(cfg.WALL_PAPER)

@home.route('/clear')
def clear_rule():
    rule = getParmas('rule')
    if not rule:
        return R.failed('规则字段必填')
    cache_path = os.path.abspath(f'cache/{rule}.js')
    if not os.path.exists(cache_path):
        return R.failed('服务端没有此规则的缓存文件!'+cache_path)
    os.remove(cache_path)
    return R.success('成功删除文件:'+cache_path)

@home.route("/plugin/<name>",methods=['GET'])
def plugin(name):
    # name=道长影视模板.js
    if not name or not name.split('.')[-1] in ['js','txt','py','json']:
        return R.failed(f'非法猥亵,未指定文件名。必须包含js|txt|json|py')
    try:
        return parser.toJs(name)
    except Exception as e:
        return R.failed(f'非法猥亵\n{e}')

@home.route('/lives')
def get_lives():
    live_path = 'js/直播.txt'
    if not os.path.exists(live_path):
        with open(live_path,mode='w+',encoding='utf-8') as f:
            f.write('')

    with open(live_path,encoding='utf-8') as f:
        live_text = f.read()
    response = make_response(live_text)
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return response

@home.route('/liveslib')
def get_liveslib():
    live_path = 'js/custom_spider.jar'
    if not os.path.exists(live_path):
        with open(live_path,mode='w+',encoding='utf-8') as f:
            f.write('')

    with open(live_path,mode='rb') as f:
        live_text = f.read()
    response = make_response(live_text)
    filename = 'custom_spider.jar'
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = f'attachment;filename="{filename}"'
    return response

@home.route('/config/<int:mode>')
def config_render(mode):
    # print(dict(app.config))
    if mode == 1:
        jyw_ip = getHost(mode)
        logger.info(jyw_ip)
    new_conf = cfg
    host = getHost(mode)
    jxs = getJxs()
    alists = getAlist()
    alists_str = json.dumps(alists, ensure_ascii=False)
    live_url = get_live_url(new_conf,mode)
    # html = render_template('config.txt',rules=getRules('js'),host=host,mode=mode,jxs=jxs,base64Encode=base64Encode,config=new_conf)
    html = render_template('config.txt',rules=getRules('js'),host=host,mode=mode,jxs=jxs,alists=alists,alists_str=alists_str,live_url=live_url,config=new_conf)
    response = make_response(html)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@home.route('/configs')
def config_gen():
    # 生成文件
    os.makedirs('txt',exist_ok=True)
    new_conf = cfg
    jxs = getJxs()
    alists = getAlist()
    alists_str = json.dumps(alists,ensure_ascii=False)
    set_local = render_template('config.txt',rules=getRules('js'),alists=alists,alists_str=alists_str,live_url=get_live_url(new_conf,0),mode=0,host=getHost(0),jxs=jxs)
    print(set_local)
    set_area = render_template('config.txt',rules=getRules('js'),alists=alists,alists_str=alists_str,live_url=get_live_url(new_conf,1),mode=1,host=getHost(1),jxs=jxs)
    set_online = render_template('config.txt',rules=getRules('js'),alists=alists,alists_str=alists_str,live_url=get_live_url(new_conf,2),mode=1,host=getHost(2),jxs=jxs)
    with open('txt/pycms0.json','w+',encoding='utf-8') as f:
        set_dict = json.loads(set_local)
        f.write(json.dumps(set_dict,ensure_ascii=False,indent=4))
    with open('txt/pycms1.json','w+',encoding='utf-8') as f:
        set_dict = json.loads(set_area)
        f.write(json.dumps(set_dict,ensure_ascii=False,indent=4))

    with open('txt/pycms2.json','w+',encoding='utf-8') as f:
        set_dict = json.loads(set_online)
        f.write(json.dumps(set_dict,ensure_ascii=False,indent=4))
    files = [os.path.abspath(rf'txt\pycms{i}.json') for i in range(3)]
    # print(files)
    return R.success('猫配置生成完毕，文件位置在:\n'+'\n'.join(files))

@home.route("/info",methods=['get'])
def info_all():
    data = storage_service.query_all()
    return R.ok(data=data)