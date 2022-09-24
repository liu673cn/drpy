js:
function GetPlayUrl(playUrl) {
    let realPlay = {parse:0,url:playUrl};
    if (/mgtv|sohu/.test(playUrl)) {
        realPlay.headers = {'User-Agent':'Mozilla/5.0'};
    } else if (/bili/.test(playUrl)) {
        realPlay.headers  ={'User-Agent':'Mozilla/5.0','Referer':'https://www.bilibili.com'};
    } else if (/ixigua/.test(playUrl)) {
        realPlay.headers = {'User-Agent':'Mozilla/5.0','Referer':'https://www.ixigua.com'};
    }
    return realPlay
}
if (/\.m3u8|\.mp4/.test(input)) {
    input={parse:0,url:input};
} else {
    try {
        let url = "http://api.kunyu77.com/api.php/provide/parserUrl?url=" + input;
    let html = request(url);
    let urll = JSON.parse(html).data.url;
    let playhtml = request(urll);
    let playurl = JSON.parse(playhtml).url;
    input = GetPlayUrl(playurl);
    }catch (e) {
        input = {parse:1,url:input};
    }
}