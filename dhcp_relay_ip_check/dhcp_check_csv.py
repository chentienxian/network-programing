# coding: utf-8
# 运行环境: python v2.7.5
# 需要附件：ip_all.txt
# 运行结果：输出dhcp_result.txt, failed_ips.txt,success_ips.txt

from netconf_client.connect import connect_ssh
from netconf_client.ncclient import Manager
from xml.etree import ElementTree as ET
import threading
import datetime
import logging
import sys
import csv

LOG_FORMAT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)

ssh_failed_ips =[]
ssh_success_ips =[]

csv_f = open("dhcp_result.csv", "wb")
csv_file= csv.writer(csv_f)
header = ["host_ip", "dhcp_relay_ip", "dhcp_relay_interface", "vrf_name", "vrf_ip",
          "vrf_ip_mask", "vrf_interface"]
csv_file.writerow(header)

# r = open("dhcp_result.txt", "w+")
# r.write('运行开始时间： ' + str(datetime.datetime.now())+'\n')

lock_a = threading.Lock()

def netconf_dhcp_check(mng_ip):
    global csv_file
    global r
    global ssh_failed_ips
    global ssh_success_ips

    try:
        session = None
        session = connect_ssh(host=mng_ip, port=830, username='w', password='XXXXXXXX', timeout=2)
    except Exception:
        session = connect_ssh(host=mng_ip, port=830, username='w', password='XXXXXX', timeout=2)

    finally:
        if session is None:
            lock_a.acquire()
            ssh_failed_ips.append(mng_ip)
            logging.error("failed ssh ip: %s" % mng_ip)
            lock_a.release()
        else:
            lock_a.acquire()
            ssh_success_ips.append(mng_ip)
            logging.info("success ssh ip: %s" % mng_ip)
            lock_a.release()

    m = Manager(session)

    FILTER6 = """
    <configuration xmlns="http://www.zte.com.cn/zxr10/netconf/schema/rosng/interfaces" xmlns:interface="http://www.zte.com.cn/zxr10/netconf/schema/rosng/interfaces">
    </configuration>
    """
    FILTER8 = """
    <configuration xmlns="http://www.zte.com.cn/zxr10/netconf/schema/rosng/dhcp" xmlns:dhcp="http://www.zte.com.cn/zxr10/netconf/schema/rosng/dhcp">
    </configuration>
    """
    config6 = m.get_config(source='running', filter=(('subtree', FILTER6))).data_xml
    config8 = m.get_config(source='running', filter=(('subtree', FILTER8))).data_xml

    xmldata_interface = ET.fromstring(config6)
    xmldata_dhcp = ET.fromstring(config8)

    ns_dhcp = {'dhcp': 'http://www.zte.com.cn/zxr10/netconf/schema/rosng/dhcp'}
    ns_if = {'if': 'http://www.zte.com.cn/zxr10/netconf/schema/rosng/interfaces'}

    dhcp_ifs = xmldata_dhcp.findall(".//dhcp:dhcp/dhcp:interfaces/dhcp:interface", ns_dhcp)
    vrf_ifs = xmldata_interface.findall(".//if:vrf/..", ns_if)

    for dhcp_if in dhcp_ifs:
        relay_if = dhcp_if[0].text
        relay_ip = dhcp_if[2][0].text
        # print("host: %s, relay if: %s, relay ip: %s" % (mng_ip, relay_if, relay_ip))
        lock_a.acquire()
        # r.write("host: %s, relay if: %s, relay ip: %s\n" % (mng_ip, relay_if, relay_ip))
        csv_file.writerow((mng_ip, relay_ip, relay_if))
        lock_a.release()

    for vrf_if in vrf_ifs:
        vrf_inf = vrf_if[0].text
        vrf_ip = vrf_if.findall(".//if:address", ns_if)[1].text
        mask = vrf_if.findall(".//if:mask", ns_if)[0].text
        vrf = vrf_if.findall(".//if:ip-vrf-forwarding", ns_if)[0].text
        # print("host: %s, if: %s, ip: %s, mask: %s, vrf: %s" % (mng_ip, vrf_inf, vrf_ip, mask, vrf))
        lock_a.acquire()
        # r.write("host: %s, if: %s, ip: %s, mask: %s, vrf: %s\n" % (mng_ip, vrf_inf, vrf_ip, mask, vrf))
        csv_file.writerow((mng_ip, '', '',vrf,vrf_ip,mask,vrf_inf))
        lock_a.release()


if __name__ == '__main__':
    ips = ['129.34.16.204', '129.34.33.76', '129.34.16.108', '129.34.64.93', '129.34.24.38','129.35.24.38']
    f = open("ip_all.txt")
    threads = list()
    for ip in ips:
        t = threading.Thread(target=netconf_dhcp_check, args=(ip.strip(),))
        t.start()
        threads.append(t)
    for t in threads:
        t.join(timeout=120)
    # print("ssh failed ips: ", ssh_failed_ips)
    # print("ssh failed ips: ", ssh_success_ips)
    f.close()
    # r.write('运行结束时间： ' + str(datetime.datetime.now())+'\n')
    # r.close()
    csv_f.close()

    fail_file = open("failed_ips.txt", "w+")
    for ip in ssh_failed_ips:
        fail_file.write(ip+'\n')
        # fail_file.write("\n")
    fail_file.write('运行结束时间： '+ str(datetime.datetime.now())+'\n')
    fail_file.close()

    success_file = open("success_ips.txt", "w+")
    count=0
    for ip in ssh_success_ips:
        count += 1
        success_file.write(str(count)+'. '+ip+'\n')
        # success_file.write("\n")
    success_file.write('运行结束时间： ' + str(datetime.datetime.now())+'\n')
    success_file.close()
