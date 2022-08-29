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