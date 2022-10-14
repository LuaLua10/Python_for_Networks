#!/usr/bin/env python3

import requests
import json
from ansible.module_utils.basic import AnsibleModule

def main():
    module = AnsibleModule(
        argument_spec=dict(
            host = dict(requests=True),
            username = dict(requests=True),
            password = dict(requests=True)
        )
    )

    device = module.params.get('host')
    username = module.params.get('username')
    password = module.params.get('password')

    url='http://' + device + '/ins'
    switchuser=username
    switchpassword=password

    myheaders={'content-type':'application/json-rpc'}

    payload=[
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

    response = requests.post(url, data=json.dumps(payload), headers=myheaders, auth=(switchuser, switchpassword)).json()

    version = response['result']['body']['nxos_ver_str']
    data = json.dumps({"version": version})
    module.exit_json(changed=False, msg=str(data))

if __name__ == '__main__':
    main()
