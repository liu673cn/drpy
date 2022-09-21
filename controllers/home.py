#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : index.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/9/6
import json
import os


from flask import Blueprint,abort,render_template,render_template_string,url_for,redirect,make_response,send_from_directory
from controllers.service import storage_service,rules_service
from controllers.classes import getClasses,getClassInfo

from utils.files import getPics,custom_merge,getAlist,get_live_url,get_multi_rules,getCustonDict
from js.rules import getRules,getPys
from utils.encode import parseText
from base.R import R
from utils.system import getHost,is_linux
from utils.cfg import cfg
from utils import parser
from utils.ua import time,get_interval
from utils.log import logger
from utils.update import getLocalVer,getHotSuggest
from js.rules import getJxs
import random
from utils.web import getParmas


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
    sup_port = cfg.get('SUP_PORT', 9001)
    lsg = storage_service()
    pid_url = lsg.getItem('PID_URL')
    manager0 = ':'.join(getHost(0).split(':')[0:2])
    manager1 = ':'.join(getHost(1).split(':')[0:2])
    manager2 = pid_url or ':'.join(getHost(2).split(':')[0:2]).replace('https','http')
    if sup_port:
        manager0 += f':{sup_port}'
        manager1 += f':{sup_port}'
        if not pid_url:
            manager2 += f':{sup_port}'
    # print(manager2)
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
    # print(pics)
    new_conf = cfg
    lsg = storage_service()
    store_conf_dict = lsg.getStoreConfDict()
    new_conf.update(store_conf_dict)
    if not new_conf.WALL_PAPER and len(pics) > 0:
        if id and f'images/{id}.jpg' in pics:
            pic = f'images/{id}.jpg'
        else:
            pic = random.choice(pics)
        file = open(pic, "rb").read()
        response = make_response(file)
        response.headers['Content-Type'] = 'image/jpeg'
        return response
    else:
        return redirect(new_conf.WALL_PAPER)

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

@home.route('/files/<name>')
def get_files(name):
    base_path = 'base/files'
    os.makedirs(base_path,exist_ok=True)
    file_path = os.path.join(base_path, f'{name}')
    if not os.path.exists(file_path):
        return R.failed(f'{file_path}文件不存在')

    with open(file_path, mode='rb') as f:
        file_byte = f.read()
    response = make_response(file_byte)
    filename = name
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = f'attachment;filename="{filename}"'
    return response

@home.route('/txt/<path:filename>')
def custom_static(filename):
    # 自定义静态目录 {{ url_for('custom_static',filename='help.txt')}}
    # print(filename)
    return send_from_directory('txt', filename)

# @home.route('/txt/<name>')
# def get_txt_files(name):
#     base_path = 'txt'
#     os.makedirs(base_path,exist_ok=True)
#     file_path = os.path.join(base_path, f'{name}')
#     if not os.path.exists(file_path):
#         return R.failed(f'{file_path}文件不存在')
#
#     with open(file_path, mode='r',encoding='utf-8') as f:
#         file_byte = f.read()
#     response = make_response(file_byte)
#     response.headers['Content-Type'] = 'text/plain; charset=utf-8'
#     return response


@home.route('/lives')
def get_lives():
    live_path = 'base/直播.txt'
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

@home.route('/hotsugg')
def get_hot_search():
    data = getHotSuggest()
    return R.success('获取成功',data)

def merged_hide(merged_config):
    t1 = time()
    store_rule = rules_service()
    hide_rules = store_rule.getHideRules()
    hide_rule_names = list(map(lambda x: x['name'], hide_rules))
    # print(hide_rule_names)
    all_cnt = len(merged_config['sites'])

    def filter_show(x):
        name = x['api'].split('rule=')[1].split('&')[0] if 'rule=' in x['api'] else x['key']
        # print(name)
        return name not in hide_rule_names

    merged_config['sites'] = list(filter(filter_show, merged_config['sites']))
    logger.info(f'数据库筛选隐藏规则耗时{get_interval(t1)}毫秒,共计{all_cnt}条规则,隐藏后可渲染{len(merged_config["sites"])}条规则')

@home.route('/config/<int:mode>')
def config_render(mode):
    # print(dict(app.config))
    if mode == 1:
        jyw_ip = getHost(mode)
        logger.info(jyw_ip)
    new_conf = cfg
    lsg = storage_service()
    store_conf_dict = lsg.getStoreConfDict()
    new_conf.update(store_conf_dict)
    # print(type(new_conf),new_conf)
    host = getHost(mode)
    # ali_token = lsg.getItem('ALI_TOKEN')
    ali_token = new_conf.ALI_TOKEN
    # print(ali_token)
    customConfig = getCustonDict(host,ali_token)
    # print(customConfig)
    jxs = getJxs()
    lsg = storage_service()
    use_py = lsg.getItem('USE_PY')
    pys = getPys() if use_py else []
    # print(pys)
    alists = getAlist()
    alists_str = json.dumps(alists, ensure_ascii=False)
    live_url = get_live_url(new_conf,mode)
    rules = getRules('js')
    rules = get_multi_rules(rules)
    # html = render_template('config.txt',rules=getRules('js'),host=host,mode=mode,jxs=jxs,base64Encode=base64Encode,config=new_conf)
    html = render_template('config.txt',pys=pys,rules=rules,host=host,mode=mode,jxs=jxs,alists=alists,alists_str=alists_str,live_url=live_url,config=new_conf)
    merged_config = custom_merge(parseText(html),customConfig)
    # print(merged_config['sites'])

    merged_hide(merged_config)
    # response = make_response(html)
    # print(len(merged_config['sites']))
    response = make_response(json.dumps(merged_config,ensure_ascii=False,indent=1))
    # response = make_response(str(merged_config))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@home.route('/configs')
def config_gen():
    # 生成文件
    os.makedirs('txt',exist_ok=True)
    new_conf = cfg
    lsg = storage_service()
    store_conf_dict = lsg.getStoreConfDict()
    new_conf.update(store_conf_dict)
    try:
        jxs = getJxs()
        lsg = storage_service()
        use_py = lsg.getItem('USE_PY')
        pys = getPys() if use_py else False
        alists = getAlist()
        alists_str = json.dumps(alists,ensure_ascii=False)
        rules = getRules('js')
        rules = get_multi_rules(rules)
        set_local = render_template('config.txt',pys=pys,rules=rules,alists=alists,alists_str=alists_str,live_url=get_live_url(new_conf,0),mode=0,host=getHost(0),jxs=jxs)
        # print(set_local)
        set_area = render_template('config.txt',pys=pys,rules=rules,alists=alists,alists_str=alists_str,live_url=get_live_url(new_conf,1),mode=1,host=getHost(1),jxs=jxs)
        set_online = render_template('config.txt',pys=pys,rules=rules,alists=alists,alists_str=alists_str,live_url=get_live_url(new_conf,2),mode=1,host=getHost(2),jxs=jxs)
        ali_token = new_conf.ALI_TOKEN
        with open('txt/pycms0.json','w+',encoding='utf-8') as f:
            customConfig = getCustonDict(getHost(0),ali_token)
            set_dict = custom_merge(parseText(set_local), customConfig)
            merged_hide(set_dict)
            # set_dict = json.loads(set_local)
            f.write(json.dumps(set_dict,ensure_ascii=False,indent=4))
        with open('txt/pycms1.json','w+',encoding='utf-8') as f:
            customConfig = getCustonDict(getHost(1),ali_token)
            set_dict = custom_merge(parseText(set_area), customConfig)
            merged_hide(set_dict)
            # set_dict = json.loads(set_area)
            f.write(json.dumps(set_dict,ensure_ascii=False,indent=4))

        with open('txt/pycms2.json','w+',encoding='utf-8') as f:
            customConfig = getCustonDict(getHost(2),ali_token)
            set_dict = custom_merge(parseText(set_online), customConfig)
            merged_hide(set_dict)
            # set_dict = json.loads(set_online)
            f.write(json.dumps(set_dict,ensure_ascii=False,indent=4))
        files = [os.path.abspath(rf'txt\pycms{i}.json') for i in range(3)]
        # print(files)
        return R.success('猫配置生成完毕，文件位置在:\n'+'\n'.join(files))
    except Exception as e:
        return R.failed(f'配置文件生成错误:\n{e}')

@home.route("/info",methods=['get'])
def info_all():
    data = storage_service.query_all()
    return R.ok(data=data)