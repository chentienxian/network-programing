get_server_capabilities.py
1. 根据提供的设备支持的yang模型列表：67_zxr10_yang_capabilities.txt，使用正则提取yang模型文件名称（module）和版本(revision)；
2. 根据module和revision，使用netconf客户端从设备（netconf服务端）下载设备的yang原始模型xml；
3. 将yang原始模型文件按名称和版本写入文件并保存；
4. 原始yang文件示例：原始zxr10-isis@2019-10-30.yang	


yang_strip_xml.py
1. 将上一步获取到的原始yang模型文件打开；
2. 使用正则，将原始文件中的xml元素去除，得到规范的yang模板，以便将下一步转化为tree模型便于人为阅读
3. 规范yang文件示例：规范zxr10-isis@2019-10-30.yang

yang_to_tree.py
1. 使用pyang模块，将规范yang模型转化为tree模型，并保存为tree文件后缀
2. tree模型文件示例：zxr10-isis@2019-10-30.yang.tree