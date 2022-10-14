"""
Меняем hostname и domain-name через PyEZ.
"""

import sys

from jnpr.junos import Device
from jnpr.junos.utils.config import Config

dev = Device(host='192.168.4.46', user='netconf', password='AdminAdmin1!')

try:
    dev.open()
except Exception as error:
    print(error)
    sys.exit(1)

config_change = """
<system>
    <host-name>R1_JunOS</host-name>
    <domain-name>Juniper_DOMAIN</domain-name>
</system>
"""

cu = Config(dev)
cu.lock()
cu.load(config_change)
cu.commit()
cu.unlock()

dev.close()