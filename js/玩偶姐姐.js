var rule = {
    title:'玩偶姐姐',
    host:'https://hongkongdollvideo.com',
    homeUrl:'/latest/',
    url:'/fyclass/fypage.html[/fypage/]',
    searchUrl:'/vodsearch/**----------fypage---.html',
    ua:'MOBILE_UA',
    class_name:'最新&Hongkong Doll&麻豆传媒&91制片厂&天美传媒&蜜桃传媒&皇家华人&星空传媒&精东影业&乐播传媒&成人头条&乌鸦传媒&兔子先生&杏吧原创&mini传媒&大象传媒&开心鬼传媒&PsychoPorn&糖心Vlog',
    class_url:'latest&Hongkong Doll&麻豆传媒&91制片厂&天美传媒&蜜桃传媒&皇家华人&星空传媒&精东影业&乐播传媒&成人头条&乌鸦传媒&兔子先生&杏吧原创&mini传媒&大象传媒&开心鬼传媒&PsychoPorn&糖心Vlog',
    class_parse:'body&&#side-menu:not(:has(.menu-icons))&&li;',
    一级:'.col-sm-6;h3&&Text;img&&data-src;.date&&Text;a&&href',
    二级:{"title":"h1&&Text;.module-info-tag&&Text","img":".lazyload&&data-original","desc":".module-info-item:eq(1)&&Text;.module-info-item:eq(2)&&Text;.module-info-item:eq(3)&&Text","content":".module-info-introduction&&Text","tabs":".module-tab-item","lists":".module-play-list:eq(#id) a"},
    搜索:'body .module-item;.module-card-item-title&&Text;.lazyload&&data-original;.module-item-note&&Text;a&&href;.module-info-item-content&&Text',
}