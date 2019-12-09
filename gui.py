# -*- coding:utf-8 -*-
"""
图形化界面模块
author:Mr Liu
version:1.0
"""
import re
import sys
import common
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
            event, values = self.window.read()
            print(event, values)
            if event in (None, 'Quit'):
                break
            elif event in 'show_tag':
                print(event)
            elif event in u'添加编码板':
                self.__add_code(event)
            elif event in u'批量添加编码板':
                print(event)
            elif event in u'删除编码板':
                self.__delete_code(event)
            elif event in u'查看编码板信息':
                self.__show_code_info(event)
            elif event in 'erase_tag':
                print(event)

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
    def __show_code_info(event):
        """查看编码板信息"""
        code_info_list = common.CONF.ENCODING_LIST
        if code_info_list:
            code_info = ''
            for i in range(len(code_info_list)):
                if (i+1) % 6 == 0:
                    code_info += '\n'
                else:
                    code_info += code_info_list[i] + '\t'
            sg.PopupScrolled(code_info, title=u'需要删除电子标签的编码板', font=25, size=(45, 5))
        else:
            sg.Popup(u'无 编 码', title='Empty', font=45)


def main():
    MainWin(title='电子标签检测').start()


if __name__ == '__main__':
    main()
