#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : app.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/8/25
import random
from utils.encode import base64Encode
import js2py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import config
import warnings
warnings.filterwarnings('ignore')

import os
from flask import Flask, jsonify, abort,request,redirect,make_response,render_template,send_from_directory,url_for
from werkzeug.utils import secure_filename
from js.rules import getRuleLists
from utils import error,parser
from utils.web import *
from utils.update import checkUpdate,getOnlineVer,getLocalVer,download_new_version
import sys
import codecs
from classes.cms import CMS,logger
from models import *
import json
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

def create_flask_app(config):
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    # app.config["JSON_AS_ASCII"] = False # jsonify返回的中文正常显示
    app.config.from_object(config)  # 单独的配置文件里写了，这里就不用弄json中文显示了
    # new_conf = get_conf(settings)
    # print(new_conf)
    print('自定义播放解析地址:', app.config.get('PLAY_URL'))
    print('当前操作系统', sys.platform)
    app.logger.name = "drLogger"
    rule_list = getRuleLists()
    wlan_info,_ = get_wlan_info()
    logger.info(rule_list)
    logger.info(f'局域网: {getHost(1, 5705)}/index\n本地: {getHost(0, 5705)}/index\nwlan_info:{wlan_info}')
    return app

app = create_flask_app(config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

now_python_ver = ".".join([str(i) for i in sys.version_info[:3]])
if sys.version_info < (3,9):
    from gevent.pywsgi import WSGIServer
    # from gevent import monkey
    # monkey.patch_socket() # 开启socket异步
    print(f'当前python版本{now_python_ver}为3.9.0及以下,支持gevent')
else:
    print(f'当前python版本{now_python_ver}为3.9.0及以上,不支持gevent')

# from geventwebsocket.handler import WebSocketHandler
RuleClass = rule_classes.init(db)
PlayParse = play_parse.init(db)
lsg = storage.init(db)
print(lsg.setItem('直播地址','https://gitcode.net/qq_26898231/TVBox/-/raw/main/live/zb.txt'))
t12 = time()
print(lsg.getItem('直播地址','111'))
print(get_interval(t12))
def is_linux():
    return not 'win' in sys.platform

def getParmas(key=None,value=''):
    """
    获取链接参数
    :param key:
    :return:
    """
    content_type = request.headers.get('Content-Type')
    args = {}
    if request.method == 'POST':
        if 'application/x-www-form-urlencoded' in content_type or 'multipart/form-data' in content_type:
            args = request.form
        elif 'application/json' in content_type:
            args = request.json
        elif 'text/plain' in content_type:
            args = request.data
        else:
            args = request.args
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
    sup_port = app.config.get('SUP_PORT', False)
    manager0 = ':'.join(getHost(0).split(':')[0:2])
    manager1 = ':'.join(getHost(1).split(':')[0:2])
    manager2 = ':'.join(getHost(2).split(':')[0:2]).replace('https','http')
    if sup_port:
        manager0 += f':{sup_port}'
        manager1 += f':{sup_port}'
        manager2 += f':{sup_port}'
    # print(manager1)
    # print(manager2)
    return render_template('index.html',getHost=getHost,manager0=manager0,manager1=manager1,manager2=manager2,is_linux=is_linux())

@app.route('/admin')
def admin_home():  # 管理员界面
    # headers  = request.headers
    # print(headers)
    cookies = request.cookies
    # print(cookies)
    token = cookies.get('token','')
    # print(f'mytoken:{token}')
    if not verfy_token(token):
        return render_template('login.html')
    # return jsonify(error.success('登录成功'))
    return render_template('admin.html',rules=getRules('js'),ver=getLocalVer())

@app.route('/api/login',methods=['GET','POST'])
def login_api():
    username = getParmas('username')
    password = getParmas('password')
    autologin = getParmas('autologin')
    if not all([username,password]):
        return jsonify(error.failed('账号密码字段必填'))
    token = md5(f'{username};{password}')
    check = verfy_token(token)
    if check:
        # response = make_response(redirect('/admin'))
        response = make_response(jsonify(error.success('登录成功')))
        response.set_cookie('token', token)
        return response
    else:
        return jsonify(error.failed('登录失败,用户名或密码错误'))

@app.route("/admin/view/<name>",methods=['GET'])
def admin_view_rule(name):
    if not name or not name.split('.')[-1] in ['js','txt','py','json']:
        return jsonify(error.failed(f'非法猥亵,未指定文件名。必须包含js|txt|json|py'))
    try:
        return parser.toJs(name,'js')
    except Exception as e:
        return jsonify(error.failed(f'非法猥亵\n{e}'))

@app.route('/admin/clear/<name>')
def admin_clear_rule(name):
    if not name or not name.split('.')[-1] in ['js','txt','py','json']:
        return jsonify(error.failed(f'非法猥亵,未指定文件名。必须包含js|txt|json|py'))
    cookies = request.cookies
    # print(cookies)
    token = cookies.get('token', '')
    # print(f'mytoken:{token}')
    if not verfy_token(token):
        return render_template('login.html')

    file_path = os.path.abspath(f'js/{name}')
    if not os.path.exists(file_path):
        return jsonify(error.failed('服务端没有此文件!'+file_path))
    os.remove(file_path)
    return jsonify(error.success('成功删除文件:'+file_path))

@app.route('/admin/get_ver')
def admin_get_ver():
    cookies = request.cookies
    # print(cookies)
    token = cookies.get('token', '')
    # print(f'mytoken:{token}')
    if not verfy_token(token):
        # return render_template('login.html')
        return jsonify(error.failed('请登录后再试'))

    return jsonify({'local_ver':getLocalVer(),'online_ver':getOnlineVer()})

@app.route('/admin/update_ver')
def admin_update_ver():
    cookies = request.cookies
    # print(cookies)
    token = cookies.get('token', '')
    # print(f'mytoken:{token}')
    if not verfy_token(token):
        # return render_template('login.html')
        return jsonify(error.failed('请登录后再试'))
    msg = download_new_version()
    return jsonify(error.success(msg))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    cookies = request.cookies
    # print(cookies)
    token = cookies.get('token', '')
    # print(f'mytoken:{token}')
    if not verfy_token(token):
        return render_template('login.html')
    if request.method == 'POST':
        try:
            file = request.files['file']
            # print(f.size)
            # print(f)
            # print(request.files)
            filename = secure_filename(file.filename)
            print(f'推荐安全文件命名:{filename}')
            # savePath = f'js/{filename}'
            savePath = f'js/{file.filename}'
            # print(savePath)
            if os.path.exists(savePath):
                return jsonify(error.failed(f'上传失败,文件已存在,请先查看删除再试'))
            with open('js/模板.js', encoding='utf-8') as f2:
                before = f2.read()
            upcode = file.stream.read().decode('utf-8')
            check_to_run = before + upcode
            # print(check_to_run)
            try:
                js2py.eval_js(check_to_run)
            except:
                return jsonify(error.failed('文件上传失败,检测到上传的文件不是drpy框架支持的源代码'))
            print(savePath)
            # savePath = os.path.join('', savePath)
            # print(savePath)
            file.seek(0) # 读取后变成空文件,重新赋能
            file.save(savePath)
            return jsonify(error.success('文件上传成功'))
        except Exception as e:
            return jsonify(error.failed(f'文件上传失败!{e}'))
    else:
        # return render_template('upload.html')
        return jsonify(error.failed('文件上传失败'))

@app.route('/vod')
def vod():
    t0 = time()
    rule = getParmas('rule')
    ext = getParmas('ext')
    if not ext.startswith('http') and not rule:
        return jsonify(error.failed('规则字段必填'))
    rule_list = getRuleLists()
    if not ext.startswith('http') and not rule in rule_list:
        msg = f'服务端本地仅支持以下规则:{",".join(rule_list)}'
        return jsonify(error.failed(msg))
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
        return jsonify(error.failed('爬虫规则加载失败'))

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
    cms = CMS(ruleDict,db,RuleClass,PlayParse,app.config)
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
    t1 = time()
    base_path = path+'/'  # 当前文件所在目录
    # print(base_path)
    os.makedirs(base_path,exist_ok=True)
    file_name = os.listdir(base_path)
    file_name = list(filter(lambda x: str(x).endswith('.js') and str(x).find('模板') < 0, file_name))
    # print(file_name)
    rule_list = [file.replace('.js', '') for file in file_name]
    js_path = [f'{path}/{rule}.js' for rule in rule_list]
    with open('js/模板.js', encoding='utf-8') as f:
        before = f.read()
    rule_codes = []
    # for js in js_path:
    #     with open(js,encoding='utf-8') as f:
    #         code = f.read()
    #         rule_codes.append(js2py.eval_js(before+code))

    ctx = js2py.EvalJs()
    codes = []
    for i in range(len(js_path)):
        js = js_path[i]
        with open(js,encoding='utf-8') as f:
            code = f.read()
            codes.append(code.replace('rule',f'rule{i}',1))
    newCodes = before + '\n'+ '\n'.join(codes)
    # print(newCodes)
    ctx.execute(newCodes)
    for i in range(len(js_path)):
        rule_codes.append(ctx.eval(f'rule{i}'))

    # print(rule_codes)
    # print(type(rule_codes[0]),rule_codes[0])
    # print(rule_codes[0].title)
    # print(rule_codes[0].searchable)
    # print(rule_codes[0].quickSearch)
    new_rule_list = []
    for i in range(len(rule_list)):
        new_rule_list.append({
            'name':rule_list[i],
            'searchable':rule_codes[i].searchable or 0,
            'quickSearch':rule_codes[i].quickSearch or 0,
            'filterable':rule_codes[i].filterable or 0,
        })
    # print(new_rule_list)
    rules = {'list': new_rule_list, 'count': len(rule_list)}
    logger.info(f'自动配置装载耗时:{get_interval(t1)}毫秒')
    return rules

def getPics(path='images'):
    base_path = path+'/'  # 当前文件所在目录
    os.makedirs(base_path,exist_ok=True)
    file_name = os.listdir(base_path)
    # file_name = list(filter(lambda x: str(x).endswith('.js') and str(x).find('模板') < 0, file_name))
    # print(file_name)
    pic_list = [base_path+file for file in file_name]
    # pic_list = file_name
    # print(type(pic_list))
    return pic_list

def getJxs(path='js'):
    with open(f'{path}/解析.conf',encoding='utf-8') as f:
        data = f.read().strip()
    jxs = []
    for i in data.split('\n'):
        i = i.strip()
        dt = i.split(',')
        if not i.startswith('#'):
            jxs.append({
                'name':dt[0],
                'url':dt[1],
                'type':dt[2] if len(dt) > 2 else 0,
                'ua':dt[3] if len(dt) > 3 else UA,
            })
    # jxs = [{'name':dt.split(',')[0],'url':dt.split(',')[1]} for dt in data.split('\n')]
    # jxs = list(filter(lambda x:not str(x['name']).strip().startswith('#'),jxs))
    # print(jxs)
    print(f'共计{len(jxs)}条解析')
    return jxs


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

@app.route('/pics')
def random_pics():
    id = getParmas('id')
    # print(f'id:{id}')
    pics = getPics()
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
        return redirect(config.WALL_PAPER)

def get_live_url(new_conf,mode):
    host = getHost(mode)
    live_url = host + '/lives' if new_conf.get('LIVE_MODE',
                                               1) == 0 else new_conf.get('LIVE_URL',getHost(2)+'/lives')
    live_url = base64Encode(live_url)
    return live_url

@app.route('/config/<int:mode>')
def config_render(mode):
    # print(dict(app.config))
    if mode == 1:
        jyw_ip = getHost(mode)
        logger.info(jyw_ip)
    new_conf = dict(app.config)
    host = getHost(mode)
    jxs = getJxs()
    live_url = get_live_url(new_conf,mode)
    # html = render_template('config.txt',rules=getRules('js'),host=host,mode=mode,jxs=jxs,base64Encode=base64Encode,config=new_conf)
    html = render_template('config.txt',rules=getRules('js'),host=host,mode=mode,jxs=jxs,live_url=live_url,config=new_conf)
    response = make_response(html)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route('/lives')
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

@app.route('/liveslib')
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

@app.route('/configs')
def config_gen():
    # 生成文件
    os.makedirs('txt',exist_ok=True)
    new_conf = dict(app.config)
    jxs = getJxs()
    set_local = render_template('config.txt',rules=getRules('js'),live_url=get_live_url(new_conf,0),mode=0,host=getHost(0),jxs=jxs)
    print(set_local)
    set_area = render_template('config.txt',rules=getRules('js'),live_url=get_live_url(new_conf,1),mode=1,host=getHost(1),jxs=jxs)
    set_online = render_template('config.txt',rules=getRules('js'),live_url=get_live_url(new_conf,2),mode=1,host=getHost(2),jxs=jxs)
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
    return jsonify(error.success('猫配置生成完毕，文件位置在:\n'+'\n'.join(files)))

@app.route("/plugin/<name>",methods=['GET'])
def plugin(name):
    # name=道长影视模板.js
    if not name or not name.split('.')[-1] in ['js','txt','py','json']:
        return jsonify(error.failed(f'非法猥亵,未指定文件名。必须包含js|txt|json|py'))
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
    http_port = int(app.config.get('HTTP_PORT', 5705))
    http_host = app.config.get('HTTP_HOST', '0.0.0.0')
    if sys.version_info < (3, 9):
        # server = WSGIServer(('0.0.0.0', 5705), app, handler_class=WebSocketHandler,log=app.logger)
        # server = WSGIServer(('0.0.0.0', 5705), app, handler_class=WebSocketHandler,log=None)
        server = WSGIServer((http_host, http_port), app,log=logger)
        server.serve_forever()
    else:
        app.run(debug=False, host=http_host, port=http_port)