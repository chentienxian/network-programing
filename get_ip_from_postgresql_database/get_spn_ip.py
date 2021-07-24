# encoding: utf-8
# 运行环境： Windows, python v2.7.5

import os,sys,re
import psycopg2
import platform

PG_CONF = {
    'host': '172.29.xx.xx',
    'port': 4001,
    'database': 'db_umebn_xxxxxxxxxxxx',
    'user': 'postgres',
    'password': 'xxxxxxx'
}

sys_type = platform.system()
if sys_type == "Windows":
    file_path = os.path.split(os.path.realpath(sys.argv[0]))[0] + "\\spn_ip.txt"
elif sys_type == "Linux":
    file_path = os.path.split(os.path.realpath(sys.argv[0]))[0] + "//spn_ip.txt"

f = open(file_path, "w+")

pg_conn = psycopg2.connect(**PG_CONF)
pg_cur = pg_conn.cursor()

sql = "select userlabel, netaddress, productname from public.me"
pg_cur.execute(sql)
rows = pg_cur.fetchall()
print "total ips: ", len(rows)

# product = ["ZXCTN 6700-24", "ZXCTN 6700-32", "ZXCTN 6180H"]   # 输出全部设备ip
product = ["ZXCTN 6180H"]    # 只输出6180h的ip
i = 0
re_ip = re.compile(r"(\d*(\.\d*){3})")
for row in rows:
    if row[2] in product:
        ip = re_ip.search(row[1]).group(0)
        f.write(ip + "\n")
        i += 1
f.close()
print "total found ips: ", i