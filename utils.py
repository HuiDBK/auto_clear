# -*- coding:utf-8 -*-
"""
工具模块，提供便捷的工具类、函数
author:Mr Liu
version:1.0
"""
import config
import logging
import telnetlib


class TelnetClient(object):
    """Telnet终端基类"""
    port = 23

    def __init__(self, host_ip):
        self.host_ip = host_ip
        self.telnet_client = telnetlib.Telnet()

    def execute_cmd(self, cmd: str):
        """
        执行telnet终端命令
        返回结果由不同的Telnet终端实现
        """
        self.telnet_client.write(cmd.encode(encoding='ascii') + b'\n')

    @staticmethod
    def check_telnet(ip):
        """
        检查telnet通不通
        :return bool
        """
        telnet_status = False
        try:
            telnet_result = telnetlib.Telnet(host=ip, port=23, timeout=2)
            telnet_status = True
        except:
            pass
        return telnet_status

    def quit(self):
        """退出telnet客户端"""
        pass


class IPCTelnet(TelnetClient):
    """IPC Telnet终端类"""

    # _instance_lock = threading.Lock()
    equipment_flag = False  # 标识是否进入装备模式

    # 进入装备模式命令和装备调试命令列表
    equipment_commands = (
        '_hide box', 'display version all board', 'display manuinfo',
        'clear manuinfo', 'clear information', 'test irled ctrl',
        'test rtc gettime', 'test rtc getzone', 'test rtc settime',
        'test rtc setzone', 'test ethernet get mac', 'test ethernet set mac',
        'test tf get status', 'set serverip', 'get serverip', 'q', 'quit'
    )

    # def __new__(cls, *args, **kwargs):
    #     """重写__new__方法实现单例"""
    #     if not hasattr(IPCTelnet, "_instance"):
    #         with IPCTelnet._instance_lock:
    #             if not hasattr(IPCTelnet, "_instance"):
    #                 IPCTelnet._instance = object.__new__(cls)
    #     return IPCTelnet._instance

    def __init__(self, ipc_ip):
        super().__init__(ipc_ip)
        self.TEL_CONF = config.TagEraseConf()
        self.username = self.TEL_CONF.USER
        self.passwords = self.TEL_CONF.TEL_PWD_LIST
        self.login_status = False
        self.telnet_client.set_debuglevel(0)

    def login(self, user, pwd):
        """登录IPC终端"""
        try:
            self.telnet_client.open(self.host_ip, self.port)
        except:
            self.login_status = False

        # 等待login: 出现,最多等待5s
        self.telnet_client.read_until(b'login:', timeout=5)

        # 以ASCII码的方式写入用户名
        self.telnet_client.write(user.encode('ascii') + b'\n')
        self.telnet_client.read_until(b'Password:', timeout=5)
        self.telnet_client.write(pwd.encode('ascii') + b'\n')
        login_result = self.telnet_client.read_until(b'User@/root>', timeout=10).decode(encoding='ascii')

        # 5秒后还没读取到User@/root>判断账号密码是否错误
        if 'Login incorrect' in login_result:
            self.login_status = False
            logging.info('telnet user[%s] pwd[%s] error\n' % (user, pwd))
        elif 'User@/root>' in login_result:
            self.login_status = True
            logging.info('login success telnet user[%s] pwd[%s]\n' % (user, pwd))
            return self.login_status
        else:
            logging.info('login telnet unknown exception\n')
            self.login_status = False
        return self.login_status

    def execute_cmd(self, cmd: str):
        """
        执行IPC终端命令并获
        :param cmd:
        :return: 执行命令之后的信息
        """

        super().execute_cmd(cmd)
        # 装备模式命令特殊处理
        if cmd in '_hide box':
            self.equipment_flag = True
        if cmd in self.equipment_commands and self.equipment_flag:
            # 装备模式下的命令获取返回结果
            if cmd in 'clear information':
                # 清除配置需要输入y同意才可
                self.telnet_client.read_until(b'Are you sure?(Y/N)', timeout=5).decode('ascii')
                super().execute_cmd('y')
            elif cmd in ('q', 'quit'):
                self.equipment_flag = False  # 退出装备模式更新标识符:
                return self.telnet_client.read_until(b'User@/root>', timeout=5).decode('ascii')
            else:
                pass
            cmd_result = self.telnet_client.read_until(b'equipment>', timeout=5).decode('ascii')
        else:
            # 正常模式下命令获取返回结果
            cmd_result = self.telnet_client.read_until(b'User@/root>', timeout=5).decode('ascii')
        return cmd_result

    def enter_equipment(self):
        """进入装备模式"""
        return self.execute_cmd('_hide box')

    def quit_equipment(self):
        """退出装备模式"""
        return self.execute_cmd('quit')

    def display_version(self):
        """
        查看IPC版本信息
        """
        if self.equipment_flag:
            command = 'display version all board'
        else:
            command = 'update -v'
        return self.execute_cmd(command)

    def close_fac_mode(self):
        """关闭工厂模式"""
        return self.execute_cmd('factorymode off')

    def open_fac_mode(self):
        """打开工厂模式"""
        return self.execute_cmd('factorymode on')

    def clear_information(self):
        """清除配置"""
        if self.equipment_flag:
            result = 'clear information'
        else:
            result = 'cleancfg'
        self.execute_cmd(result)

    def show_date(self):
        """查看时间"""
        return self.execute_cmd('date')

    def manuinfo_erase(self):
        """清除电子标签"""
        if self.equipment_flag:
            cmd = 'clear manuinfo'
        else:
            cmd = 'manuinfotool erase'
        return self.execute_cmd(cmd)

    def display_manuinfo(self):
        """查看电子标签"""
        if self.equipment_flag:
            cmd = 'display manuinfo'
        else:
            cmd = 'manuinfotool'
        return self.execute_cmd(cmd)

    def display_conf(self):
        """查看IPC设备的网络配置信息"""
        return self.execute_cmd('ifconfig')

    def ware_state(self):
        """查看软件启动状态"""
        ware_result = self.execute_cmd('catmwarestate')
        if 'state: [1]' in ware_result:
            ware_status = True
        elif 'state: [0]':
            ware_status = False
        return ware_status

    def reboot(self):
        """设备重启"""
        result = self.execute_cmd('reboot')
        print(result)
        return result

    def quit(self):
        """退出设备"""
        try:
            self.execute_cmd('exit')
        except Exception as e:
            logging.error(e)

    manuinfo = property(display_manuinfo)
    date = property(show_date)  # 时间信息
    ipconfig = property(display_conf)  # 网络配置信息
    ware_state = property(ware_state)  # 软件启动状态
    version = property(display_version)  # IPC软件版本信息


def ipc_telnet_test():
    """IPC telnet客户端测试"""
    dev_ip = '192.168.0.13'
    ipc_client = IPCTelnet(dev_ip)

    tel_status = ipc_client.check_telnet(dev_ip)
    if tel_status:
        # 登录ipc客户端
        status = ipc_client.login()
        if status:
            print(ipc_client.manuinfo)
            print(ipc_client.version)
            print(ipc_client.date)
            print(ipc_client.ware_state)
            print(ipc_client.ipconfig)

            print(ipc_client.open_fac_mode())
            print(ipc_client.telnet_client.interact())
            print(ipc_client.enter_equipment())
            print(ipc_client.manuinfo)
            print(ipc_client.telnet_client.get_socket())
        else:
            print("login %s" % status)


def iter_out(iter_obj, row_num=5, left_just=18)-> (iter, int):
    """
    指定格式迭代输出
    :param iter_obj: 待输出的可迭代对象
    :param row_num: 默认一行输出5个
    :param left_just: 左对齐的宽度默认18
    """
    for index in range(len(iter_obj)):
        print(iter_obj[index].ljust(left_just), end='')
        if (index+1) % row_num == 0:
            print()
    print('\n')


def main():
    ipc_telnet_test()


if __name__ == '__main__':
    main()