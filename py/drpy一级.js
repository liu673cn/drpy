js:
// print(input);
// print(MY_CATE);
// print(MY_PAGE);
// print(MY_FL);
let d = [];
let douban = input.split('douban=')[1].split('&')[0];
let douban_api_host = 'https://frodo.douban.com/api/v2';
let miniapp_apikey = '0ac44ae016490db2204ce0a042db2916';
const count = 30;

function miniapp_request(path, query){
    try {
        let url = douban_api_host + path;
        query.apikey = miniapp_apikey;
        // let headers = {
        //     "Host": "frodo.douban.com",
        //     "Connection": "Keep-Alive",
        //     "Referer": "https://servicewechat.com/wx2f9b06c1de1ccfca/84/page-frame.html",
        //     "content-type": "application/json",
        //     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat"
        // }
        // fetch_params.headers = headers;
        fetch_params.headers = oheaders;
        // print(fetch_params);
        url = buildUrl(url,query);
        // let html = request(url);
        let html = fetch(url,fetch_params);
        // print(html);
        return JSON.parse(html);
    }
    catch(e){
    print('发生了错误:'+e.message);
    return {}
    }
}

function cate_filter(d,douban){
    douban = douban||'';
    try {
        if(MY_CATE==='interests'){
            if(douban){
            let status = MY_FL.status||"mark";
            let subtype_tag = MY_FL.subtype_tag||"";
            let year_tag = MY_FL.year_tag||"全部";
            let path = "/user/"+douban+"/interests";
            let res = miniapp_request(path, {
                "type": "movie",
                "status": status,
                "subtype_tag": subtype_tag,
                "year_tag": year_tag,
                "start": (MY_PAGE - 1) * count,
                "count": count
            });
            // print(res);
            }else{
             return {}
            }
        }else if(MY_CATE === "hot_gaia"){
            let sort =MY_FL.sort||"recommend";
            let area =MY_FL.area||"全部";
            let path = '/movie/'+MY_CATE;
            let res = miniapp_request(path, {
                "area": area,
                "sort": sort,
                "start": (MY_PAGE - 1) * count,
                "count": count
            });
            // print(res);
        }else if(MY_CATE === "tv_hot" || MY_CATE === "show_hot"){
            let stype = MY_FL.type||MY_CATE;
            let path = "/subject_collection/"+stype+"/items"
            let res = miniapp_request(path, {
                "start": (MY_PAGE - 1) * count,
                "count": count
            });
            // print(res);
        }
        else if(MY_CATE.startsWith("rank_list")){
            let id = MY_CATE === "rank_list_movie"?"movie_real_time_hotest":"tv_real_time_hotest";
            id = MY_FL.榜单||id;
            let path = "/subject_collection/"+id+"/items";
            let res = miniapp_request(path, {
                "start": (MY_PAGE - 1) * count,
                "count": count
            });
            // print(res);
        }else{
            let path = "/"+MY_CATE+"/recommend";
            let selected_categories;
            if(Object.keys(MY_FL).length > 0){
                let sort = MY_FL.sort||"T";
                let tags = Object.Values(MY_FL).join(',');
                if(MY_CATE === "movie"){
                    selected_categories = {
                        "类型": MY_FL.类型||'',
                        "地区": MY_FL.地区||''
                    }
                }else{
                    selected_categories = {
                        "类型": MY_FL.类型||"",
                        "形式": MY_FL.类型?MY_FL.类型+'地区':'',
                        "地区": MY_FL.地区||""
                    }
                }
            }else{
                let sort = "T";
                let tags = "";
                if(MY_CATE === "movie"){
                selected_categories = {
                    "类型": "",
                    "地区": ""
                };
                }else{
                selected_categories = {
                    "类型": "",
                    "形式": "",
                    "地区": ""
                }
                }
            }
            let params = {
                "tags": tags,
                "sort": sort,
                "refresh": 0,
                "selected_categories": stringify(selected_categories),
                "start": (MY_PAGE - 1) * count,
                "count": count
            }
            // print(params);
            let res = miniapp_request(path, params)
        }
        let result = {
            "page": MY_PAGE,
            "pagecount": Math.ceil(res.total / count),
            "limit": count,
            "total": res.total
        }
        let items = [];
        if(/^rank_list|tv_hot|show_hot/.test(MY_CATE)) {
            items = res['subject_collection_items']
        }
        else if(MY_CATE==='interests'){
            res["interests"].forEach(function (it){
                items.push(it.subject)
            });
        }else{
            items = res.items
        }
        let lists = [];
        // print(items);
        items.forEach(function (item){
            if( item.type==='movie'||item.type==='tv'){
                let rating = item.rating?item.rating.value:'';
                let rat_str = rating||'暂无评分';
                let title = item.title;
                let honor = item.honor_infos||[];
                let honor_str = honor.map(function (it){return it.title}).join('|');
                let vod_obj = {
                    // "vod_id": f'msearch:{item.get("type", "")}__{item.get("id", "")}',
                    // "vod_id": item.type+'$'+item.id,
                    "vod_name": title !== "未知电影"?title: "暂不支持展示",
                    "vod_pic": item.pic.normal,
                    "vod_remarks": rat_str + " " + honor_str
                };
                let vod_obj_d = {
                    url: item.type+'$'+item.id,
                    title: title !== "未知电影"?title: "暂不支持展示",
                    pic_url: item.pic.normal,
                    desc: rat_str + " " + honor_str
                };
                lists.push(vod_obj);
                d.push(vod_obj_d);
            }
        });
        result.list = lists;
        return result

    }catch (e) {
        print(e.message);
    }
    return {}
}
// cate_filter(d);
// setResult(d);

let res = cate_filter(d);
// setHomeResult(res);
setResult2(res);