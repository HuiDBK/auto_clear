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

# 日志配置文件路径
LOG_CONF_PATH = os.path.join(common.BASE_DIR, 'config\log_conf.yaml')
print(LOG_CONF_PATH)

# 程序默认的配置文件
DEF_CONF = 'config.cfg'


class Config(object):
    """信息配置基类"""

    conf_parser = configparser.ConfigParser()  # 获取配置文件解析器

    @classmethod
    def parser(cls):
        try:
            cls.conf_parser.read(DEF_CONF, encoding='utf-8')  # 解析配置文件
        except Exception:
            print(traceback.format_exc())
            sys.exit()


class TagEraseConf(Config):
    """电子标签需要清除的配置类"""

    ENCODING_LIST = []     # 需要清除的编码板列表
    USER = None
    TEL_PWD_LIST = []
    DEFAULT_IP = None

    ENCODING_SECTION = 'encode'    # 编码板信息节点名称

    TELNET_SECTION = 'telnet'          # telnet信息节点名称

    SPIT_STR = '#'  # telnet密码分隔符

    def __init__(self):
        self.parser()

    @classmethod
    def parser(cls):
        """解析数据库配置信息"""
        super().parser()

        # 解析编码板节点信息并封装到列表中
        encoding_options = cls.conf_parser.options(cls.ENCODING_SECTION)
        for option in encoding_options:
            code_value = cls.conf_parser.get(cls.ENCODING_SECTION, option)
            cls.ENCODING_LIST.append(str(code_value).upper())

        # 解析telnet节点信息
        cls.USER = cls.conf_parser.get(cls.TELNET_SECTION, 'user')
        cls.TEL_PWD_LIST = str(cls.conf_parser.get(cls.TELNET_SECTION, 'password')).split(cls.SPIT_STR)
        cls.DEFAULT_IP = cls.conf_parser.get(cls.TELNET_SECTION, 'default_ip')

    def add_code(self, code):
        """添加编码板信息"""
        new_code_option = 'code_' + str(len(self.ENCODING_LIST)+1)
        self.conf_parser.set(self.ENCODING_SECTION, new_code_option, code)
        self.conf_parser.write(open(self.conf_file, mode='w'))
        self.ENCODING_LIST.append(str(code))

    def remove_code(self, code):
        """删除指定的编码板信息"""
        # 找到要删除编码对应的option信息
        items = self.conf_parser.items(self.ENCODING_SECTION)
        option_values = [str(item[1]).upper() for item in items]
        option_index = option_values.index(code)
        self.conf_parser.remove_option(self.ENCODING_SECTION, option=items[option_index][0])
        self.conf_parser.write(open(self.conf_file, mode='w'))
        self.ENCODING_LIST.remove(str(code))


CONFIG = TagEraseConf()

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