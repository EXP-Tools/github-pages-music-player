#!/usr/bin/env python
# -*- coding: utf-8 -*-
# env: python3
# --------------------------------------------
# 生成仓库所有音乐文件的路径，供播放器读取（ajax.js loadLocalMusicList）
#  （可人工执行、亦可通过 Github Action 在 PR 时触发）
# --------------------------------------------
# usage: 
#   python ./py/gen_music_list.py -i {ignore_dir_keyword1,ignore_dir_keyword2,ignore_dir_keyword3,...}
# --------------------------------------------


import argparse
import glob
import os
import re
import json
import hashlib
from mutagen.easyid3 import EasyID3
from datetime import datetime
from color_log.clog import log

DEFAULT_ENCODING = "utf-8"
WORK_DIR = "."
MUSIC_DIR = f"{WORK_DIR}/static"
MUSIC_LIST_PERFIX = "music_list"
MUSIC_LIST = f"{MUSIC_DIR}/{MUSIC_LIST_PERFIX}_%s.json"
MUSIC_LIST_JS = "js/player.js"
MUSIC_SUFFIXES = [ ".mp3", ".wma" ]
LYRIC_SUFFIX = ".lrc"
PIC_SUFFIX = ".jpg"


def args() :
    parser = argparse.ArgumentParser(
        prog='', # 会被 usage 覆盖
        usage='python ./py/gen_music_list.py -i {ignore_dir_keyword1,ignore_dir_keyword2,ignore_dir_keyword3,...}',  
        description='生成 static 目录下的音乐歌单，允许跳过一些目录',  
        epilog='\r\n'.join([
            '更多参数执行', 
            '  python ./py/gen_music_list.py -h', 
            '查看', 
        ])
    )
    parser.add_argument('-i', '--ignores', dest='ignores', type=str, default="", help='忽略目录列表（关键字即可），多个用英文逗号分隔')
    return parser.parse_args()


def main(args) :
    if args.ignores :
        ignores = [x.strip() for x in args.ignores.split(',')]
    else :
        ignores = []

    # 创建歌曲列表
    musiclist = MusicList(
        id="9527",
        name="Github 歌单",
        cover="images/album.png",
        creatorName="EXP",
        creatorAvatar="images/avatar.jpg"
    )
    log.info(f"开始生成歌单：【{musiclist.name}】")

    # 遍历所有文件
    for root, _, files in os.walk(MUSIC_DIR):

        if any(kw in root.lower() for kw in ignores) :
            log.warn(f"跳过目录： {root}")
            continue
        
        for file in files:
            if not file.lower().endswith(tuple(MUSIC_SUFFIXES)) :
                continue

            absolute_path = os.path.join(root, file)
            rel_path = os.path.relpath(absolute_path, WORK_DIR).replace("\\", "/")
            rel_dir = os.path.dirname(rel_path)
            music_name = file[:-4]
            
            lyric_path = f"{rel_dir}/{music_name}{LYRIC_SUFFIX}"
            pic_path = f"{rel_dir}/{music_name}{PIC_SUFFIX}"

            # 检查歌词文件和封面图片文件是否存在
            if not os.path.exists(os.path.join(WORK_DIR, lyric_path)) :
                lyric_path = ""
            if not os.path.exists(os.path.join(WORK_DIR, pic_path)) :
                pic_path = ""

            # 获取 MP3 文件的元数据
            try:
                audio = EasyID3(absolute_path)
                artist = audio.get('artist', [''])[0]
                album = audio.get('album', [''])[0]
            except:
                artist = ""
                album = ""

            # 创建 Music 对象
            music = Music(
                id=calculate_md5(absolute_path),
                name=music_name,
                artist=artist,
                album=album,
                pic=pic_path,
                url=rel_path,
                lyric=lyric_path
            )
            musiclist.add(music)

    del_music_lists()
    musiclist_path = MUSIC_LIST % now()
    musiclist.save_to_file(musiclist_path)
    to_js(musiclist_path)
    log.info(f"完成，共收录 {musiclist.size()} 首歌曲")


def calculate_md5(file_path):
    return hashlib.md5(file_path.encode()).hexdigest().lower()


def now() :
    return datetime.now().strftime('%Y%m%d%H%M%S')


def del_music_lists() :
    path = f"{MUSIC_DIR}/{MUSIC_LIST_PERFIX}*"  # 使用 glob 来找到所有以'music_list'开头的文件
    files = glob.glob(path)
    for file in files:
        try:
            os.remove(file)
        except:
            pass


def to_js(musiclist_path) :
    with open(MUSIC_LIST_JS, 'r', encoding=DEFAULT_ENCODING) as file:
        content = file.read()

    content = re.sub(
        r'githubAPI:\s*"' + MUSIC_DIR + r'/' + MUSIC_LIST_PERFIX + r'.*"', 
        f'githubAPI: "{musiclist_path}"', 
        content
    )

    with open(MUSIC_LIST_JS, 'w', encoding=DEFAULT_ENCODING) as file:
        file.write(content)


class MusicList:
    def __init__(self, id, name, cover, creatorName, creatorAvatar):
        self.id = id
        self.name = name
        self.cover = cover
        self.creatorName = creatorName
        self.creatorAvatar = creatorAvatar
        self.item = []

    def add(self, music):
        self.item.append(music.__dict__)

    def size(self) :
        return len(self.item)

    def save_to_file(self, file_path):
        with open(file_path, 'w+', encoding=DEFAULT_ENCODING) as file:
            json.dump([self.__dict__], file, ensure_ascii=False, indent=4)

class Music:
    def __init__(self, id, name, artist, album, pic, url, lyric, source="local", url_id=None, pic_id=None, lyric_id=None):
        self.id = id
        self.name = name
        self.artist = artist
        self.album = album
        self.url = url
        self.pic = pic
        self.lyric = lyric
        self.source = source
        self.url_id = "" if not url else id
        self.pic_id = "" if not pic else id
        self.lyric_id = "" if not lyric else id


if __name__ == "__main__" :
    main(args())
