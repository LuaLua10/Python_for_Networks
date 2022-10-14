#!/usr/bin/python2

from __future__ import print_function
from jsonrpclib import Server
import ssl

ssl.create_default_https_context = ssl._create_unverified_context()

switch = Server("https://admin:arista@192.168.4.45/command-api")

response = switch.runCmds( 1, ["show version"] )
print('Serial Number: ' + response[0]['serialNumber'])