"""
Данный код отправляет запрос на версию оборудования через NXAPI.
Генерировать playload можно через NXAPI Sandbox.
"""

import requests
import json

url = 'http://192.168.4.44/ins'
switchuser = 'admin'
switchpassword = 'AdminAdmin1!'

myheaders = {'content-type':'application/json-rpc'}
payload = [
  {
    "jsonrpc": "2.0",
    "method": "cli",
    "params": {
      "cmd": "show version",
      "version": 1
    },
    "id": 1
  }
            ]
response = requests.post(url, data=json.dumps(payload), headers=myheaders, auth=(switchuser,switchpassword)).json()

#print(json.dumps(response, indent= 4))
print(response['result']['body']['nxos_ver_str'])
