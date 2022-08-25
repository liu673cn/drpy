var rule = {
    title:'蓝莓影视',
    url:'https://lanmeiguojiang.com/show/fyclass--------fypage---.html',
    searchUrl:'/vodsearch/**----------fypage---.html',
    ua:'MOBILE_UA',
    class_name:'电影&网剧&剧集&动漫&综艺&记录',
    class_url:'20&1&2&3&4&23',
    一级:'body a.module-poster-item.module-item;a&&title;.lazyload&&data-original;.module-item-note&&Text;a&&href',
    二级:{"title":"h1&&Text;.module-info-tag&&Text","img":".lazyload&&data-original","desc":".module-info-item:eq(1)&&Text;.module-info-item:eq(2)&&Text;.module-info-item:eq(3)&&Text","content":".module-info-introduction&&Text","tabs":".module-tab-item","lists":".module-play-list:eq(#id) a"},
    搜索:'body .module-item;.module-card-item-title&&Text;.lazyload&&data-original;.module-item-note&&Text;a&&href;.module-info-item-content&&Text',
}