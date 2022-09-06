#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : admin.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/9/6
import os

from flask import Blueprint,request,render_template,jsonify,make_response
from controllers.service import storage_service
from base.R import R
from utils.web import verfy_token
from utils.update import getLocalVer,getOnlineVer,download_new_version,download_lives
from utils import parser
from utils.web import getParmas
from js.rules import getRules
from utils.parser import runJScode
from werkzeug.utils import secure_filename
import js2py
from utils.web import md5

admin = Blueprint("admin", __name__)

# @admin.route("/",methods=['get'])
# def index():
#     return R.ok(msg='欢迎进入首页',data=None)

# @admin.route("/info",methods=['get'])
# def info_all():
#     data = storage_service.query_all()
#     return R.ok(data=data)

@admin.route('/')
def admin_index():  # 管理员界面
    lsg = storage_service()
    live_url = lsg.getItem('LIVE_URL')
    print(f'live_url:',live_url)
    if not verfy_token():
        return render_template('login.html')
    live_url = lsg.getItem('LIVE_URL')
    return render_template('admin.html', rules=getRules('js'), ver=getLocalVer(), live_url=live_url)

@admin.route("/view/<name>",methods=['GET'])
def admin_view_rule(name):
    if not name or not name.split('.')[-1] in ['js','txt','py','json']:
        return R.error(f'非法猥亵,未指定文件名。必须包含js|txt|json|py')
    try:
        return parser.toJs(name,'js')
    except Exception as e:
        return R.error(f'非法猥亵\n{e}')

@admin.route('/clear/<name>')
def admin_clear_rule(name):
    if not name or not name.split('.')[-1] in ['js','txt','py','json']:
        return R.error(f'非法猥亵,未指定文件名。必须包含js|txt|json|py')
    if not verfy_token():
        return render_template('login.html')

    file_path = os.path.abspath(f'js/{name}')
    print(file_path)
    if not os.path.exists(file_path):
        return R.error('服务端没有此文件!'+file_path)
    os.remove(file_path)
    return R.ok('成功删除文件:'+file_path)

@admin.route('/get_ver')
def admin_get_ver():
    if not verfy_token():
        # return render_template('login.html')
        return R.error('请登录后再试')

    return jsonify({'local_ver':getLocalVer(),'online_ver':getOnlineVer()})

@admin.route('/update_ver')
def admin_update_ver():
    if not verfy_token():
        return R.failed('请登录后再试')
    msg = download_new_version()
    return R.success(msg)

@admin.route('/update_lives')
def admin_update_lives():
    url = getParmas('url')
    if not url:
        return R.failed('未提供被同步的直播源远程地址!')
    if not verfy_token():
        return R.failed('请登录后再试')
    live_url = url
    success = download_lives(live_url)
    if success:
        return R.success(f'直播源{live_url}同步成功')
    else:
        return R.failed(f'直播源{live_url}同步失败')

@admin.route('/write_live_url')
def admin_write_live_url():
    url = getParmas('url')
    if not url:
        return R.failed('未提供修改后的直播源地址!')
    if not verfy_token():
        return R.failed('请登录后再试')
    lsg = storage_service()
    id = lsg.setItem('LIVE_URL',url)
    msg = f'已修改的配置记录id为:{id}'
    return R.success(msg)

@admin.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if not verfy_token():
        return render_template('login.html')
    if request.method == 'POST':
        try:
            file = request.files['file']
            filename = secure_filename(file.filename)
            print(f'推荐安全文件命名:{filename}')
            savePath = f'js/{file.filename}'
            if os.path.exists(savePath):
                return R.failed(f'上传失败,文件已存在,请先查看删除再试')
            with open('js/模板.js', encoding='utf-8') as f2:
                before = f2.read()
            upcode = file.stream.read().decode('utf-8')
            check_to_run = before + upcode
            # print(check_to_run)
            try:
                # js2py.eval_js(check_to_run)
                loader, _ = runJScode(check_to_run)
                rule = loader.eval('rule')
                if not rule:
                    return R.failed('文件上传失败,检测到上传的文件不是drpy框架支持的源代码')
            except:
                return R.failed('文件上传失败,检测到上传的文件不是drpy框架支持的源代码')
            print(savePath)
            file.seek(0) # 读取后变成空文件,重新赋能
            file.save(savePath)
            return R.success('文件上传成功')
        except Exception as e:
            return R.failed(f'文件上传失败!{e}')
    else:
        # return render_template('upload.html')
        return R.failed('文件上传失败')

@admin.route('/login',methods=['GET','POST'])
def login_api():
    username = getParmas('username')
    password = getParmas('password')
    autologin = getParmas('autologin')
    if not all([username,password]):
        return R.failed('账号密码字段必填')
    token = md5(f'{username};{password}')
    check = verfy_token(token=token)
    if check:
        # response = make_response(redirect('/admin'))
        response = make_response(R.success('登录成功'))
        response.set_cookie('token', token)
        return response
    else:
        return R.failed('登录失败,用户名或密码错误')