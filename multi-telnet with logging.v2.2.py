# coding:utf-8
# 待实现功能：多网元telnet， 强密码错误判断

import telnetlib
from datetime import *
import time
import os
import sys

### 配置登录信息
_Username = 'who'
_Password = 'Who_123#4$'

_Host = ['129.34.33.58', '129.34.33.58']

# _UsermodTag = '>'
_SysEnableTag = '#'
_MoreTag = '--More--'
_ErrorTag = 'error'

# 待下发命令
_Command = (
    "show alarm current",
    "show le",
    "segment-routing",
    "end"
)

# 配置log路径
_dir = os.path.split(os.path.realpath(sys.argv[0]))
path = str(_dir[0]) + r"\logs"
# print dir,path

# 若没有logs文件夹则创建
try:
    os.makedirs(path)
except OSError:
    if not os.path.exists(path):
        raise


# ======================函数操作定义开始===========================

# 命令下发，字符等待，打印cli, log记录
def push_command(telnetsession, command, waiting_tag=_SysEnableTag):
    telnetsession.write("  " + command + "\n".encode())
    response = telnetsession.read_until(waiting_tag.encode(), 1)
    if waiting_tag.encode('ascii') in response:
        print_cli_and_log(response)
    elif _MoreTag in response:
        print_more(telnetsession, waiting_tag)
    elif _ErrorTag in response:
        print_cli_and_log("Can not proceed! Error might occurred!!!")
    return telnetsession


def print_cli_and_log(response):
    print (response.decode('ascii'))
    f_log.write(response.decode('ascii'))
    time.sleep(0.1)
    return None


def print_more(telnetsession, waiting_tag=_SysEnableTag):
    telnetsession.write(" ".encode())
    response = telnetsession.read_until(waiting_tag.encode(), 1)
    while True:
        if waiting_tag in response:
            print_cli_and_log(response)
            break
        elif _MoreTag in response:
            print_cli_and_log(response)
            telnetsession.write(" ".encode())
            response = telnetsession.read_until(waiting_tag.encode(), 1)
    return None


def telnet_login(telnetsession):
    # Telnet用户名密码登录，当出现'Username'时，输入：
    login_prompt = b'Username'
    response = telnetsession.read_until(login_prompt, 1)
    if login_prompt in response:
        print_cli_and_log('\n[*] Username: ' + _Username)
    telnetsession.write(_Username.encode('ascii') + b'\n')

    # 当出现'Password'时，输入：
    password_prompt = 'Password'
    response = telnetsession.read_until(password_prompt.encode('ascii'), 1)
    if password_prompt.encode('ascii') in response:
        print_cli_and_log('\n[*] Password: ' + _Password + '\n')
    telnetsession.write(_Password.encode('ascii') + b'\n')

    # 确认登录成功
    response = telnetsession.read_until(_SysEnableTag.encode('ascii'), 1)
    if _SysEnableTag.encode('ascii') in response:
        print_cli_and_log(response.decode('ascii'))

    # 提权enable
    telnetsession.write(" enable\n".encode())
    response = telnetsession.read_until("Password:".encode(), 1)
    print_cli_and_log(response.decode('ascii'))
    telnetsession.write("zxr10\n".encode())
    # 确认提权enable成功
    response = telnetsession.read_until(_SysEnableTag.encode(), 1)
    print_cli_and_log(response.decode('ascii'))

    return telnetsession


# ======================函数操作定义结束===========================

# log文件名
log_file = path + '\\' + datetime.now().date().isoformat() + ' ' + datetime.now().time().strftime('%H-%M-%S') + '.log'
# print log_file

# 创建log并开启日志写入
f_log = open(log_file, 'a+')

for host in _Host:
    tn = telnetlib.Telnet(host)
    # 开启调试，按需开启，方便判断
    # telnetsession.set_debuglevel(2)

    print_cli_and_log('\n[*] Session connecting on ' + host + '.\n')

    tn = telnet_login(tn)

    for command in _Command:
        tn = push_command(tn, command)

    # 完毕后，关闭连接
    tn.close()
    print_cli_and_log('\n[*] Session Closed on ' + host + '.\n')
# 完毕后，关闭log写入
f_log.close()
