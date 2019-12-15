# -*- coding:utf-8 -*-
"""
用配置文件配置程序日志信息
author: Mr Liu
version: 1.0
"""
import os
import yaml
import config
import logging.config


def setup_logging(default_path=config.LOG_CONF_PATH, default_level=logging.INFO, env_key="LOG_CFG"):
    """加载yaml文件配置信息"""
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "r") as log_file:
            conf = yaml.load(log_file, Loader=yaml.FullLoader)
            logging.config.dictConfig(conf)
    else:
        logging.basicConfig(level=default_level)


def func():
    logging.info("start func")

    logging.info("exec func")

    logging.info("end func")


if __name__ == "__main__":
    setup_logging()
    func()
