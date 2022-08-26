var rule = {
    title:'喵喵',
    host:'https://www.2345ka.com',
    // homeUrl:'/',
    url:'/t/fyclass/fypage.html',
    searchUrl:'/s/**/fypage.html',
    headers:{
        'User-Agent':'Mozilla/5.0 (Linux; U; Android 9; zh-CN; MI 9 Build/PKQ1.181121.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.5.1035 Mobile Safari/537.36'
    },
    timeout:5000,
    class_parse:'.bm-item-list a:gt(0):lt(7);a&&Text;a&&href;/(\\d+).html',
    limit:10,
    推荐:'.movie-list-body;.movie-list-item;.movie-title&&Text;.movie-post-lazyload&&data-original;.movie-rating&&Text;a&&href',
    double:true, // 推荐内容是否双层定位
    一级:'.movie-list-body .movie-list-item;.movie-title&&Text;.Lazy&&data-original;.movie-rating&&Text;a&&href',
    二级:{"title":"h1.movie-title&&Text;.data:eq(1)&&Text","img":".poster img&&src","desc":".cr3.starLink&&Text","content":".detailsTxt&&Text","tabs":".play_source_tab a","lists":".content_playlist:eq(#id) a"},
    搜索:'.vod-search-list;.movie-title&&Text;.Lazy&&data-original;.getop&&Text;a&&href;.getop:eq(-1)&&Text',
}