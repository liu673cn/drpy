js:
var d = [];
var vod={vod_id:input};
let html=request(input);
// print(html);
let json = JSON.parse(html);
if (/keyword/.test(input)) {
    input = 'https://search.youku.com/api/search?appScene=show_episode&showIds=' + json.pageComponentList[0].commonData.showId;
    json = JSON.parse(fetch(MY_URL, fetch_params));
}
let video_lists = json.serisesList;
var name = json.sourceName;
if(/优酷/.test(name)&&video_lists.length>0){//获取简介详情
    let ourl = 'https://v.youku.com/v_show/id_' + video_lists[0].videoId + '.html';
    let _img = video_lists[0].thumbUrl;
    // log(ourl);
    let html = fetch(ourl,{headers:{'Referer':'https://v.youku.com/','User-Agent':PC_UA}});
    let json = /__INITIAL_DATA__/.test(html)?html.split('window.__INITIAL_DATA__ =')[1].split(';')[0]:'{}';
    if(json==='{}'){
        log('触发了优酷人机验证');
        vod.vod_remarks = ourl;
        vod.vod_pic = _img;
        vod.vod_name = video_lists[0].title.replace(/(\d+)/g,'');
        vod.vod_content = '触发了优酷人机验证,本次未获取详情,但不影响播放('+ourl+')';
    }else{
        try {
            json = JSON.parse(json);
            let data = json.data.data;
            let data_extra = data.data.extra;
            let img = data_extra.showImgV;
            let model = json.data.model;
            let m =  model.detail.data.nodes[0].nodes[0].nodes[0].data;
            let _type = m.showGenre
            let _desc = m.updateInfo||m.subtitle;
            let JJ=m.desc;
            let _title = m.introTitle;
            // subtitle  desc   showImgV 是竖着的  showImg横着的
            // let uptips = pdfh(html,'.title-info&&Text');
            vod.vod_pic = img;
            vod.vod_name = _title;
            vod.vod_type = _type;
            vod.vod_remarks = _desc;
            vod.vod_content = JJ;
        }catch (e) {
            log('海报渲染发生错误:'+e.message);
            vod.vod_remarks = name;
        }
    }
}

if(!/优酷/.test(name)){
    vod.vod_content = '非自家播放源,暂无视频简介及海报';
    vod.vod_remarks = name;
}
function adhead(url){
    // let hd = 'https://v.sogou.com';
    // if(!url.startsWith(hd)){
    //     url = hd+url
    // }
    return urlencode(url)
}
play_url = play_url.replace('&play_url=','&type=json&play_url=');
video_lists.forEach(function (it){
    let url = 'https://v.youku.com/v_show/id_' + it.videoId + '.html';
    if (it.thumbUrl) {
        d.push({
            desc: it.showVideoStage ? it.showVideoStage.replace('期', '集') : it.displayName,
            pic_url: it.thumbUrl,
            title: it.title,
            url: play_url+adhead(url),
        });
    }else if (name!=='优酷'){
        d.push({
            title: (it.displayName?it.displayName:it.title),
            url: play_url+adhead(it.url),
        });
    }
});
vod.vod_play_from = name;
vod.vod_play_url = d.map(function (it){
    return it.title + '$' + it.url;
}).join('#');