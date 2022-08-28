var rule = {
    title:'cokemv',
    host:'https://cokemv.me',
    // homeUrl:'/',
    url:'/vodshow/fyclass--------fypage---.html',
    searchUrl:'/vodsearch/**----------fypage---.html',
    headers:{
        'User-Agent':'MOBILE_UA',
        "Cookie": "showBtn=true;PHPSESSID=58nhbq5r54jivukrk4o27dn7m6"
    },
    timeout:5000,
    class_parse:'.navbar-items li:gt(1):lt(7);a&&Text;a&&href;/(\\d+).html',
    play_parse:true,
    limit:8,
    推荐:'.tab-list.active;a.module-poster-item.module-item;.module-poster-item-title&&Text;.lazyload&&data-original;.module-item-note&&Text;a&&href',
    double:true, // 推荐内容是否双层定位
    一级:'body a.module-poster-item.module-item;a&&title;.lazyload&&data-original;.module-item-note&&Text;a&&href',
    二级:{"title":"h1&&Text;.module-info-tag&&Text","img":".lazyload&&data-original","desc":".module-info-item:eq(1)&&Text;.module-info-item:eq(2)&&Text;.module-info-item:eq(3)&&Text","content":".module-info-introduction&&Text","tabs":".module-tab-item","lists":".module-play-list:eq(#id) a"},
    搜索:'body .module-item;.module-card-item-title&&Text;.lazyload&&data-original;.module-item-note&&Text;a&&href;.module-info-item-content&&Text',
}