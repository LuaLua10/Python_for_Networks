#!/usr/bin/env python

from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result


# If you are using Nornir3, there are some changes:
# https://github.com/twin-bridges/nornir_course/blob/master/nornir3_changes.md
# Please pip install: pip install nornir_utils nornir_netmiko
# Then replace the 2 nornir.plugin imports with below:
#from nornir_utils.plugins.functions import print_result
#from nornir_netmiko import netmiko_send_command

nr = InitNornir()

result = nr.run(
    task=netmiko_send_command,
    command_string="show ip int br"
)

print_result(result)