# coding:utf-8

from datetime import *
import time
import os
import sys

_SysEnableTag = '#'
_MoreTag = '--More--'
_ErrorTag = 'error'


class TelnetFunction(object):

    @staticmethod
    def log_file_enable():                       # 使能log记录
        # 配置log路径(for windows)
        _dir = os.path.split(os.path.realpath(sys.argv[0]))
        path = str(_dir[0]) + r"\logs"
        # print dir,path

        # 若logs文件夹不存在，则新建文件夹
        try:
            os.makedirs(path)
        except OSError:
            if not os.path.exists(path):
                raise

        # 构建log文件名(for windows)
        log_file = path + '\\' + datetime.now().date().isoformat() + ' ' + datetime.now().time().strftime(
            '%H-%M-%S') + '.log '
        # print log_file

        # 创建log并开启日志写入
        f_log = open(log_file, 'a+')

        return f_log

    @classmethod
    def print_and_log(cls, log_file, response):
        print(response.decode('ascii'))
        log_file.write(response.decode('ascii'))
        time.sleep(0.1)
        return None

    @staticmethod
    def log_close(log_file):
        log_file.close()
    
    @classmethod
    def push_command(cls, telnetsession, log_file, command, waiting_tag=_SysEnableTag):
        telnetsession.write("  " + command + "\n".encode())
        response = telnetsession.read_until(waiting_tag.encode(), 1)
        if waiting_tag.encode('ascii') in response:
            TelnetFunction.print_and_log(log_file, response)
        elif _MoreTag in response:
            TelnetFunction.print_and_log(log_file, response)
            TelnetFunction.print_more(telnetsession, log_file, waiting_tag)
        elif _ErrorTag in response:
            TelnetFunction.print_and_log(log_file, "Can not proceed! Error might occurred!!!")
        return telnetsession

    @classmethod
    def print_more(cls, telnetsession, log_file, waiting_tag=_SysEnableTag):
        telnetsession.write(" ".encode())
        response = telnetsession.read_until(waiting_tag.encode(), 1)
        while True:
            if waiting_tag in response:
                TelnetFunction.print_and_log(log_file, response)
                break
            elif _MoreTag in response:
                TelnetFunction.print_and_log(log_file, response)
                telnetsession.write(" ".encode())
                response = telnetsession.read_until(waiting_tag.encode(), 1)
        return None

    @staticmethod
    def telnet_login(telnetsession, log_file, username, password):
        # Telnet用户名密码登录，当出现'Username'时，输入：
        login_prompt = b'Username'
        response = telnetsession.read_until(login_prompt, 1)
        if login_prompt in response:
            TelnetFunction.print_and_log(log_file, '\n[*] Username: ' + username)
        telnetsession.write(username.encode('ascii') + b'\n')

        # 当出现'Password'时，输入：
        password_prompt = 'Password'
        response = telnetsession.read_until(password_prompt.encode('ascii'), 1)
        if password_prompt.encode('ascii') in response:
            TelnetFunction.print_and_log(log_file, '\n[*] Password: ' + password + '\n')
        telnetsession.write(password.encode('ascii') + b'\n')

        # 确认登录成功
        response = telnetsession.read_until(_SysEnableTag.encode('ascii'), 1)
        if _SysEnableTag.encode('ascii') in response:
            TelnetFunction.print_and_log(log_file, response.decode('ascii'))

        # 提权enable
        telnetsession.write(" enable\n".encode())
        response = telnetsession.read_until("Password:".encode(), 1)
        TelnetFunction.print_and_log(log_file, response.decode('ascii'))
        telnetsession.write("zxr10\n".encode())
        # 确认提权enable成功
        response = telnetsession.read_until(_SysEnableTag.encode(), 1)
        TelnetFunction.print_and_log(log_file, response.decode('ascii'))

        return telnetsession
