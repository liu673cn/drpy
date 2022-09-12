js:
// fetch_params.withHeaders = 1;
// let data=fetch(input,fetch_params);
// let html = data.body;
fetch_params.headers['user-agent'] = MOBILE_UA;
let html=request(input);
// let rurl = html.match(/window\.open\('(.*?)',/)[1].split('?')[0];
let rurl = html.match(/window\.open\('(.*?)',/)[1];
// print(rurl);
rurl = urlDeal(rurl);
// print(rurl);
// input = rurl;
input = {parse:1,url:rurl};
// print(html);
