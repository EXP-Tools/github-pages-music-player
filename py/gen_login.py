#!/usr/bin/env python
# -*- coding: utf-8 -*-
# env: python3
# --------------------------------------------
# 生成在音乐播放页面的登录认证信息
# --------------------------------------------
# usage: 
#   python ./py/gen_login.py -u {username} -p {password}
# --------------------------------------------


import argparse
import hashlib
from color_log.clog import log

DEFAULT_ENCODING = "iso-8859-1"
PWD_PATH = "static/pwd"


def args() :
    parser = argparse.ArgumentParser(
        prog='', # 会被 usage 覆盖
        usage='python ./py/gen_login.py -u {username} -p {password}',  
        description='生成在音乐播放页面的登录认证信息',  
        epilog='\r\n'.join([
            '更多参数执行', 
            '  python ./py/gen_login.py -h', 
            '查看', 
        ])
    )
    parser.add_argument('-u', '--username', dest='username', type=str, default="admin", help='账号')
    parser.add_argument('-p', '--password', dest='password', type=str, default="654321", help='密码')
    return parser.parse_args()


def main(args) :
    username = args.username
    password = sha256(args.password)
    basicauth = to_basicauth(username, password)
    log.info(f"username: [{username}]")
    log.info(f"password: [{args.password}]")
    log.info(f"basicauth: [{basicauth}]")

    with open(PWD_PATH, "w+", encoding=DEFAULT_ENCODING) as file : 
        file.write(basicauth)
    log.info(f"登录认证信息已保存到： {PWD_PATH}")


def sha256(text):
    return hashlib.sha256(text.encode(DEFAULT_ENCODING)).hexdigest()


def to_basicauth(username, password) :
    return f"{username}:{password}"


if __name__ == "__main__" :
    main(args())
