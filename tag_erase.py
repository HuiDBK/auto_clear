# -*- coding:utf-8 -*-
"""
程序主入口模块
根据编码板信息动态擦除电子标签
author:Mr Liu
version:1.0
"""
import gui
import config
import logging


def load_conf():
    """加载配置文件"""
    config.setup_logging()  # 加载日志配置文件


def main():
    load_conf()
    logging.info('\n[Program Started]')
    gui.start()


if __name__ == '__main__':
    main()