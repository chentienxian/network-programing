# encoding: utf-8
# 运行环境：Linux, python v2.7.5, pyang

import subprocess,os,sys

file_list = os.listdir("./yang")

for each_file in file_list:
    cli = r'pyang -f tree ./yang/%s > ./yang_tree/%s 2>&1'% (each_file, each_file+".tree")
    # print cli
    subprocess.call(cli, shell=True)

