muban.首图2.二级.tabs = '.stui-pannel__head h3';
var rule = Object.assign(muban.首图2,{
    title:'人人影视',
    host:'https://www.rttks.com',
    url:'/rrtop/fyclass/page/fypage.html',
    searchUrl:'/rrso**/page/fypage.html',
    class_parse:'.stui-header__menu li;a&&Text;a&&href;.*/(.*?).html',
    // cate_exclude:'解说',
    play_parse:true,
    lazy:'',
    搜索:'ul.stui-vodlist__media&&li;a&&title;.lazyload&&data-original;.pic-text&&Text;a&&href;.text-muted:eq(-1)&&Text',
});