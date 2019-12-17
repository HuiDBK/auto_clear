# -*- coding:utf-8 -*-
"""
配置文件模块
author: Mr Liu
version: 1.0
"""
import os
import sys
import yaml
import common
import traceback
import configparser
import logging.config
import PySimpleGUI as sg


# 日志配置文件路径
LOG_CONF_PATH = os.path.join(common.BASE_DIR, 'config\\log_conf.yaml')


# 程序默认的配置文件
DEF_CONF = os.path.join(common.BASE_DIR, 'config\\config.txt')


def setup_logging(default_path=LOG_CONF_PATH, default_level=logging.INFO, env_key="LOG_CFG"):
    """加载日志yaml配置文件信息"""
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


class Config(object):
    """信息配置基类"""

    conf_parser = configparser.ConfigParser()  # 获取配置文件解析器

    @classmethod
    def parser(cls):
        try:
            cls.conf_parser.read(DEF_CONF)  # 解析配置文件
        except Exception:
            logging.error(traceback.format_exc())
            sg.PopupError(u'\n无法正常解析配置文件\n\n请勿随意更改配置文件信息!!!\n',
                          title=u'配置文件错误', background_color='#242834', font=45, text_color='WHITE')
            sys.exit()


class TagEraseConf(Config):
    """电子标签需要清除的配置类"""

    USER = None

    DEFAULT_IP = None

    ENCODING_SECTION = 'encode'  # 编码板信息节点名称

    TELNET_SECTION = 'telnet'  # telnet信息节点名称

    WIN_SECTION = 'win_style'   # gui窗口信息节点名称

    SPIT_STR = '#'  # telnet密码分隔符

    def __init__(self):
        self.ENCODING_LIST = list()  # 需要清除的编码板列表
        self.TEL_PWD_LIST = list()   # telnet账户密码列表
        self.WIN_THEME = None
        self.parser()

    def parser(self):
        """解析数据库配置信息"""
        super().parser()

        # 解析编码板节点信息并封装到列表中
        encoding_options = self.conf_parser.options(self.ENCODING_SECTION)
        for option in encoding_options:
            code_value = self.conf_parser.get(self.ENCODING_SECTION, option)
            self.ENCODING_LIST.append(str(code_value).upper())

        # 解析telnet节点信息
        self.USER = self.conf_parser.get(self.TELNET_SECTION, 'user')
        self.TEL_PWD_LIST = str(self.conf_parser.get(self.TELNET_SECTION, 'password')).split(self.SPIT_STR)
        self.DEFAULT_IP = self.conf_parser.get(self.TELNET_SECTION, 'default_ip')

        # 解析win_style节点信息
        self.WIN_THEME = self.conf_parser.get(self.WIN_SECTION, 'win_theme')

    def add_code(self, code):
        """添加编码板信息"""
        new_code_option = 'code_' + str(len(self.ENCODING_LIST) + 1)
        self.conf_parser.set(self.ENCODING_SECTION, new_code_option, code)
        self.conf_parser.write(open(DEF_CONF, mode='w'))
        self.ENCODING_LIST.append(str(code))

    def remove_code(self, code):
        """删除指定的编码板信息"""
        # 找到要删除编码对应的option信息
        items = self.conf_parser.items(self.ENCODING_SECTION)
        option_values = [str(item[1]).upper() for item in items]
        option_index = option_values.index(code)
        self.conf_parser.remove_option(self.ENCODING_SECTION, option=items[option_index][0])
        self.conf_parser.write(open(DEF_CONF, mode='w'))
        self.ENCODING_LIST.remove(str(code))

    def add_tel_pwd(self, add_tel_pwd):
        """添加Telnet密码"""
        tel_pwd = self.conf_parser.get(self.TELNET_SECTION, 'password')
        new_tel_pwd = tel_pwd + '#' + add_tel_pwd
        self.conf_parser.set(self.TELNET_SECTION, 'password', new_tel_pwd)
        self.conf_parser.write(open(DEF_CONF, mode='w'))
        self.TEL_PWD_LIST.append(add_tel_pwd)

    def change_win_theme(self, new_theme):
        """
        改变窗口主题
        :param new_theme: 新主题名称
        """
        self.conf_parser.set(self.WIN_SECTION, 'win_theme', new_theme)
        self.conf_parser.write(open(DEF_CONF, mode='w'))
        self.WIN_THEME = new_theme


def main():
    conf = TagEraseConf()
    print(conf.ENCODING_LIST)
    print(conf.USER)
    print(conf.TEL_PWD_LIST)
    print(conf.DEFAULT_IP)
    print(conf.conf_parser.items(conf.ENCODING_SECTION))
    items = [option[1] for option in list(conf.conf_parser.items(conf.ENCODING_SECTION))]
    print(items)
    print(items.index('0302C1E4'))


if __name__ == '__main__':
    main()
