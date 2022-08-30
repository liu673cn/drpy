var rule = Object.assign(muban.mxpro,{
title:'夜空',
host:'https://www.yekong.cc',
url:'/pianku-fyclass--------fypage---/',
searchUrl:'/search-**----------fypage---/',
searchable:1,
quickSearch:0,
class_parse:'.navbar-items li:gt(1):lt(7);a&&Text;a&&href;.*v/(.*?)/',
});