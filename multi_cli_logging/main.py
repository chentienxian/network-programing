# coding:utf-8
# 待实现功能： 强密码错误判断

import telnetlib
from telnet_funs import TelnetFunction
import os
import sys

# 配置登录信息
_Username = 'who'
_Password = 'Who_123#4$'

# 待下发命令
_Command = (
    "show le",
)

tf = TelnetFunction()
log_file = tf.log_file_enable()       #开启log记录

current_dir = os.path.split(os.path.realpath(sys.argv[0]))
host_ip_file = current_dir[0] + "\\" + "ip2.txt"     # 需要登录的设备IP文件路径(for windows)
ip_file = open(host_ip_file, "r")

for host in ip_file.readlines():
    host = host.strip()
    try:
        telnet_session = telnetlib.Telnet(host)       #telnet连接设备
        # 开启调试，按需开启，方便判断
        # telnet_session.set_debuglevel(2)
        tf.print_and_log(log_file, '\n[*] Session connecting on ' + host + '.\n')

        tn = tf.telnet_login(telnet_session, log_file, _Username, _Password)   #telnet登录并进入配置模式
        for command in _Command:
            tn = tf.push_command(tn, log_file, command)            #逐条下发cli命令

        # 下发完毕后，关闭telnet连接
        tn.close()

        tf.print_and_log(log_file, '\n[*] Session Closed on ' + host + '.\n')
    except Exception as login_error:
        print(login_error)
        tf.print_and_log(log_file, '[*] Session Failed on ' + host + '.\n')

# 完毕后，关闭log文件写入
tf.log_close(log_file)
