# !/usr/bin/env python3

import requests
import json
import xml.etree.ElementTree as ET
import unittest

# Getting NX-OSv Version with NXAPI
url ='http://192.168.4.55/ins'
switchuser ='cisco'
switchpassword ='cisco'

myheaders ={'content-type' :'application/json-rpc'}
payload =[
    {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
            "cmd": "show version",
            "version": 1.2
        },
        "id": 1
    }
]
response = requests.post(url ,data=json.dumps(payload), headers=myheaders ,auth=(switchuser ,switchpassword)).json()

nxos_version = response['result']['body']['sys_ver_str']

# Parse VIRL file, same as in example 1
with open('ex_topology_cisco.virl', 'rt') as f:
    tree = ET.parse(f)

devices = {}

for node in tree.findall('./{http://www.cisco.com/VIRL}node'):
    name = node.attrib.get('name')
    devices[name] = {}
    for attr_name, attr_value in sorted(node.attrib.items()):
        devices[name][attr_name] = attr_value

# Custom attributes
devices['iosv-1']['os'] = '15.6(3)M2'
devices['nx-osv-1']['os'] = '7.3(0)D1(1)'
devices['host1']['os'] = '16.04'
devices['host2']['os'] = '16.04'

# Unittest Test case
class TestNXOSVersion(unittest.TestCase):
    def test_version(self):
        self.assertEqual(nxos_version, devices['nx-osv-1']['os'])

if __name__ == '__main__':
    unittest.main()