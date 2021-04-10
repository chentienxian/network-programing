# coding:utf-8

import os
import sys
import re
import openpyxl
import pprint
import pathlib

current_dir = os.path.split(os.path.realpath(sys.argv[0]))
log_dir = pathlib.Path(current_dir[0]) / "logs"
# log_dir = current_dir[0] + r"/logs"
# print os.listdir(log_dir)

log_path = {}
i = 0
for each_file in os.listdir(log_dir):
    log_path[i] = log_dir / each_file
    # print(log_path[i])
    i += 1

host_ip_list = []
whole_log_flie_str = str()

ip_address_pattern = r'(129.34.\d+\.\d+)'
session_begin = str(r"Session\sconnecting\son\s")
session_end = str(r"Session\sClosed\son\s")

for each_file in log_path.values():
    if os.path.isfile(each_file) is True:
        log_file = open(each_file, "r")
        log_lines = log_file.readlines()
        whole_log_flie_str += str(log_lines)


re_ip = re.compile(ip_address_pattern)
match_ip = re_ip.findall(str(whole_log_flie_str))

if len(match_ip) != 0:
    for each_ip in match_ip:
        host_ip_list.append(each_ip)
host_ip_list = list(set(host_ip_list))    #ip去重


raw_host_log = {}
for each_host in host_ip_list:
    re_pattern = session_begin + each_host + r'[^\d].*?' + session_end + each_host
    # print (re_pattern)
    re_host_log = re.compile(re_pattern, re.S)
    host_log = re_host_log.findall(whole_log_flie_str)

    raw_host_log.setdefault(each_host, 0)
    raw_host_log[each_host] = str(host_log)

# pprint.pprint(raw_host_log.items())
host_isis_log = {}
isis_overload_config = ""
overload_value = ""

re_overload_pattern = r'(set-overload-bit\s*on-start-up\s*(\d*))'
re_overload = re.compile(re_overload_pattern)

for each_host in raw_host_log.keys():
    host_isis_log.setdefault(each_host, [isis_overload_config,overload_value] )
    host_log = raw_host_log[each_host]
    isis_config = re_overload.findall(host_log)
    # print type(isis_config)

    if len(isis_config) >= 1:
        isis_overload_config = isis_config[0][0]
        overload_value = isis_config[0][1]
    else:
        isis_overload_config = "no overload config"
        overload_value = "null"
    host_isis_log[each_host] = [isis_overload_config, overload_value]

# pprint.pprint(host_isis_log)
print("log analyst finish, save to xlsx file begins...")

wb = openpyxl.load_workbook("isis_overload_config.xlsx")
isis_sheet = wb["isis"]
isis_sheet["A1"] = "Host IP"
isis_sheet["B1"] = "ISIS Overload Config"
isis_sheet["C1"] = "Value"

i = 2
for key in host_isis_log.keys():
    isis_sheet["A" + str(i)] = key
    isis_sheet["B" + str(i)] = host_isis_log[key][0]
    isis_sheet["C" + str(i)] = host_isis_log[key][1]
    i += 1
try:
    wb.save("isis_overload_config.xlsx")
    print("saved successfully!")
except IOError:
    print("failed to save as xlsx...")

