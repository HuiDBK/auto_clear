# -*- coding:utf-8 -*-
"""
图形化界面模块
author:Mr Liu
version:1.0
"""
# from gevent import monkey; monkey.patch_all()
import re
import sys
import time
import utils
import common
# import gevent
import threading
import multiprocessing
import PySimpleGUI as sg

sg.change_look_and_feel('DarkBlue1')  # 窗口主题


class BaseWin(object):
    """窗口基类"""

    FONT_SIZE = 18  # 字体大小
    DISABLE_FONT_COLOR = "BLACK"  # 控件不可用的字体颜色

    LOGO = './image/unv.png'

    def __init__(self):
        pass


class MainWin(BaseWin):
    """主窗口"""
    # 菜单项
    menu_def = [[u'编码板信息', [u'添加编码板', '批量添加编码板', u'删除编码板', u'查看编码板信息']],
                [u'帮助', u'关于作者'], ]

    def __init__(self, title):
        self.title = title
        self.window = None
        self.layout = None
        self.__init_layout()

    def __init_layout(self):
        """初始化窗口布局"""
        self.layout = [
            [sg.Menu(self.menu_def, key='menu', tearoff=True)],
            [
                sg.Text(u'Telnet用户:'),
                sg.InputText(common.CONF.USER, text_color=self.DISABLE_FONT_COLOR,
                             size=(20, 20), key='telnet_user', disabled=True)
            ],
            [
                sg.Text(u'Telnet密码:'),
                sg.InputText(str(common.CONF.TEL_PWD_LIST[0]), text_color=self.DISABLE_FONT_COLOR,
                             size=(20, 20), key='telnet_pwd', disabled=True)
            ],
            [
                sg.Text(u'默 认 IP:'),
                sg.InputText(common.CONF.DEFAULT_IP, text_color=self.DISABLE_FONT_COLOR,
                             size=(20, 20), pad=(31, 0), key='def_ip', disabled=True)
            ],
            [
                sg.Text(u'设 备 IP:'),
                sg.InputText('', size=(20, 20), pad=(31, 0), text_color='YELLOW', key='dev_ip')],
            [
                sg.Button(u'查看电子标签', key='show_tag'),
                sg.Button(u'清除电子标签', key='erase_tag'),
                sg.Image(filename=self.LOGO, tooltip='UNV'),
            ],
        ]

    def start(self):
        """开启主窗口"""
        self.window = sg.Window(title=self.title, layout=self.layout, element_padding=(5, 30),
                                font=('宋体', self.FONT_SIZE))
        # 开启事件监听
        self.__event_handler()

    def __event_handler(self):
        while True:
            event, value_dict = self.window.read()
            print(event, value_dict)
            if event in (None, 'Quit'):
                break
            elif event in u'添加编码板':
                self.__add_code(event)
            elif event in u'批量添加编码板':
                print(event)
            elif event in u'删除编码板':
                self.__delete_code(event)
            elif event in u'查看编码板信息':
                self.__show_code_info(event)
            elif event in 'show_tag':
                self.__show_dev_tag(value_dict, event)
            elif event in 'erase_tag':
                self.__erase_dev_tag(value_dict, event)

        self.window.close()
        sg.quit()
        sys.exit(0)

    def __delete_code(self, event):
        """删除编码,修改配置文件信息"""
        code = str(sg.PopupGetText(u'请输入要删除的编码', event, keep_on_top=True)).upper()
        if code and code not in 'NONE':
            if self.__check_code(code):
                # 判断删除的编码是否在配置文件中
                if code in common.CONF.ENCODING_LIST:
                    common.CONF.remove_code(code)
                    sg.Popup(u'%s编码删除成功' % code, title='RemoveSuccess', keep_on_top=True, font=25)
                else:
                    sg.Popup(u'配置文件不存在%s编码无需删除' % code, title='CodeNoExist', keep_on_top=True, font=25)
                    self.__delete_code(event)
            else:
                sg.Popup(
                    u'%s编码格式错误,请输入正确的编码格式\n\n例如:0302C1E5' % code,
                    title='编码格式错误',
                    font=25,
                    keep_on_top=True
                )
                self.__delete_code(event)

    @staticmethod
    def __check_code(content):
        """检查编码格式"""
        # 8位由字母加数字组成的正则表达式,不区分大小写
        pattern = re.compile(r'^[a-zA-Z0-9]{8}$')
        return re.match(pattern, content)

    def __add_code(self, event):
        """添加编码,修改配置文件信息"""
        code = str(sg.PopupGetText(u'请输入要添加的编码', event, keep_on_top=True, font=25)).upper()
        print(code)
        if code and code not in 'NONE':
            if self.__check_code(code):
                # 判断添加的编码是否重复
                if code in common.CONF.ENCODING_LIST:
                    sg.Popup(u'配置文件存在%s编码无需添加' % code, title='CodeRepeat', keep_on_top=True, font=25)
                    self.__add_code(event)
                else:
                    common.CONF.add_code(code)
                    sg.Popup(u'%s编码插入成功' % code, title='InsertSuccess', keep_on_top=True, font=25)
            else:
                sg.Popup(
                    u'%s编码格式错误,请输入正确的编码格式\n\n例如:0302C1E5' % code,
                    title='编码格式错误',
                    font=25,
                    keep_on_top=True
                )
                self.__add_code(event)

    @staticmethod
    def __show_code_info():
        """查看需要要擦除的编码板信息"""
        code_info_list = common.CONF.ENCODING_LIST
        if code_info_list:
            code_info = ''
            for i in range(len(code_info_list)):
                if (i + 1) % 6 == 0:
                    code_info += '\n'
                else:
                    code_info += code_info_list[i] + '\t'
            sg.PopupScrolled(code_info, title=u'需要删除电子标签的编码板', font=25, size=(45, 5))
        else:
            sg.Popup(u'无 编 码', title='Empty', font=45)

    def __show_dev_tag(self, value_dict, event):
        """
        查看设备的电子标签
        :param value_dict: 窗口信息字典
        """
        # print(value_dict)
        dev_ip = value_dict['dev_ip']
        self.__choose_dev_fn(value_dict, event)

    def __choose_dev_fn(self, value_dict, flag):
        """
        选择查看或者删除设备的电子标签
        :param value_dict: 窗口信息字典
        :param flag: 实现功能标识  -->  flag = 'show_tag' 显示, flag='erase_tag' 擦除
        """
        dev_ip = value_dict['dev_ip']
        if dev_ip:
            # 手动输入了设备IP
            if common.check_ip(dev_ip):
                print('合法IP')
                if utils.TelnetClient.check_telnet(dev_ip):
                    # IP ping 通进入IPC终端
                    ipc = utils.IPCTelnet(dev_ip)
                    if ipc.login():
                        # 通过flag来标识具体实现什么功能
                        ipc_manuinfo = str(ipc.manuinfo).upper()
                        if flag == 'show_tag':

                            print("登录成功,查看电子标签")
                            if len(ipc_manuinfo) > 200:
                                sg.PopupScrolled(ipc_manuinfo, title=u'电子标签', font=25, size=(52, 25))
                            else:
                                sg.PopupScrolled(ipc_manuinfo, title=u'电子标签', font=25, size=(52, 8))
                        elif flag == 'erase_tag':
                            print("登录成功,删除电子标签")
                            # 判断配置文件的要删除电子标签的编码板信息是否在该设备的电子标签中
                            is_exist = False    # 默认标识不存在
                            index = ipc_manuinfo.find('ENC-')
                            print(index)
                            index += 4
                            encode = ipc_manuinfo[index: index+8]   # 截取编码板信息
                            print(encode)
                            for code in common.CONF.ENCODING_LIST:
                                if code in ipc_manuinfo:
                                    # 存在删除
                                    is_exist = True
                                    result = ipc.manuinfo_erase()
                                    print(result)
                                    break
                            if is_exist:
                                sg.Popup(u'删除成功', title=u'删除成功', font=25)
                            else:
                                print('不存在配置文件无需删除')
                                sg.Popup(
                                    u'该电子标签的编码板不在配置文件中无需删除',
                                    title=u'无需删除', font=25)
                    else:
                        print("登录失败")
                        sg.Popup(u'Telnet无法登录', title=u'登录失败', font=25, text_color='red')
                else:
                    print('网络不通或者工厂模式关闭')
                    sg.Popup(u'网络不通或者工厂模式关闭', title=u'网络不通', font=25, text_color='red')
            else:
                sg.Popup(
                    u'手输设备IP: %s 格式不正确\n\n正确格式例如: 192.168.0.12' % dev_ip,
                    title=u'IP格式错误',
                    font=25,
                    text_color='red'
                )
        else:
            print('无手动输入设备IP使用默认IP')
            def_ip = value_dict['def_ip']
            if utils.TelnetClient.check_telnet(def_ip):
                # IP ping 通进入IPC终端
                ipc = utils.IPCTelnet(def_ip)
                if ipc.login():
                    print('登录成功,查看电子标签')
                    if len(ipc.manuinfo) > 200:
                        sg.PopupScrolled(ipc.manuinfo, title=u'电子标签', font=25, size=(52, 25))
                    else:
                        sg.PopupScrolled(ipc.manuinfo, title=u'电子标签', font=25, size=(52, 8))
                else:
                    print("登录失败")
                    sg.Popup(u'Telnet无法登录', title=u'登录失败', font=25, text_color='red')
            else:
                print('网络不通或者工厂模式关闭')
                sg.Popup(u'网络不通或者工厂模式关闭', title=u'网络不通', font=25, text_color='red')

    def __erase_dev_tag(self, value_dict, event):
        """
        删除设备的电子标签
        :param value_dict: 窗口信息字典
        """
        self.__choose_dev_fn(value_dict, event)


def main():
    MainWin(title='电子标签检测').start()


if __name__ == '__main__':
    main()
    # check_ip_state_win("192.168.0.12")