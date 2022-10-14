#!/usr/bin/python2

from __future__ import print_function
from jsonrpclib import Server
import ssl, pprint

ssl._create_default_https_context = ssl._create_unverified_context

def runAristaCommands(switch_object, list_of_commands):
    response = switch_object.runCmds(1, list_of_commands)
    return response

switch = Server("https://192.168.4.45/command-api")

commands = ['enable', 'configure', 'interface etchernet 1/3', 'switchport access vlan 100', 'end', 'write memory']

response = runAristaCommands(switch, commands)

pprint.pprint(response)