#!/usr/bin/env python
# -*- coding: utf-8 -*-
# env: python3
# --------------------------------------------
# 修复音乐文件的乱码元数据（歌名、艺术家、专辑）
# --------------------------------------------
# usage: 
#   python ./py/fix_metadata.py
# --------------------------------------------


import os
from mutagen.id3 import ID3, TIT2, TPE1, TALB
from color_log.clog import log

WORK_DIR = "."
MUSIC_DIR = f"{WORK_DIR}/static"
MUSIC_SUFFIXES = [ ".mp3", ".wma" ]


def main() :
    log.info(f"开始修复元数据，歌曲列表：{MUSIC_DIR}")
    for root, _, files in os.walk(MUSIC_DIR):
        for file in files:
            if not file.lower().endswith(tuple(MUSIC_SUFFIXES)) :
                continue

            music_path = os.path.join(root, file)
            music_name = file[:-4]
            fix_meta_to_utf8(music_path, music_name)

    log.info("修复完成")


# 修复歌曲文件的乱码元数据为 utf8
def fix_meta_to_utf8(music_path, music_name) :
    try:
        audio = ID3(music_path)
        album, artist, title = take_metadate(music_name)
        fix_title(audio, title)
        fix_artist(audio, artist)
        fix_album(audio, album)

        audio.save()  # 保存修改后的元数据
        log.debug(f"修复歌曲元数据成功： {music_name}")

    except:
        # 正确的元数据因为无法解码报错，无需处理
        pass


# 修正 标题 元数据
def fix_title(audio, default_title) :
    fix_metadata(audio, TIT2, 'TIT2', default_title, '<未知标题>')


# 修正 艺术家 元数据
def fix_artist(audio, default_artist) :
    fix_metadata(audio, TPE1, 'TPE1', default_artist, '<未知艺术家>')


# 修正 专辑 元数据
def fix_album(audio, default_album) :
    fix_metadata(audio, TALB, 'TALB', default_album, '<未知唱片集>')


def fix_metadata(audio, meta_class, meta_tag, default_value, unknow_value) :
    try:
        frames = audio.getall(meta_tag)  # 获取元标签的所有帧
        value = decode_gibberish(frames)
        if value == "" or value == unknow_value :
            value = default_value

        audio.delall(meta_tag)                   # 删除元标签的所有帧
        audio.add(meta_class(encoding=3, text=value))  # 添加新的元标签帧
    except:
        pass    # 正确的元数据因为无法解码报错，无需处理


# 乱码解码（以 GBK 存储的元数据会乱码）
def decode_gibberish(frames) :
    text = ""
    if frames :
        text = frames[0].text[0].encode('iso-8859-1').decode('gbk')
        text = text.strip()
    return text


# 从文件名提取元数据
def take_metadate(music_name) :
    title = ""
    artist = ""
    album = ""
    metas = music_name.split('-')

    if len(metas) == 3 :
        album = metas[0].strip()
        artist = metas[1].strip()
        title = metas[2].strip()

    elif len(metas) == 2 :
        artist = metas[0].strip()
        title = metas[1].strip()

    else :
        title = music_name

    return (album, artist, title)

    

if __name__ == "__main__" :
    main()
