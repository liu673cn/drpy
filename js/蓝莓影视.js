var rule = {
    title:'蓝莓影视',
    host:'https://lanmeiguojiang.com',
    // homeUrl:'/',
    url:'/show/fyclass--------fypage---.html',
    headers:{
        'User-Agent':'MOBILE_UA'
    },
    searchUrl:'/vodsearch/**----------fypage---.html',
    // class_name:'电影&网剧&剧集&动漫&综艺&记录',
    // class_url:'20&1&2&3&4&23',
    class_parse:'.navbar-items li:gt(1):lt(8);a&&Text;a&&href;/(\\d+).html',
    limit:5,
    推荐:'.tab-list.active;a.module-poster-item.module-item;.module-poster-item-title&&Text;.lazyload&&data-original;.module-item-note&&Text;a&&href',
    double:true, // 推荐内容是否双层定位
    一级:'body a.module-poster-item.module-item;a&&title;.lazyload&&data-original;.module-item-note&&Text;a&&href',
    二级:{"title":"h1&&Text;.module-info-tag&&Text","img":".lazyload&&data-original","desc":".module-info-item:eq(1)&&Text;.module-info-item:eq(2)&&Text;.module-info-item:eq(3)&&Text","content":".module-info-introduction&&Text","tabs":".module-tab-item","lists":".module-play-list:eq(#id) a"},
    搜索:'body .module-item;.module-card-item-title&&Text;.lazyload&&data-original;.module-item-note&&Text;a&&href;.module-info-item-content&&Text',
}