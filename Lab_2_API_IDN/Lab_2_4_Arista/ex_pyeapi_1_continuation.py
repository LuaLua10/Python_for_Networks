#!/urs/bin/python3

import ex_pyeapi_1

s1 = ex_pyeapi_1.my_switch('./.eapi.conf', 'Arista1')

print(s1.hostname) # print hostname

print(s1.running_config) #print run conf

s1.create_vlan(11, 'my_vlan_11')

s1.node.api('vlans').getall() #print all vlans