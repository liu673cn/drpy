#### dr模板的python实现
###### 更新日志
###### 2022/08/27
- [X] 1.增加PC_UA变量
- [X] 2.首页增加更多功能按钮  
- [X] 3.增加猫配置自动生成，分别有本地配置，局域网配置，在线配置
- [ ] 4.引入sqlite3数据进行缓存分类定位到的标签
- [ ] 5.增加filter一键爬取和入库(filter_name,filter_url,filter_parse)
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
- [ ] 11.待开发模板渲染器,一键生成猫配置文件。
######  特性说明
1. 参考了海阔视界dr模板设计思路
2. 参考tv_box的t4项目思路重新设计了cms接口

######  本地搭建
1. 安装zero termux
2. 在termux里安装tome 虚拟机
3. tome 虚拟机 里安装ubuntu1804容器
4. ubuntu1804容器里安装python3-pip,nodejs
5. pip3换源并安装requirements.txt
6. python3 app.py运行项目(也可以其他方式)
7. 访问地址加/index查看dr_py主页

#### 测试地址
[远程网站](http://cms.nokia.press/index)  
[本地网站](http://192.168.10.99:5705/index)  
[需要安装nodejs](https://registry.npmmirror.com/binary.html?path=node/latest-v14.x/)  
[本地服务配置地址](http://localhost:5705/config/0)  
[远程服务配置地址](http://cms.nokia.press/config/1)  

### 配置相关
本地地址  clan://localhost/pycms_local.json  
推荐把文件放到  /storage/emulated/0/PlutoPlayer/pycms_local.json  
并且pluto要自己切换路径为PlutoPlayer

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
    headers:{//网站的请求头,完整支持所有的,常带ua和cookies
        'User-Agent':'MOBILE_UA',
        "Cookie": "searchneed=ok"
    },
    timeout:5000,//网站的全局请求超时,默认是3000毫秒
    class_name:'电影&电视剧&动漫&综艺',//静态分类名称拼接
    class_url:'1&2&3&4',//静态分类标识拼接
    //动态分类获取 列表;标题;链接;正则提取 不需要正则的时候后面别加分号
    class_parse:'#side-menu:lt(1) li;a&&Text;a&&href;com/(.*?)/',
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