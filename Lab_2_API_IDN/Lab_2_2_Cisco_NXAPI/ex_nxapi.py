"""
Данный запрос получит в ответ информацию о поддерживаемых протоколах.
Пример вывода:

urn:ietf:params:xml:ns:netconf:base:1.0
urn:ietf:params:netconf:base:1.0
urn:ietf:params:netconf:capability:validate:1.0
urn:ietf:params:netconf:capability:writable-running:1.0
urn:ietf:params:netconf:capability:url:1.0?scheme=file
urn:ietf:params:netconf:capability:rollback-on-error:1.0
urn:ietf:params:netconf:capability:candidate:1.0
urn:ietf:params:netconf:capability:confirmed-commit:1.0

"""

from ncclient import manager

conn = manager.connect(
    host='192.168.4.56',
    port=22,
    username='admin',
    password='14881488',
    hostkey_verify=False,
    device_params={'name': 'iosxe'},
    look_for_keys=False
    )

for value in conn.server_capabilities:
    print(value)

conn.close_session()
