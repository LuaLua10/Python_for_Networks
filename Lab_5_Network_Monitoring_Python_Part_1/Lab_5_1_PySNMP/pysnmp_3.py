from pysnmp.entity.rfc3413.oneliner import cmdgen
import datetime

cmdGen = cmdgen.CommandGenerator()

host = '192.168.4.44'
community = 'secret'

# Hostname OID
system_name = '1.3.6.1.2.1.1.5.0'

# Interface OID
eth0_1_in_oct = '1.3.6.1.2.1.2.2.1.10.2'
eth0_1_in_uPackets = '1.3.6.1.2.1.2.2.1.11.2'
eth0_1_out_oct = '1.3.6.1.2.1.2.2.1.16.2'
eth0_1_out_uPackets = '1.3.6.1.2.1.2.2.1.17.2'


def snmp_query(host, community, oid):
    # GET SNMP
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData(community),
        cmdgen.UdpTransportTarget((host, 161)),
        oid
    )

    # Check for errors and print out results
    if errorIndication:
        print(errorIndication)
    else:
        if errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex)-1] or '?'
                )
            )
        else:
            for name, val in varBinds:
                return(str(val))

result = {}
result['Time'] = datetime.datetime.utcnow().isoformat()
result['hostname'] = snmp_query(host, community, system_name)
result['Eth0-1_In_Octet'] = snmp_query(host, community, eth0_1_in_oct)
result['Eth0-1_In_uPackets'] = snmp_query(host, community, eth0_1_in_uPackets)
result['Eth0-1_Out_Octet'] = snmp_query(host, community, eth0_1_out_oct)
result['Eth0-1_Out_uPackets'] = snmp_query(host, community, eth0_1_out_uPackets)

with open('/home/lualua/git/Python_for_Networks/Lab_5_Network_Monitoring_Python/results.txt', 'a') as f:
    f.write(str(result))
    f.write('\n')