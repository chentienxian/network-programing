# network-programming
工作中网元运维自动化相关脚本整理。

1. get_ip_from_postgresql_database：
获取pg数据库的特定型号的设备的全部IP，比便用于telnet/ssh登录。
   
2. multi_cli_logging：
采用telnet的方式批量下发配置
   
3. isis_config_analyze
对存量的log文件进行isis配置分析, 查找和比对缺少和不同配置项

4. port_format_convertion：
端口格式转换，将网络中不同设备，不同单板的端口和速率进行转换成标准格式：转换前示例：PXGA12T1[0-1-1] 10GE:8 ；转换后示例：xgei-1/1/0/8

5. netconf_yang_capabilities：
从netconf服务器下载支持的全部yang模型文件，并转换为tree模型

6. dhcp_relay_ip_check：
采用netconf方式多线程获取设备vrf和dhcp配置，对比和记录配置差异
