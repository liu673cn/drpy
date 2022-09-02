var rule = Object.assign(muban.mxpro,{
title:'蓝莓影视',
host:'https://lanmeiguojiang.com',
url:'/show/fyclass--------fypage---.html',
searchUrl:'/search/**-fypage.html',
searchable:1,
quickSearch:1,
class_parse:'.navbar-items li:gt(1):lt(8);a&&Text;a&&href;/(\\d+).html',
// lazy:'js:print(fetch_params);var MY_HOME="http://lanmeiguojiang.com:5244/d/%E8%93%9D%E8%8E%93%E4%BA%91%E7%9B%98";let headers=d.headers;headers["Referer"]=input;let fetch_params={headers:headers,timeout:d.timeout,encoding:d.encoding};let html=fetch(input,fetch_params);var player=JSON.parse(html.match(/r player_.*?=(.*?)</)[1]);var jsurl=player.url;var from=player.from;if(player.encrypt=="1"){var jsurl=unescape(jsurl)}else if(player.encrypt=="2"){var jsurl=unescape(base64Decode(jsurl))}else{jsurl}if(/ddzy|duoduo/.test(from)){let mx=false;if(mx){let html=request(MY_HOME+"/pzwj.js");eval(html);var jx=MacPlayerConfig.player_list[from].parse;print("第1次多多解析:",jx);eval(fetch(jx+jsurl,fetch_params).match(/var config = {[\\s\\S]*?}/)[0]);jx=jx.replace("?url=","");eval(fetch(jx+"js/decode.js",fetch_params));jxk=fetch(jx+"js/setting.js",fetch_params).split(",");jx+="555tZ4pvzHE3BpiO838.php";print("第2次多多解析:",jx);config.tm=(new Date).getTime();config.sign="F4penExTGogdt6U8";input=getVideoInfo(JSON.parse(fetch(buildUrl(jx,config),fetch_params)).url)}}else{let jxurl="https://lanmeiguojiang.com/dd/?url="+jsurl;input=maoss(jxurl,jxurl,"A42EAC0C2B408472")}',
lazy:'js:var MY_HOME="http://lanmeiguojiang.com:5244/d/%E8%93%9D%E8%8E%93%E4%BA%91%E7%9B%98";print(fetch_params);let html=fetch(input,fetch_params);var player=JSON.parse(html.match(/r player_.*?=(.*?)</)[1]);var jsurl=player.url;var from=player.from;if(player.encrypt=="1"){var jsurl=unescape(jsurl)}else if(player.encrypt=="2"){var jsurl=unescape(base64Decode(jsurl))}else{jsurl}if(/ddzy|duoduo/.test(from)){let mx=false;if(mx){let html=request(MY_HOME+"/pzwj.js");eval(html);var jx=MacPlayerConfig.player_list[from].parse;print("第1次多多解析:",jx);eval(fetch(jx+jsurl,fetch_params).match(/var config = {[\\s\\S]*?}/)[0]);jx=jx.replace("?url=","");eval(fetch(jx+"js/decode.js",fetch_params));jxk=fetch(jx+"js/setting.js",fetch_params).split(",");jx+="555tZ4pvzHE3BpiO838.php";print("第2次多多解析:",jx);config.tm=(new Date).getTime();config.sign="F4penExTGogdt6U8";input=getVideoInfo(JSON.parse(fetch(buildUrl(jx,config),fetch_params)).url)}}else{let jxurl="https://lanmeiguojiang.com/dd/?url="+jsurl;input=maoss(jxurl,jxurl,"A42EAC0C2B408472")}',
// lazy:(function(input){
//     console.log(typeof(pdfh))
//     return input
// }),
});