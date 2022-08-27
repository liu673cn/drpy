var rule = {
    title:'莫扎兔',
    host:'https://www.mozhatu.com',
    // homeUrl:'/',
    url:'/index.php/vod/show/id/fyclass/page/fypage.html',
    searchUrl:'/vodsearch/**----------fypage---.html',
    headers:{//网站的请求头,完整支持所有的,常带ua和cookies
        'User-Agent':'MOBILE_UA',
        "Cookie": "searchneed=ok"
    },
    // class_name:'电影&连续剧&福利&动漫&综艺',
    // class_url:'1&2&124&4&3',
    class_parse:'.navbar-items li:gt(2):lt(8);a&&Text;a&&href;.*/(.*?).html',
    limit:10,
    推荐:'.tab-list.active;a.module-poster-item.module-item;.module-poster-item-title&&Text;.lazyload&&data-original;.module-item-note&&Text;a&&href',
    double:true, // 推荐内容是否双层定位
    一级:'body a.module-poster-item.module-item;a&&title;.lazyload&&data-original;.module-item-note&&Text;a&&href',
    二级:{"title":"h1&&Text;.module-info-tag&&Text","img":".lazyload&&data-original","desc":".module-info-item:eq(1)&&Text;.module-info-item:eq(2)&&Text;.module-info-item:eq(3)&&Text","content":".module-info-introduction&&Text","tabs":".module-tab-item","lists":".module-play-list:eq(#id) a"},
    //搜索:'body .module-item;.module-card-item-title&&Text;.lazyload&&data-original;.module-item-note&&Text;a&&href;.module-info-item-content&&Text',
}