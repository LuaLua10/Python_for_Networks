"""
Получение версии ОС от устройства на JunOS посредством NETCONF.
"""

from ncclient import manager

conn = manager.connect(
    host='192.168.4.46',
    port='830',
    username='netconf',
    password='AdminAdmin1!',
    timeout=10,
    device_params={'name': 'junos'},
    hostkey_verify=False)

result = conn.command('show version', format='text')
print(result.xpath('output')[0].text)
conn.close_session()
