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
import config
import common
import threading
import PySimpleGUI as sg


sg.change_look_and_feel('DarkBlue1')  # 窗口主题


class BaseWin(object):
    """窗口基类"""

    FONT_SIZE = 18  # 默认字体大小
    DIALOG_FONT_SIZE = 25   # 对话框的字体大小
    DISABLE_FONT_COLOR = "BLACK"  # 控件不可用的字体颜色

    LOGO = common.BASE_DIR + '/image/unv.png'

    def __init__(self):
        pass


class MainWin(BaseWin):
    """主窗口"""

    # 程序默认配置文件
    CONF = config.TagEraseConf()

    # 菜单项
    menu_def = [
        [u'编码板信息', [u'添加编码板', u'删除编码板', u'批量添加编码板', u'查看编码板信息']],
        [u'Telnet信息', [u'添加Telnet密码', u'查看账户和密码']],
        [u'帮助', [u'导出日志', u'关于作者', ]],
    ]

    def __init__(self, title):
        self.title = title  # 窗口标题
        self.window = None  # 窗口对象
        self.layout = None  # 窗口布局
        self.__init_layout()

    def __init_layout(self):
        """初始化窗口布局"""
        self.layout = [
            [sg.Menu(self.menu_def, key='menu', tearoff=True)],
            [
                sg.Text(u'Telnet用户:'),
                sg.InputText(self.CONF.USER, text_color=self.DISABLE_FONT_COLOR,
                             size=(20, 20), key='telnet_user', disabled=True)
            ],
            [
                sg.Text(u'Telnet密码:'),
                sg.InputText(str(self.CONF.TEL_PWD_LIST[0]), text_color=self.DISABLE_FONT_COLOR,
                             size=(20, 20), key='telnet_pwd', disabled=True)
            ],
            [
                sg.Text(u'默 认 IP:'),
                sg.InputText(self.CONF.DEFAULT_IP, text_color=self.DISABLE_FONT_COLOR,
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
            else:
                self.__handle_events(event, value_dict)
        self.window.close()
        sg.quit()
        sys.exit(0)

    def __handle_events(self, event, value_dict):
        """
        统一处理事件,降低代码的冗余性
        :param event:事件
        :param value_dict:窗口内容字典
        """

        # 开启另一个窗口时,让主窗口不可用,防止用户刻意多次点击造成不如意的结果
        self.window.disable()
        if event in u'添加编码板':
            self.__add_code(event)
        elif event in u'删除编码板':
            self.__delete_code(event)
        elif event in u'批量添加编码板':
            self.__batch_add_code(event)
        elif event in u'查看编码板信息':
            self.__show_code_info(event)
        # elif event in u'添加Telnet账户':
        #     print(event)
        elif event in u'添加Telnet密码':
            self.__add_tel_pwd()
        elif event in u'查看账户和密码':
            self.__show_tel_info()
        elif event in u'导出日志':
            print(event)
        elif event in u'关于作者':
            self.__about_author(event)
        elif event in 'show_tag':
            self.__show_dev_tag(value_dict, event)
        elif event in 'erase_tag':
            self.__erase_dev_tag(value_dict, event)
        self.window.enable()

    def __delete_code(self, event):
        """删除编码,修改配置文件信息"""
        code = str(sg.PopupGetText(u'请输入要删除的编码', event, keep_on_top=True)).upper()
        if code and code not in 'NONE':
            if self.check_code(code):
                # 判断删除的编码是否在配置文件中
                if code in self.CONF.ENCODING_LIST:
                    self.CONF.remove_code(code)
                    sg.Popup(u'\n %s 编码删除成功\n' % code, title=u'移除成功', keep_on_top=True, font=self.DIALOG_FONT_SIZE)
                else:
                    sg.Popup(u'\n配置文件不存在 %s 编码无需删除\n' % code, title=u'编码不存在', keep_on_top=True, font=self.DIALOG_FONT_SIZE)
                    self.__delete_code(event)
            else:
                sg.Popup(
                    u'\n %s 编码格式错误,请输入正确的编码格式\n\n例如:0302C1E5\n' % code,
                    title='编码格式错误',
                    font=self.DIALOG_FONT_SIZE,
                    keep_on_top=True
                )
                self.__delete_code(event)

    @staticmethod
    def check_code(content):
        """检查编码格式"""
        # 8位由字母加数字组成的正则表达式,不区分大小写
        pattern = re.compile(r'^[a-zA-Z0-9]{8}$')
        return re.match(pattern, content)

    def __add_code(self, event):
        """添加编码,修改配置文件信息"""
        code = str(sg.PopupGetText(u'请输入要添加的编码', event, keep_on_top=True, font=self.DIALOG_FONT_SIZE)).upper()
        print(code)
        if code and code not in 'NONE':
            if self.check_code(code):
                # 判断添加的编码是否重复
                if code in self.CONF.ENCODING_LIST:
                    sg.Popup(u'\n配置文件存在 %s 编码无需添加\n' % code, title=u'编码存在', keep_on_top=True, font=self.DIALOG_FONT_SIZE)
                    self.__add_code(event)
                else:
                    self.CONF.add_code(code)
                    sg.Popup(u'\n %s 编码添加成功\n' % code, title=u'添加成功', keep_on_top=True, font=self.DIALOG_FONT_SIZE)
            else:
                sg.Popup(
                    u'\n %s 编码格式错误,请输入正确的编码格式\n\n例如:0302C1E5\n' % code,
                    title=u'编码格式错误',
                    font=self.DIALOG_FONT_SIZE,
                    keep_on_top=True
                )
                self.__add_code(event)

    def __show_code_info(self, event):
        """查看需要要擦除的编码板信息"""
        code_info_list = self.CONF.ENCODING_LIST
        if code_info_list:
            code_info = ''
            for i in range(len(code_info_list)):
                if (i + 1) % 6 == 0:
                    code_info += '\n'
                else:
                    code_info += code_info_list[i] + '\t'
            sg.PopupScrolled(code_info, title=u'需要删除电子标签的编码板:', font=self.DIALOG_FONT_SIZE, size=(45, 5))
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
        if not dev_ip:
            # 无手输设备IP,使用默认IP
            dev_ip = value_dict['def_ip']
            print(dev_ip)

        if common.check_ip(dev_ip):  # 检查IP的合法性
            print('合法IP')
            if utils.TelnetClient.check_telnet(dev_ip):  # 检查IP的是否可以进入telnet
                ipc = utils.IPCTelnet(dev_ip)
                if ipc.login():  # 判断设备是否登录成功
                    ipc_manuinfo = str(ipc.manuinfo).upper()  # 取出IPC的电子标签
                    if flag == 'show_tag':
                        print("登录成功,查看电子标签,长度%d" % len(ipc_manuinfo))
                        if len(ipc_manuinfo) > 200:
                            sg.PopupScrolled(ipc_manuinfo, title=u'电子标签', font=self.DIALOG_FONT_SIZE, size=(52, 25))
                        else:
                            sg.PopupScrolled(ipc_manuinfo, title=u'电子标签', font=self.DIALOG_FONT_SIZE, size=(52, 8))
                    elif flag == 'erase_tag':
                        print("登录成功,删除电子标签")
                        # 根据@符号的个数来判断电子标签是否为空
                        if ipc_manuinfo.count('@') <= 2:
                            sg.Popup(u'\n该设备的电子标签为空,无需删除\n\n请人工排查是否正确\n',
                                     title=u'电子标签为空', font=self.DIALOG_FONT_SIZE, text_color='red')
                            return

                        # 判断配置文件的要删除电子标签的编码板信息是否在该设备的电子标签中
                        index = ipc_manuinfo.find('ENC-')
                        print(index)
                        if index == -1:  # 没有找到ENC-说明电子标签不完整
                            sg.Popup(u'该设备的电子标签不完整,请人工检查电子标签是否正确\n\n%s\n'
                                     % ipc_manuinfo.replace('\r', ''),
                                     title=u'电子标签不完整', font=self.DIALOG_FONT_SIZE, text_color='white')
                            return
                        index += 4
                        encode = ipc_manuinfo[index: index + 8]  # 截取编码板信息
                        print(encode)
                        if encode in self.CONF.ENCODING_LIST:
                            print('需要删除')
                            result = ipc.manuinfo_erase()
                            print(result)
                            sg.Popup(u'\n电子标签删除成功,根据%s编码板\n' % encode, title=u'删除成功', font=self.DIALOG_FONT_SIZE, text_color='#08F61A')
                        else:
                            print('无需删除')
                            sg.Popup(u'无需删除,该设备的%s编码不在配置文件中\n\n如需删除请把%s编码添加到配置文件中\n'
                                     % (encode, encode), title=u'电子标签无需删除', font=self.DIALOG_FONT_SIZE, text_color='#08F61A')
                else:
                    print("登录失败")
                    sg.Popup(u'Telnet无法登录', title=u'登录失败', font=self.DIALOG_FONT_SIZE, text_color='red')
            else:
                print('网络不通或者工厂模式关闭')
                sg.Popup(u'网络不通或者工厂模式关闭', title=u'网络不通', font=self.DIALOG_FONT_SIZE, text_color='red')
        else:
            sg.Popup(
                u'手输设备IP: %s 格式不正确\n\n正确格式例如: 192.168.0.12' % dev_ip,
                title=u'IP格式错误',
                font=self.DIALOG_FONT_SIZE,
                text_color='red'
            )

    def __erase_dev_tag(self, value_dict, event):
        """
        删除设备的电子标签
        :param value_dict: 窗口信息字典
        """
        self.__choose_dev_fn(value_dict, event)

    def __about_author(self, event):
        """关于作者的信息"""
        author_info = u'姓名: %s\n\n\n工号: %s\n\n\n邮箱: %s\n\n\n%s\n' % \
                      (common.AUTHOR_NAME, common.WORK_NUM, common.EMAIL, common.COPY_RIGHT)
        sg.Popup(author_info, title=u'关于作者', font=self.DIALOG_FONT_SIZE)

    def __batch_add_code(self, event=None):
        """批量添加要删除电子标签的编码"""
        tip_msg = u'批量添加要删除电子标签的编码, 每个编码一行'
        layout = [
            [sg.T(tip_msg, font=self.DIALOG_FONT_SIZE)],
            [sg.Multiline(key='codes', size=(45, 20), font=self.DIALOG_FONT_SIZE)],
            [sg.Ok(u'批量添加')]
        ]
        batch_add_win = sg.Window(u'批量添加编码', layout)
        event, value_dict = batch_add_win.read()

        if event in ('None', None):     # 点击关闭按钮X
            batch_add_win.close()
            return

        # 判断没有输入编码数据
        if not str(value_dict['codes']).replace('\n', ''):
            sg.Popup(u'没有输入任何编码信息', title='无输入', font=self.DIALOG_FONT_SIZE)
            batch_add_win.close()
            return

        # 去除空格, \t并按'\n'切割,最后去除重复值
        code_list = set(str(value_dict['codes']).replace(' ', '').replace('\t', '').split('\n'))

        # 去除空值并取出符合8位由字母加数字的正则的元素
        code_list = [code for code in code_list if code != '']
        code_set = set()
        for code in code_list:
            result = re.search(r'[a-zA-Z0-9]{8}', code)
            if result:
                code = result.group(0)
                # 判断是否是0302编码前缀
                if code.startswith('0302'):
                    code_set.add(code.upper())

        if not code_set:
            sg.Popup(u'\n输入的编码没有符合要求\n', title=u'无编码添加', font=self.DIALOG_FONT_SIZE)
            batch_add_win.close()
            return

        if code_set.issubset(self.CONF.ENCODING_LIST):
            # 配置文件已存在，无需添加
            sg.Popup(u'\n配置文件已存在\n\n%s，无需添加\n' % code_set, title=u'无需添加', keep_on_top=True, font=self.DIALOG_FONT_SIZE)
            batch_add_win.close()
            return

        # 取出不在配置文件中的元素
        ok_list = list(code_set.difference(self.CONF.ENCODING_LIST))

        if ok_list:
            result = ''
            for i in range(len(ok_list)):
                if (i + 1) % 6 == 0:
                    result += '\n'
                else:
                    result += ok_list[i] + '\t'
                self.CONF.add_code(ok_list[i])
                self.CONF.ENCODING_LIST.append(ok_list[i])
            sg.PopupScrolled(u'%s 个编码添加成功分别为:\n%s' % (len(ok_list), result),
                             title=u'添加成功', keep_on_top=True, font=self.DIALOG_FONT_SIZE)
        else:
            sg.Popup(u'\n输入的编码没有符合要求\n', title=u'无编码添加', font=self.DIALOG_FONT_SIZE)
        batch_add_win.close()

    # 暂时不开放添加Telnet用户功能
    # def __add_tel_user(self):
    #     """添加Telnet用户"""
    #     title = u'添加Telnet用户'
    #     user = sg.PopupGetText(u'请输入要添加的Telnet用户', title, keep_on_top=True, font=self.DIALOG_FONT_SIZE)
    #     pass

    def __add_tel_pwd(self):
        """添加Telnet密码"""
        title = u'添加Telnet密码'
        tel_pwd = sg.PopupGetText(u'请输入要添加的Telnet密码', title, keep_on_top=True, font=self.DIALOG_FONT_SIZE)
        print(tel_pwd)
        if tel_pwd:
            if tel_pwd in self.CONF.TEL_PWD_LIST:
                sg.Popup(u'\n%s 密码已存在,无需添加\n' % tel_pwd, title=u'密码存在', font=self.DIALOG_FONT_SIZE)
            else:
                self.CONF.add_tel_pwd(tel_pwd)
                self.CONF.TEL_PWD_LIST.append(tel_pwd)
                sg.Popup(u'\n成功添加 %s Telnet密码\n' % tel_pwd, title=u'添加成功', font=self.DIALOG_FONT_SIZE)

    def __show_tel_info(self):
        """显示Telnet账户信息"""
        telnet_info = '\nTelnet用户: %s\n\n' \
                      'Telnet密码: %s\n' % (self.CONF.USER, self.CONF.TEL_PWD_LIST)
        sg.Popup(telnet_info, title='Telnet账户信息:', font=self.DIALOG_FONT_SIZE)


def start():
    """开启程序图形化界面"""
    MainWin(title='电子标签检测').start()


def open_factorymode():
    """开启设备的工厂模式"""
    def_ip = '192.168.0.13'
    # start_time = time.time()
    while True:
        print('test')
        ipc = utils.IPCTelnet(def_ip)
        if ipc.login():
            ipc.open_fac_mode()
            ipc.reboot()
            break
        time.sleep(1)
        # if (time.time() - start_time) > 10:     # 超时退出循环
        #     break
    print('exit fn')


def main():
    # 利用设备刚上电有一段ip是192.168.0.13的时间
    # 开一个线程去开启设备的工厂模式防止进不去telnet
    open_fac_t = threading.Thread(target=open_factorymode)
    open_fac_t.start()
    MainWin(title='电子标签检测').start()


if __name__ == '__main__':
    main()
    # check_ip_state_win("192.168.0.12")
