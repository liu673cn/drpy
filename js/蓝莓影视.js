var rule = {
    title:'蓝莓影视1',
    host:'https://lanmeiguojiang.com',
    // homeUrl:'/',
    url:'/show/fyclass--------fypage---.html',
    headers:{
        'User-Agent':'MOBILE_UA'
    },
    searchUrl:'/search/**-fypage.html',
    // class_name:'电影&网剧&剧集&动漫&综艺&记录',
    // class_url:'20&1&2&3&4&23',
    class_parse:'.navbar-items li:gt(1):lt(8);a&&Text;a&&href;/(\\d+).html',
    play_parse:true,//一般有免嗅才开,没免嗅还开只能服务器打印日志进行监听并重定向
    // lazy:'通用免嗅',
    lazy:'js:var MY_HOME="http://lanmeiguojiang.com:5244/d/%E8%93%9D%E8%8E%93%E4%BA%91%E7%9B%98";let headers=d.headers;headers["Referer"]=input;let fetch_params={headers:headers,timeout:d.timeout,encoding:d.encoding};let html=fetch(input,fetch_params);var player=JSON.parse(html.match(/r player_.*?=(.*?)</)[1]);var jsurl=player.url;var from=player.from;if(player.encrypt=="1"){var jsurl=unescape(jsurl)}else if(player.encrypt=="2"){var jsurl=unescape(base64Decode(jsurl))}else{jsurl}if(/ddzy|duoduo/.test(from)){let mx=false;if(mx){let html=request(MY_HOME+"/pzwj.js");eval(html);var jx=MacPlayerConfig.player_list[from].parse;print("第1次多多解析:",jx);eval(fetch(jx+jsurl,fetch_params).match(/var config = {[\\s\\S]*?}/)[0]);jx=jx.replace("?url=","");eval(fetch(jx+"js/decode.js",fetch_params));jxk=fetch(jx+"js/setting.js",fetch_params).split(",");jx+="555tZ4pvzHE3BpiO838.php";print("第2次多多解析:",jx);config.tm=(new Date).getTime();config.sign="F4penExTGogdt6U8";input=getVideoInfo(JSON.parse(fetch(buildUrl(jx,config),fetch_params)).url)}}else{let jxurl="https://lanmeiguojiang.com/dd/?url="+jsurl;input=maoss(jxurl,jxurl,"A42EAC0C2B408472")}',
    limit:30,
    推荐:'.tab-list.active;a.module-poster-item.module-item;.module-poster-item-title&&Text;.lazyload&&data-original;.module-item-note&&Text;a&&href',
    double:true, // 推荐内容是否双层定位
    一级:'body a.module-poster-item.module-item;a&&title;.lazyload&&data-original;.module-item-note&&Text;a&&href',
    二级:{"title":"h1&&Text;.module-info-tag&&Text","img":".lazyload&&data-original","desc":".module-info-item:eq(1)&&Text;.module-info-item:eq(2)&&Text;.module-info-item:eq(3)&&Text","content":".module-info-introduction&&Text","tabs":".module-tab-item","lists":".module-play-list:eq(#id) a"},
    搜索:'body .module-item;.module-card-item-title&&Text;.lazyload&&data-original;.module-item-note&&Text;a&&href;.module-info-item-content&&Text',
}