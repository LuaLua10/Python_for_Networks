#!/usr/bin/env python3

import requests
import json

url='http://192.168.4.47/ins'
switchuser='cisco'
switchpassword='CiscoCisco1'

myheaders={'content-type':'application/json-rpc'}
playload=[
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
response = requests.post(url, data=json.dumps(playload), headers=myheaders, auth=(switchuser,switchpassword)).json()

version = response['result']['body']['nxos_ver_str']

print(json.dumps({"version": version}))
