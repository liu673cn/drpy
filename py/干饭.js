js:
cacheUrl = d.getParse(input);
print(cacheUrl);
if(cacheUrl){
    input=cacheUrl;
}else{
    try {
        r = requests.get(input, headers=d.headers,timeout=d.timeout);
        r.encoding = d.encoding;
        html = r.text;
        let ret = html.match(/var player_(.*?)=(.*?)</)[2];
        let url = JSON.parse(ret).url;
        if(/\.m3u8|\.mp4/.test(url)){
            input = url
        }else if(!/http/.test(url)&&!/\//.test(url)){
            try {
                url = unescape(base64Decode(url));
                if(/http/.test(url)){
                    input = url
                }
            }catch (e) {
                print('解码url发生错误:'+e.message);
            }
        }
    }catch (e) {
        print('发生错误:'+e.message);
    }
}
