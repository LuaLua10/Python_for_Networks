"""
По средствам PyEZ получаем информацию о интерфейсе.

Ключ dev.rpc.get_interface_information можно найти 3 путями:
    1. Junos XML API Operatoinal Developer Reference на сайте Juniper;
    2. С помощью CLI - show interfaces em1 | display xml rpc ;
    3. Через библиотеку PyEZ - dev1.display_xml_rpc('show interfaces em1', format='text') .
"""

import sys

from jnpr.junos import Device
import xml.etree.ElementTree as ET
import pprint

dev = Device(host='192.168.4.46', user='netconf', password='AdminAdmin1!')

try:
    dev.open()
except Exception as error:
    print(error)
    sys.exit(1)

#print(dev.display_xml_rpc('show interfaces em1', format='text'))

result = dev.rpc.get_interface_information(interface_name='em1', terse=True)
pprint.pprint(ET.tostring(result))

dev.close()