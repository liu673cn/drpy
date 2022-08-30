var rule = {
    title:'鸭奈飞',
    host:'https://yanetflix.com',
    // homeUrl:'/',
    url:'/vodshow/fyclass--------fypage---.html',
    detailUrl:'https://yanetflix.com/voddetail/fyid.html',//非必填
    searchUrl:'/vodsearch/**----------fypage---.html',
    searchable:0,
    quickSearch:0,
    // class_name:'电影&连续剧&综艺&动漫',
    // class_url:'dianying&lianxuju&zongyi&dongman',
    class_parse:'.navbar-items li:gt(1):lt(6);a&&Text;a&&href;.*/(.*?).html',
    play_parse:true,
    lazy:'',
    推荐:'.tab-list.active;a.module-poster-item.module-item;.module-poster-item-title&&Text;.lazyload&&data-original;.module-item-note&&Text;a&&href',
    double:true, // 推荐内容是否双层定位
    一级:'body a.module-poster-item.module-item;a&&title;.lazyload&&data-original;.module-item-note&&Text;a&&href',
    二级:{"title":"h1&&Text;.module-info-tag&&Text","img":".lazyload&&data-original","desc":".module-info-item:eq(1)&&Text;.module-info-item:eq(2)&&Text;.module-info-item:eq(3)&&Text","content":".module-info-introduction&&Text","tabs":".module-tab-item","lists":".module-play-list:eq(#id) a"},
    搜索:'body .module-item;.module-card-item-title&&Text;.lazyload&&data-original;.module-item-note&&Text;a&&href;.module-info-item-content&&Text',
}