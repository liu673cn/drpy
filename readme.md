[comment]: <> (#### 🚀dr模板的python实现🚀)
<div align="center">
<h4>🚀第二派-dr模板的python实现🚀</h4>
  <a href="https://alist.nn.ci"><img height="100px" alt="logo" src="https://gitcode.net/qq_32394351/dr_py/-/raw/1fe0e082b1ceacc4469d7f175a605cc2edf0bab0/static/img/icon.png"/></a>
  <p><em>🗂️A webServer convert web and x5 movie sites to cms api data</em></p>
  <a href="https://gitcode.net/qq_32394351/dr_py/-/releases">
    <img src="https://img.shields.io/badge/version-3.6.15-blue" alt="latest version" />
  </a>
  <a href="https://gitcode.net/qq_32394351/dr_py/-/issues">
    <img src="https://img.shields.io/badge/discussions-2-orange" alt="discussions" />
  </a>

  <a href="https://gitcode.net/qq_32394351/dr_py/-/releases">
    <img src="https://img.shields.io/badge/downloads-1325-blue" alt="Downloads" />
  </a>


<a href="https://wwi.lanzoup.com/i02Vp0c3hpkd">
    <img src="https://img.shields.io/badge/蓝奏云下载-3.7.0-blue" alt="Downloads" />
  </a>



<a href="https://hub.docker.com/repository/docker/hjdhnx/drpy">
    <img src="https://img.shields.io/badge/docker镜像主页-drpy-blue" alt="Downloads" />
  </a>

  <a href="https://gitcode.net/qq_32394351/dr_py/-/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/license-AGPL3.0-orange" alt="License" />
  </a>

<a href="https://gitcode.net/qq_32394351/dr_py">
    <img src="https://img.shields.io/badge/coverage-80%25-yellowgreen" alt="License" />
  </a>
</div>  

##### python3.6-3.8完美运行(3.9以上不支持linux进程启动)
<a href="./安卓本地搭建说明.md" alt="install">
<img src="https://img.shields.io/badge/install support-termux|windows|ubuntu|python3.6~python3.8-yellowgreen" />
</a>

[搭建教程](./安卓本地搭建说明.md) | [install_help](./安卓本地搭建说明.md)  |[goorm](./道长乱说.md)  
[dr项目QQ官群](https://qm.qq.com/cgi-bin/qm/qr?k=H2KwcXrMdiR5M2blHR5gjZzPfN_S3N_C&jump_from=webapi)  
[参考T4](https://github.com/sec-an/TV_Spider/blob/main/spider/sp360.py)  
[golang最好的js引擎-otto](https://github.com/robertkrimen/otto)   
[dockerfile教程](https://blog.csdn.net/qq_46158060/article/details/125718218)   
[获取本地设备信息](https://blog.csdn.net/cui_yonghua/article/details/125508991)   
[获取本地设备信息](https://m.jb51.net/article/140716.htm)   
###### 2022/09/22
- [X] 1.v3.7.3修复静态文件阿里token没渲染的bug,修复数据库升级bug,优化app.py
- [X] 2.v3.7.4修复自定义drives合并配置报错问题
###### 2022/09/21
- [X] 1.未来功能增加显示和隐藏多选规则的实际逻辑，增加顺序字段等待有缘人
- [X] 2.版本升级至3.7.0
- [X] 3.版本升级至3.7.1,修复/js目录的内置源会被缓存的问题
- [X] 4.修复鸭奈飞,牛马tv内置源
###### 2022/09/19
- [X] 1.增加20多个缓存源,需要在custom.conf文件自定义添加
- [X] 2.修复缓存js播放免嗅问题
###### 2022/09/17
- [X] 1.pluto1.5.1最新beta版支持drpy首页推荐点击跳drpy内部聚搜(原理同T4)
- [X] 2.pluto1.5.1最新beta版支持searchable为2的源忽略参与聚搜,正常单一搜索
- [X] 3.drpy源增加内部聚搜进入二级详情页的简介签名备注真实来源规则名
###### 2022/09/16
- [X] 1.规则headers合并优化
- [X] 2.基础js功能修复,如pdfh,request,Object.keys
- [X] 3.菜狗改为PC_UA
- [X] 4.增加drpy首页源,实现T4相同功能
- [X] 5.增加多源模式,聚搜超时等后台设置中心
- [X] 6.增加豆瓣首页插件以及详情评分功能,可以custom自定义
- [X] 7.增加嗅探配置,可自定义
- [X] 8.版本升级 至3.6.9
- [X] 9.版本升级 至3.7.10,优化drpy搜索必定成功
###### 2022/09/15
- [X] 1.修复生成配置文件中静态文件链接对应的配置文本爬虫地址渲染异常问题
- [X] 2.删除custom里的xb、xp源
- [X] 3.未来功能页面设置为管理员登录后可见
- [X] 4.修复局域网ip可能会获取成网关地址问题
- [X] 5.设置中心增加自定义进程管理地址(可用于goorm等设备绑定快捷方式)
- [X] 6.直播文件目录迁移
- [X] 7.增加py_gitcafe.py和其他几个js首图2模板源
- [X] 8.版本号更新至3.6.6
- [X] 9.增加了start.sh脚本(感谢Antod提供),配置模板增加leshi的flag
###### 2022/09/14
- [X] 1.升级至3.6.2,增加了一些解析
- [X] 2.升级至3.6.5,修复菜狗部分源解析失败问题(url参数有+号被自动变空格导致的)
###### 2022/09/13
- [X] 1.升级至3.5.8
- [X] 2.迁移alist.conf文件,修改默认模板,增加模板url参数支持fyfilter变量从此支持更多筛选场景
- [X] 3.升级至3.5.9,修复重大bug:模板继承导致的自动生成配置的搜索开关异常问题
- [X] 4.增加菜狗热搜
- [X] 5.修复菜狗源纪录片和综艺
###### 2022/09/12
###### 特别说明:仅pluto 1.4.2以上版本支持此项目的筛选及自定义播放免嗅
- [X] 1.升级至3.5.7
- [X] 2.爱奇艺增加了筛选,修复搜索错误,修复json:表达式取不到数据问题
- [X] 3.尝试增加升级过滤txt目录下通过一键生成的配置文件
- [X] 4.主页增加静态配置文件的链接
- [X] 5.生成静态配置文件也会自动合并自定义配置了
- [ ] 6.拖拽排序源(无限延期,有空再说)
- [ ] 7.隐藏显示源(无限延期,有空再说)
###### 2022/09/11
- [X] 1.升级至3.5.2.后台管理增加设置中心 (可能会存在bug)
- [X] 2.升级至3.5.3.增加菜狗源(筛选及解析播放暂未解决)
- [X] 3.升级至3.5.4 (此版本+pluto1.4.1以上版本支持filter,源示例:菜狗.js)
- [X] 4.升级至3.5.5 (菜狗播放返回json)
###### 2022/09/10
- [X] 1.升级至3.4.4.增加小强迷源,增加二级重定向属性(提供重定向后的源码,让代码重新取重定向过后的线路和播放列表)
- [X] 2.升级至3.4.5.增加兔小贝儿歌源,优化json:细节处理以及详情页拼接细节
- [X] 3.升级至3.4.7 后台管理增加了py源开关
- [X] 4.升级至3.4.8 转移数据库到base目录防止被覆盖,增加js源的tab_exclude属性(线路名称过滤)
- [X] 5.v3.4.8 三架构镜像已发布
###### 2022/09/09
- [X] 1.增加西瓜源,修复一级不支持lazy的bug
- [X] 2.兄弟们dockerhub没法push镜像不知道咋回事,3.4.1的镜像自己用docker目录下的文件build吧
- [X] 3.版本升至3.4.2,增加py源支持,放txt/py目录即可,特别鸣谢Pyramid开发者及xiaoya liu提供的技术和源
- [X] 4.版本升至3.4.3,增加了强制升级功能(本地增量覆盖大法)
###### 2022/09/08
- [X] 1.升级到3.2.9,支持自动合并自定义用户配置(内置t4测试源)
- [X] 2.升级到3.3.0,增加奇珍异兽源
- [X] 3.升级到3.3.2,增加自定义本地文件路由: {{ host }}/files/文件名和{{ host }}/txt/文件名 比如 {{ host }}/files/custom_spider.jar
- [X] 4.升级到3.3.4,修改了默认爬虫jar方案,支持轮询和并发json解析,新增用户自定义解析配置
- [ ] 5.待开发搜索支持js写法(后续再考虑首页推荐支持json双模式+js)
- [X] 6.版本升级3.3.5.搜索支持js写法,并修复了360影视搜索问题(搜索定位标题支持||多个分开合并,解决猫壳自动过滤搜索结果问题,比如月升沧海改名了会被猫壳过滤)
###### 2022/09/07
- [X] 1.优化后台管理登录界面,升级更新脚本
- [X] 2.增加了镜像合并脚本(三合一直接拉 hjdhnx/drpy 即可)
- [X] 3.js源增加cate_exlude参数
- [X] 4.增加腾云驾雾源(二级暂未完善,后面再说)
- [X] 5.完善腾云驾雾源,修复直播下载乱码,修复网站强制证书验证
- [X] 6.升级到3.2.8,增加两套模板和多个对应源
###### 2022/09/06
- [X] 1.增加了后台管理界面在线检测升级系统功能
- [X] 2.增加了后台管理界面修改直播源地址和同步直播源
- [X] 3.首页推荐内容不限制数量(新版pluto牛逼!!!)
- [X] 4.增加lsg配置模型和缓存
- [X] 5.增加了默认alist挂载
- [X] 6.升级到3.2.0,进行了全面后端重构用了蓝图写法,app.py文件以后尽量不动
- [X] 7.后台管理界面显示美化-感谢蓝莓果酱
- [X] 8.打包升级后的三平台镜像(v3.2.1)
- [X] 9.首页美化,升级版本号(v3.2.2)
###### 2022/09/05
- [X] 1.内置jar修复了原本tv_box无法播放直播的问题
- [X] 2.重新构建了三种平台的镜像 amd64,armv7,arm64
- [X] 3.优化日志打印wlan信息
###### 2022/09/04
- [X] 1.增加了dockerfile
- [X] 2.基于dockerfile构建的镜像并上传至dockerhub,小白可以一键运行.参考[搭建教程](./安卓本地搭建说明.md)
###### 2022/09/03
- [X] 1.增加了json定位支持(需要升级依赖),写法为 字符串以json:开头,二级的话含is_json:true
- [X] 2.研究正版线路对接解析(摸索出type1与4的区别，但是不知道1怎么走解析)
- [X] 3.调整linux进程配置自动识别(自动去除https)
- [X] 4.搞定360影视和解析播放
- [X] 5.新增二级支持js写法(参考360影视)
###### 2022/09/02
- [X] 1.优化了免嗅探的注入变量,封装了fetch_params变量
- [X] 2.一定程度兼容python3高版本,支持termux直装(高于3.9版本首页推荐无法获取)
- [X] 3.准备弃坑,基本完结撒花
- [X] 4.增加自定义配置直播外网地址
###### 2022/09/01
- [X] 1.增加动态分类排除配置
- [X] 2.优化pdfh,pdfa,pd等函数,支持多个&&写法,自动取第一个
- [X] 3.增加vfed规则模板
###### 2022/08/31
- [X] 1.增加管理员登录功能
- [X] 2.增加管理员上传和删除内置规则功能
- [X] 3.增加上传文件校验(仅支持pydr的js规则并且100kb以内)
###### 2022/08/30
- [X] 1.增加动态局域网ip获取
- [X] 2.增加js规则热加载(增删改不用重启)
- [X] 3.增加视界的加密库
- [X] 4.增加蓝莓影视免嗅探
- [X] 5.增加免嗅耗时毫秒数统计
- [X] 6.增加自动装载配置
- [X] 7.增加js里单独设置某个源是否可搜索
- [X] 8.增加外网免嗅(自定义config.py里面改)
- [X] 9.增加错误处理和首页单个详情获取
- [X] 10.增加本地直播地址自定义
- [X] 11.增加数据库迁移,[新版教程](https://www.cjavapy.com/article/1977/)  [旧版教程](https://www.cnblogs.com/LoveMoney-MrLi/articles/15765985.html)
- [X] 12.自动ocr识别过搜索验证码
###### 2022/08/29
- [X] 1.更换js引擎,速度更快性能更好
- [X] 2.新版js支持与python互动,后期可能支持js免嗅(lazy:'js:xxx')
- [X] 3.支持了js免嗅和常用的fetch,post方法
- [X] 4.配置uglifyjs可以把js代码压缩到一行(es5不支持多行js)
###### 2022/08/28
- [X] 1.增加linux进程启动,命令 supervisord -c manager.conf
- [X] 2.转移文本文件到txt目录
- [X] 3.增加服务器解析播放(全局配置和js分别配置.后期可以针对性运行解析)
- [X] 4.增加自定义免嗅(基于道长任务仓库核心逻辑实现云函数)
- [X] 5.增加模板继承,优化免嗅参数二
###### 2022/08/27
- [X] 1.增加PC_UA变量
- [X] 2.首页增加更多功能按钮  
- [X] 3.增加猫配置自动生成，分别有本地配置，局域网配置，在线配置
- [X] 4.修复默认网站的favicon图标问题
- [X] 5.增加 flask-sqlalchemy 用于驱动sqlite3数据库
- [X] 6.引入sqlite3数据进行缓存分类定位到的标签
- [ ] 7.增加filter一键爬取和入库(filter_name,filter_url,filter_parse)
- [X] 8.使用gevent作为服务,提升大量性能
###### 2022/08/26
- [X] 1.支持首页推荐功能,模板属性增加limit参数  
- [X] 2.支持纯一级的功能(比如车车网没二级)  
- [X] 3.解决配置首页报错和嗅探播放报错问题
- [X] 4.支持分类第一页独立链接,直接在链接后面加[第一页的独立链接]
- [X] 5.增加headers参数,可以传ua和cookie，此方法解决555影视搜索问题
- [X] 6.增加homeUrl和host参数,以及class_parse参数,可以动态定位分类标签
- [X] 7.获取二级详情函数增加了线程池的使用
- [ ] 8.模板自定义filter过滤
- [X] 9.网页端显示缓存的规则以及提供点击清除缓存操作
- [X] 10.增加本地配置文件，增加指定编码。
- [X] 11.待开发模板渲染器,一键生成猫配置文件。
######  特性说明
1. 参考了海阔视界dr模板设计思路
2. 参考tv_box的t4项目思路重新设计了cms接口

######  本地搭建
1. 安装zero termux
2. 在termux里安装tome 虚拟机
3. tome 虚拟机 里安装ubuntu1804容器
4. ubuntu1804容器里安装python3-pip,nodejs
5. pip3换源并安装requirements.txt(pip3 install -r requirements.txt)
6. python3 app.py运行项目(也可以其他方式nohup或者 supervisord -c manager.conf)
7. 访问地址加/index查看dr_py主页

#### 测试地址
[sqlite3使用教程](https://m.yisu.com/zixun/375448.html)  
[远程网站](http://cms.nokia.press/index)  
[本地网站](http://192.168.10.99:5705/index)  
[gevent下载地址](https://pypi.org/project/gevent/#files)
[aarch64的cp310](http://pan.nokia.press/d/hiker/whl/gevent-21.12.0-cp310-cp310-linux_aarch64.whl)

[comment]: <> ([需要安装nodejs]&#40;https://registry.npmmirror.com/binary.html?path=node/latest-v14.x/&#41;)
[本地服务配置地址](http://localhost:5705/config/0)  
[远程服务配置地址](http://cms.nokia.press/config/2)  

### 配置相关
直接复制对应的三种地址就行了，不需要生成本地文件(下面教程不要了)  
~~本地地址  clan://localhost/pycms_local.json  
推荐把文件放到  /storage/emulated/0/PlutoPlayer/pycms_local.json  
并且pluto要自己切换路径为PlutoPlayer~~

### 相关教程
[pyquery定位](https://blog.csdn.net/Arise007/article/details/79513094)

### 模板规则说明
所有相关属性说明
```javascript
var rule = {
    title:'',//规则标题,没有实际作用,但是可以作为cms类名称依据
    编码:'',//不填就默认utf-8
    host:'',//网页的域名根,包含http头如 https://www,baidu.com
    homeUrl:'/latest/',//网站的首页链接,可以是完整路径或者相对路径,用于分类获取和推荐获取 fyclass是分类标签 fypage是页数
    url:'/fyclass/fypage.html[/fyclass/]',//网站的分类页面链接
    detailUrl:'https://yanetflix.com/voddetail/fyid.html',//非必填,二级详情拼接链接,感觉没啥卵用
    searchUrl:'',//搜索链接 可以是完整路径或者相对路径,用于分类获取和推荐获取 **代表搜索词 fypage代表页数
    searchable:0,//是否启用全局搜索,
    quickSearch:0,//是否启用快速搜索,
    filterable:0,//是否启用筛选,
    filter:{},// 筛选条件字典
    // 筛选网站传参,会自动传到分类链接下(本示例中的url参数)-url里参数为fyfilter,可参考蓝莓影视.js
    filter_url:'style={{fl.style}}&zone={{fl.zone}}&year={{fl.year}}&fee={{fl.fee}}&order={{fl.order}}',
    // 注意,由于猫有配置缓存,搜索配置没法热加载，修改了js不需要重启服务器
    // 但是需要tv_box进设置里换源使配置重新装载
    headers:{//网站的请求头,完整支持所有的,常带ua和cookies
        'User-Agent':'MOBILE_UA',
        "Cookie": "searchneed=ok"
    },
    timeout:5000,//网站的全局请求超时,默认是3000毫秒
    class_name:'电影&电视剧&动漫&综艺',//静态分类名称拼接
    class_url:'1&2&3&4',//静态分类标识拼接
    //动态分类获取 列表;标题;链接;正则提取 不需要正则的时候后面别加分号
    class_parse:'#side-menu:lt(1) li;a&&Text;a&&href;com/(.*?)/',
    // 除开全局过滤之外还需要过滤哪些标题不视为分类
    cate_exclude:'',
    // 除开全局动态线路名过滤之外还需要过滤哪些线路名标题不视为线路
    tab_exclude:'',
    // 服务器解析播放
    play_parse:true,
    // 自定义免嗅
    lazy:'',
    // 首页推荐显示数量
    limit:6,
    double:true,//是否双层列表定位,默认false
    // 类似海阔一级 列表;标题;图片;描述;链接;详情 其中最后一个参数选填
    // 如果是双层定位的话,推荐的第2段分号代码也是第2层定位列表代码
    推荐:'.col-sm-6;h3&&Text;img&&data-src;.date&&Text;a&&href',
    // 类似海阔一级 列表;标题;图片;描述;链接;详情 其中最后一个参数选填
    一级:'.col-sm-6;h3&&Text;img&&data-src;.date&&Text;a&&href',
    // 二级可以是*,表示规则无二级,直接拿一级的链接进行嗅探
    // 或者 {title:'',img:'',desc:'',content:'',tabs:'',lists:''} 同海阔dr二级
    二级:'*',
    // 搜索可以是*,集成一级，或者跟一级一样的写法 列表;标题;图片;描述;链接;详情
    搜索:'*',
}
```
模板继承写法
```javascript
var rule = Object.assign(muban.mxpro,{
title:'鸭奈飞',
host:'https://yanetflix.com',
url:'/index.php/vod/show/id/fyclass/page/fypage.html',
class_parse:'.navbar-items li:gt(1):lt(6);a&&Text;a&&href;.*/(.*?).html',
});
```