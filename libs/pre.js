Object.assign = function () {
	var target = arguments[0];
    for (var i = 1; i < arguments.length; i++) {
        var source = arguments[i];
        for (var key in source) {
            if (Object.prototype.hasOwnProperty.call(source, key)) {
                target[key] = source[key];
            }
        }
    }
    return target;
};
Object.prototype.myValues=function(obj){
   if(obj ==null) {
   	 throw new TypeError("Cannot convert undefined or null to object");
   }
   var res=[]
   for(var k in obj){
     if(obj.hasOwnProperty(k)){//需判断是否是本身的属性
   		res.push(obj[k]);
   	 }
   }
   return res;
}
Array.prototype.join = function (emoji) {
    emoji = emoji||',';
      let self = this;
      let str = "";
      let i = 0;
      if (!Array.isArray(self)) {throw String(self)+'is not Array'}
      if(self.length===0){return ''}
      if (self.length === 1){return String(self[0])}
      i = 1;
      str = this[0];
      for (; i < self.length; i++) {
        str += String(emoji)+String(self[i]);
      }
      return str;
};
// 千万不要用for in 推荐 forEach (for in 会打乱顺序)
//猫函数
    function maoss(jxurl, ref, key) {
        eval(getCryptoJS());
        try {
            var getVideoInfo = function(text) {
                return CryptoJS.AES.decrypt(text, key, {
                    iv: iv,
                    padding: CryptoJS.pad.Pkcs7
                }).toString(CryptoJS.enc.Utf8);
            };
            var token_key = key == undefined ? 'dvyYRQlnPRCMdQSe' : key;
            if (ref) {
                var html = request(jxurl, {
                    headers: {
                        'Referer': ref
                    }
                });
            } else {
                var html = request(jxurl);
            }
            if (html.indexOf('&btwaf=') != -1) {
                html = request(jxurl + '&btwaf' + html.match(/&btwaf(.*?)"/)[1], {
                    headers: {
                        'Referer': ref
                    }
                })
            }
            var token_iv = html.split('_token = "')[1].split('"')[0];
            var key = CryptoJS.enc.Utf8.parse(token_key);
            var iv = CryptoJS.enc.Utf8.parse(token_iv);
            // log("iv:"+iv);
            //  log(html);
            eval(html.match(/var config = {[\s\S]*?}/)[0] + '');
            if (config.url.slice(0, 4) != 'http') {
                //config.url = decodeURIComponent(AES(config.url, key, iv));
                config.url = CryptoJS.AES.decrypt(config.url, key, {
                    iv: iv,
                    padding: CryptoJS.pad.Pkcs7
                }).toString(CryptoJS.enc.Utf8)
            }
            return config.url;
        } catch (e) {
            return '';
        }
    }