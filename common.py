# -*- coding:utf-8 -*-
"""
公共信息模块
author:Mr Liu
version:1.0
"""
import configparser


class Config(object):
    """信息配置基类"""
    conf_file = 'config.cfg'
    conf_parser = configparser.ConfigParser()  # 获取配置文件解析器

    @classmethod
    def parser(cls):
        cls.conf_parser.read(cls.conf_file, encoding='utf-8')  # 解析配置文件


class TagEraseConf(Config):
    ENCODING_LIST = []     # 需要清除的编码板列表
    USER = None
    TEL_PWD_LIST = []
    DEFAULT_IP = None

    ENCODING_SECTION = 'code_plate'    # 编码板信息节点名称

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
            cls.ENCODING_LIST.append(code_value)

        # 解析telnet节点信息
        cls.USER = cls.conf_parser.get(cls.TELNET_SECTION, 'user')
        cls.TEL_PWD_LIST = str(cls.conf_parser.get(cls.TELNET_SECTION, 'password')).split(cls.SPIT_STR)
        cls.DEFAULT_IP = cls.conf_parser.get(cls.TELNET_SECTION, 'default_ip')


CONF = TagEraseConf()


def main():
    conf = TagEraseConf()
    print(conf.ENCODING_LIST)
    print(conf.USER)
    print(conf.TEL_PWD_LIST)
    print(conf.DEFAULT_IP)


if __name__ == '__main__':
    main()
