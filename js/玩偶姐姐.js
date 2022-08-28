var rule = {
    title:'玩偶姐姐',
    host:'https://hongkongdollvideo.com',
    homeUrl:'/latest/',
    url:'/fyclass/fypage.html[/fyclass/]',
    headers:{
        'User-Agent':'MOBILE_UA'
    },
    timeout:5000,
    class_parse:'#side-menu:lt(1) li;a&&Text;a&&href;com/(.*?)/',
    play_parse:true,
    一级:'.col-sm-6;h3&&Text;img&&data-src;.date&&Text;a&&href',
    二级:'*',
}