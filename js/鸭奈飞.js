var rule = {
    title:'鸭奈飞',
    url:'https://yanetflix.com/vodshow/fyclass--------fypage---.html',
    detailUrl:'https://yanetflix.com/voddetail/fyid.html',
    // url:'https://yanetflix.com/vodshow/',
    searchUrl:'/vodsearch/**----------fypage---.html',
    ua:'MOBILE_UA',
    class_name:'电影&连续剧&综艺&动漫',
    class_url:'dianying&lianxuju&zongyi&dongman',
    一级:'body a.module-poster-item.module-item;a&&title;.lazyload&&data-original;.module-item-note&&Text;a&&href',
    二级:{"title":"h1&&Text;.module-info-tag&&Text","img":".lazyload&&data-original","desc":".module-info-item:eq(1)&&Text;.module-info-item:eq(2)&&Text;.module-info-item:eq(3)&&Text","content":".module-info-introduction&&Text","tabs":".module-tab-item","lists":".module-play-list:eq(#id) a"},
    搜索:'body .module-item;.module-card-item-title&&Text;.lazyload&&data-original;.module-item-note&&Text;a&&href;.module-info-item-content&&Text',
}