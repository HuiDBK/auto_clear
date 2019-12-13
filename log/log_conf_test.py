# -*- coding:utf-8 -*-
"""
用配置文件配置程序日志信息
author: Mr Liu
version: 1.0
"""
import os
import sys
import yaml
import common
import logging.config


def setup_logging(default_path=common.LOG_CONF_PATH, default_level=logging.INFO, env_key="LOG_CFG"):
    """加载yaml文件配置信息"""
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        print('exists')
        with open(path, "r") as f:
            config = yaml.load(f)
            logging.config.dictConfig(config)
    else:
        print('not exists')
        logging.basicConfig(level=default_level)


def func():
    logging.info("start func")

    logging.info("exec func")

    logging.info("end func")


if __name__ == "__main__":
    setup_logging(default_path="logging.yaml")
    func()
