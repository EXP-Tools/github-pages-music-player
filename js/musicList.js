/**************************************************
 * GithubMusicPlayer v3.0
 * 播放列表配置模块
 *************************************************/
// 建议修改前先备份一下
// js/player.js 中开启调试模式，然后按 F12 打开浏览器的控制台。播放歌曲或点开歌单即可看到相应信息

var musicList = [
    // 以下三个系统预留列表请勿更改，否则可能导致程序无法正常运行！
    // 预留列表：搜索结果
    {
        id: "0",
        name: "搜索结果",   // 播放列表名字
        cover: "",          // 播放列表封面
        creatorName: "",        // 列表创建者名字
        creatorAvatar: "",      // 列表创建者头像
        item: [

        ]
    },
    // 预留列表：正在播放
    {
        id: "1",
        name: "正在播放",   // 播放列表名字
        cover: "images/album.png",          // 播放列表封面
        creatorName: "",        // 列表创建者名字
        creatorAvatar: "",      // 列表创建者头像
        item: [

        ]
    },
    // 预留列表：播放历史
    {
        /* 可以手动维护这个歌单，然后再把它自动生成就好了，其他功能用到再调 */
        id: "2",
        name: "播放历史",   // 播放列表名字
        cover: "images/history.png",          // 播放列表封面
        creatorName: "",        // 列表创建者名字
        creatorAvatar: "",      // 列表创建者头像
        item: [

        ]
    },
    // 以上三个系统预留列表请勿更改，否则可能导致程序无法正常运行！
    //*********************************************
    // 自定义列表，手动创建列表并添加歌曲信息
    {
        id: "9527",
        name: "Github 歌单",        // 播放列表名字
        cover: "images/album.png", // 播放列表封面图像
        creatorName: "EXP",        // 列表创建者名字(暂时没用到，可空)
        creatorAvatar: "EXP",      // 列表创建者头像(暂时没用到，可空)
        item: [                 // 这里面放歌曲（除非调试，否则这里不要手动添加，不然不会自动加载 music_list_*.json）
            /*
                {
                    id: "964fc8fd474936dc1eb50654d14703a9",
                    name: "brave heart - 初代进化曲",
                    artist: "brave heart",
                    album: "",
                    url: "static/动漫/brave heart - 初代进化曲.mp3",
                    pic: "static/动漫/brave heart - 初代进化曲.jpg",
                    lyric: "static/动漫/brave heart - 初代进化曲.lrc",
                    source: "local",
                    url_id: "964fc8fd474936dc1eb50654d14703a9",
                    pic_id: "964fc8fd474936dc1eb50654d14703a9",
                    lyric_id: "964fc8fd474936dc1eb50654d14703a9"
                },
                {
                    id: "55503cb295eecbf1bc2bed651583d0af",
                    name: "妖精的尾巴 - 星",
                    artist: "妖精的尾巴",
                    album: "「FAIRY TAIL」ORIGINAL SOUNDTRACK",
                    url: "static/动漫/妖精的尾巴 - 星.mp3",
                    pic: "static/动漫/妖精的尾巴 - 星.jpg",
                    lyric: "static/动漫/妖精的尾巴 - 星.lrc",
                    source: "local",
                    url_id: "55503cb295eecbf1bc2bed651583d0af",
                    pic_id: "55503cb295eecbf1bc2bed651583d0af",
                    lyric_id: "55503cb295eecbf1bc2bed651583d0af"
                },
                {
                    id: "666b6d82bef4b5ab0c02907a50bd1b82",
                    name: "程响 - 可能",
                    artist: "程响",
                    album: "",
                    url: "static/流行/程响 - 可能.mp3",
                    pic: "static/流行/程响 - 可能.jpg",
                    lyric: "static/流行/程响 - 可能.lrc",
                    source: "local",
                    url_id: "666b6d82bef4b5ab0c02907a50bd1b82",
                    pic_id: "666b6d82bef4b5ab0c02907a50bd1b82",
                    lyric_id: "666b6d82bef4b5ab0c02907a50bd1b82"
                }  // 列表中最后一首歌大括号后面不要加逗号
            */
        ]
    }
];