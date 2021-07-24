# encoding: utf-8
import subprocess, os, sys, fileinput,re

file_list = os.listdir("./yang_67")
path = os.path.split(os.path.realpath(sys.argv[0]))[0]

re_xml = re.compile(r'(<\?xml.*\n<rpc.*>)module(.*\n)*(</data></rpc-reply>)')

for each_file in file_list:
    file_path = path + "\\yang_67\\" + each_file
    # print file_path
    if each_file is not "yang":   # 去掉目录
        f = open(file_path, "r+")
        text = f.read()
        # print text
        re_xml_result = re_xml.search(str(text))
        if re_xml_result is not None:
            t1= text.replace(re_xml_result.group(1), " ")
            t2 = t1.replace(re_xml_result.group(3), " ")
            # print t2
            with open(path + "\\67\\" + each_file, "w+" ) as f2:
                f2.write(t2)
                f2.close()
            print file_path + "——ok"
        else:
            print file_path+"查询为空"

