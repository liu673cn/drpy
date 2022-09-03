var rule = {
    title:'360影视',
    host:'https://www.360kan.com',
    homeUrl:'https://api.web.360kan.com/v1/rank?cat=2&size=9',
    detailUrl:'https://api.web.360kan.com/v1/detail?cat=fyclass&id=fyid',
    searchUrl:'https://api.so.360kan.com/index?force_v=1&kw=**&from=&pageno=fypage&v_ap=1&tab=all',
    url:'https://api.web.360kan.com/v1/filter/list?catid=fyclass&rank=rankhot&cat=&year=&area=&act=&size=35&pageno=fypage&callback=',
    headers:{
        'User-Agent':'MOBILE_UA'
    },
    timeout:5000,
    class_name:'电视剧&电影&综艺&动漫',
    class_url:'2&1&3&4',
    limit:5,
    play_parse:true,
    // play_parse:true,
    lazy:'js:input={parse: 1, playUrl: "", jx: 1, url: input}',
    推荐:'json:data;title;cover;comment;cat+ent_id;description',
    一级:'json:data.movies;title;cover;pubdate;id;description',
    二级:{is_json:1,"title":"data.title;data.moviecategory[0]+data.moviecategory[1]","img":"data.cdncover","desc":"data.area[0];data.director[0]","content":"data.description","tabs":"data.playlink_sites;data.playlinksdetail.#idv.quality","lists":"data.playlinksdetail.#idv.default_url"},
    // 二级:{is_json:1,"title":"data.title;data.moviecategory[0]+data.moviecategory[1]","img":"data.cdncover","desc":"data.area[0];data.director[0]","content":"data.description","tabs":"data.playlink_sites","lists":"data.playlinksdetail.#idv.default_url"},
    搜索:'json:data.longData.rows;titleTxt;cover;score;cat_id+id;description',
}