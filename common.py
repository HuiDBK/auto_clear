# -*- coding:utf-8 -*-
"""
公共信息模块
author:Mr Liu
version:1.0
"""
import re
import os
import sys
import logging
import traceback
import configparser

# 项目根路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
sys.path.append(BASE_DIR)

# 作者信息
AUTHOR_NAME = u'刘民晖'
WORK_NUM = 'W8402'
EMAIL = 'liuminhui W8402/uniview01'
COPY_RIGHT = u'CopyRight©2019-2020 宇视科技 uniview.com 浙ICP备5201314号'


def check_ip(ip):
    """检查IP是否有效"""
    # ip合法性的正则表达式
    pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return re.match(pattern, ip)


def main():
    pass


if __name__ == '__main__':
    main()


