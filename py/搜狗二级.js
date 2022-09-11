js: var res = {};
var d = [];
var html = getResCode();
var jsUrl = fetch('hiker://files/cache/MyParseSet.json');
if (jsUrl == '' || !fetch(JSON.parse(jsUrl).cj)) {
    var jsFile = fetch('https://gitee.com/Duan-Nian/Dn/raw/master/hikerview/CloudParse-V2_Dn.js');
} else {
    var jsFile = fetch(JSON.parse(jsUrl).cj);
}
eval(jsFile);
if (getVar("解析列表") == "开") {
    setParse();
}

var easy = `@lazyRule=.js:try{var input=fetch(input,{}).split("('")[1].split("',")[0];if(input.match(/ixigua|iqiyi|qq.com|mgtv|le.com|bili|sohu|youku|pptv|cctv|1905.com/)){var input=input.split("?")[0];{input;`+lazy+`}}else if(input.match(/huanxi/)){var input=input.split("&")[0];{input;`+lazy+`}}else if(input.match(/migu/)){var input=input.replace(/\\?.*cid/,'?cid').replace(/http/,'https').split("&")[0];{input;`+lazy+`}}else{input;`+lazy+`}}catch(e){input}`;


var Rule = MY_URL+`@rule=js:var res={};var d=[];var html=getResCode();var get=parseDomForHtml(html, 'body&&.srch-result-info&&Html');for(let i = 0;;i++){try{d.push({title:parseDomForHtml(get, 'div,' +i+ '&&Html'),col_type: 'rich_text'});d.push({col_type: 'line'});}catch(e){break;}};res.data=d;setHomeResult(res);`;


try {

    var json = JSON.parse(html.match(/INITIAL_STATE.*?({.*});/)[1]).detail.itemData;

    var key = json.dockey;
    var name = json.name;
    var zone = json.zone;
    var score = json.score ? json.score: '暂无';
    var style = json.style;
    var emcee = json.emcee ? '主持：' + json.emcee: json.name;
    var director = json.director ? '导演：' + json.director: name;
    var starring = json.starring ? '演员：' + json.starring: '声优：' + json.shengyou;
    var update = json.update_wordstr ? json.update_wordstr: '';
    var tv_station = json.tv_station ? json.tv_station: zone;
    var introduction = json.introduction;
    var shengyou = json.shengyou;

    var shows = json.play_from_open_index;
    var plays = json.play.item_list;

    if (shows) {
        d.push({
            title: emcee + '\n' + tv_station,
            desc: style + ' 评分:' + score + '\n' + update,
            pic_url: parseDom(html, '#thumb_img&&img&&src'),
            url: set_switch,
            col_type: 'movie_1_vertical_pic_blur'
        });
    } else {
        d.push({
            title: director.replace(/;/g, '\t') + '\n' + starring.replace(/.*undefined/, '').replace(/;/g, '\t'),
            desc: style + ' 评分:' + score + '\n' + update,
            pic_url: parseDom(html, '#thumb_img&&img&&src'),
            url: set_switch,
            col_type: 'movie_1_vertical_pic_blur'
        });
    }
    d.push({
        title: "剧情",
        url: Rule,
pic_url:'https://s1.ax1x.com/2020/11/09/BT6WIe.png',
        col_type: 'icon_small_3'
    });
    d.push({
        title: "资源网",
        url: 'hiker://search?s=' + name + '&rule=资源网采集.xyq',
pic_url:'https://s3.ax1x.com/2020/11/23/DGW0de.png',
        col_type: 'icon_small_3'
    });
    d.push({
        title: "剧照",
        url: MY_URL+`@rule=js:var res={};var d=[];var html=getResCode();try{var tabs=parseDomForArray(html, '#photoList&&.sort_lst_bx&&a');for(var i in tabs){d.push({pic_url: parseDomForHtml(tabs[i], 'img&&data-src'),url: parseDomForHtml(tabs[i], 'img&&data-src'),col_type: 'pic_1_full'});d.push({col_type: 'line'});}}catch(e){};res.data=d;setHomeResult(res);`,
pic_url:'https://s1.ax1x.com/2020/11/09/BT6cqK.png',
        col_type: 'icon_small_3'
    });
    d.push({
        col_type: "line"
    });
    try {
        var tabs = [];
        var lists = [];

        for (var i in plays) {
            lists.push(plays[i].info)
            tabs.push(plays[i].sitename[0])
        }

        function setTabs(tabs, vari) {
            if (plays[i].info || shows) {
                d.push({
                    title: (getVar('shsort') == ' - 逆序') ? '““””<b><span style="color: #FF0000">∨</span></b>': '““””<b><span style="color: #1aad19">∧</span></b>',
                    url: `#noLoading#@lazyRule=.js:let conf = getVar('shsort');if(conf==' - 逆序'){putVar({key:'shsort', value:' - 正序'});}else{putVar({key:'shsort', value:' - 逆序'})};refreshPage(false);'toast://切换排序成功';'#noHistory#hiker://empty'`,
                    col_type: 'flex_button'
                }) ;
			  for (var o in tabs) {
                    var url = "#noLoading#@lazyRule=.js:putVar('" + vari + "', '" + o + "');refreshPage(false);'toast://切换成功！';'#noHistory#hiker://empty'";
                    d.push({
                        title: getVar(vari, '0') == o ? '‘‘' + tabs[o] + '’’': tabs[o],
                        url: url,
                        col_type: 'flex_button'
                    })
                }
                d.push({
                    col_type: "line"
                })
            } else {
                d.push({
                    col_type: "blank_block"
                })
            }
        }

        function setLists(lists, index) {
            if (plays[i].info || shows) {
                var list = lists[index];
                if (list) {
                    if (getVar('shsort') == ' - 逆序') {

                        for (var j = list.length - 1; j >= 0; j--) {
                            if (!list[j].index == '0') {
                                d.push({
                                    title: list[j].index,
                                    url: 'https://v.sogou.com' + list[j].url + easy,
                                    col_type: "text_4"
                                });
                            }
                        }
                    } else {

                        for (var j = 0; j < list.length; j++) {
                            if (!list[j].index == '0') {
                                d.push({
                                    title: list[j].index,
                                    url: 'https://v.sogou.com' + list[j].url + easy,
                                    col_type: "text_4"
                                });
                            }
                        }
                    }
                }
                if (shows) {
                    var arr = [];
                    zy = shows.item_list[index];

                    for (var ii in zy.date) {

                        date = zy.date[ii];

                        day = zy.date[ii].day;

                        for (j in day) {

                            dayy = day[j][0] >= 10 ? day[j][0] : "0" + day[j][0];

                            Tdate = date.year + date.month + dayy;

                            arr.push(Tdate);
                            if (getVar('shsort') == ' - 逆序') {
                                arr.sort(function(a, b) {
                                    return b - a
                                })
                            } else {
                                arr.sort(function(a, b) {
                                    return a - b
                                })
                            }
                        }
                    }
                    for (var k = 0; k < arr.length; k++) {
                        url = "https://v.sogou.com/vc/eplay?query=" + arr[k] + "&date=" + arr[k] + "&key=" + json.dockey + "&st=5&tvsite=" + plays[index].site;

                        d.push({
                            title: "第" + arr[k] + "期",
                            col_type: "text_2",
                            url: url + easy
                        });
                    }
                }
            } else if (plays[index].site) {
                for (var m in plays) {
                    if (plays[m].flag_list.indexOf('trailer') == -1) {
                        d.push({
                            title: plays[m].sitename[0],
                            img: plays[m].picurl || 'http://dlweb.sogoucdn.com/video/wap/static/img/logo/' + plays[m].sitename[1],
                            url: 'https://v.sogou.com' + plays[m].url + easy,
                            col_type: !plays[m].picurl ? "icon_2": "movie_2"
                        })
                    } else {
                        d.push({
                            url: "https://v.sogou.com" + plays[m].url + easy,
                            img: plays[m].picurl || 'http://dlweb.sogoucdn.com/video/wap/static/img/logo/' + plays[m].sitename[1],
                            title: plays[m].sitename[0] + '—预告',
                            col_type: !plays[m].picurl ? "icon_2": "movie_2"
                        });
                    }
                }
            }
        }
        setTabs(tabs, MY_URL);
        setLists(lists, getVar(MY_URL, '0'));
    } catch(e) {
        var img = json.photo.item_list;
        d.push({
            title: '‘‘本片无选集’’',
            col_type: "text_center_1"
        });
	  for (var i in img) {
            d.push({
                img: img[i],
                col_type: "pic_1_full"
            })
        }
    }
} catch(e) {}

res.data = d;
setHomeResult(res);