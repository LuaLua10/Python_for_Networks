#!/usr/bin/python3

import vymgmt

vyos = vymgmt.Router('192.168.4.53', 'vyos', password='vyos', port=22)
vyos.login()
vyos.configure()
vyos.set("system host-name MyVyOS")
vyos.commit()
vyos.save()
vyos.exit()
vyos.logout()