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

# 项目根路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging.debug(BASE_DIR)
sys.path.append(BASE_DIR)

# 日志路径
INFO_LOG_PATH = os.path.join(BASE_DIR, 'log/info.log')
ERROR_LOG_PATH = os.path.join(BASE_DIR, 'log/error.log')

# 作者信息
AUTHOR_NAME = u'刘民晖'
WORK_NUM = 'W8402'
DEPARTMENT = u'测试工程部'
EMAIL = 'liuminhui W8402/uniview01'
COPY_RIGHT = u'CopyRight©2019-2020 宇视科技 uniview.com 浙ICP备5201314号'


def check_ip(ip):
    """检查IP是否有效"""
    # IPv4合法性的正则表达式
    pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return re.match(pattern, str(ip))


def main():
    print(check_ip('192.168.02'))


if __name__ == '__main__':
    main()


