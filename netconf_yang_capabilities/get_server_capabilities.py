# encoding: utf-8
# 运行环境：Linux, python v2.7.5


from ncclient import manager
from ncclient.xml_ import to_xml
import logging
import sys ,re

LOG_FORMAT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)
m = manager.connect(host='129.34.48.188', port=830, username='who', password='Who_123#4$',
                    hostkey_verify=False, device_params={'name':'default'}, timeout=30)

f = open("67_zxr10_yang_capabilities.txt","r")
i = 1
re_module = re.compile(r"module=(\w.*)&revision=(\d{4}-\d{2}-\d{2})")
for cap in f.readlines():
    module = re_module.search(cap).group(1)
    revision = re_module.search(cap).group(2)

    schema = m.get_schema(module, revision)

    f_schema = open("/home/ubuntu/chentienx/yang_67/" + module + "@" + revision + ".yang", "a+")
    f_schema.write(str(schema))
    f_schema.close()
    i += 1

f.close()

