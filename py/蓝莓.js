js:
var MY_HOME='http://lanmeiguojiang.com:5244/d/%E8%93%9D%E8%8E%93%E4%BA%91%E7%9B%98';
let fetch_params = {headers:d.headers,timeout:d.timeout,encoding:d.encoding};
let html = fetch(input,fetch_params);
var player = JSON.parse(html.match(/r player_.*?=(.*?)</)[1]);
var jsurl = player.url;
var from = player.from;
if (player.encrypt == '1') {
    var jsurl = unescape(jsurl);
} else if (player.encrypt == '2') {
    var jsurl = unescape(base64Decode(jsurl));
} else {
    jsurl
}
eval(getCryptoJS());
if (/ddzy|duoduo/.test(from)) {
    eval(fetch(MY_HOME + '/pzwj.js',fetch_params));
    var jx = MacPlayerConfig.player_list[from].parse;
    eval(request(jx + jsurl, {
        headers: {
            'Referer': input
        }
    }).match(/var config = {[\s\S]*?}/)[0]);
    jx = jx.replace('?url=', '');
    eval(request(jx + 'js/decode.js'));
    jxk = request(jx + 'js/setting.js').split(',');
    jx += '555tZ4pvzHE3BpiO838.php'; //eval(jxk[32])
    config.tm = new Date().getTime();
    config.sign = 'F4penExTGogdt6U8'; //eval(jxk[36])
    input =  getVideoInfo(JSON.parse(fetch(buildUrl(jx, config))).url);
} else {
    let jxurl = "https://lanmeiguojiang.com/dd/?url="+jsurl;
    input =  maoss(jxurl, jxurl, "A42EAC0C2B408472");
}