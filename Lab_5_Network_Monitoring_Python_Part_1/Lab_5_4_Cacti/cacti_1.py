import pexpect, sys

devices = {'iosv-1': {'prompt': 'IOS_R_1#', 'ip': '192.168.4.44'}}
username = 'admin'
password = 'ciscocisco'

for device in devices.keys():
    device_prompt = devices[device]['prompt']
    child = pexpect.spawn('telnet ' + devices[device]['ip'])
    child.expect('Username:')
    child.sendline(username)
    child.expect('Password:')
    child.sendline(password)
    child.expect(device_prompt)
    child.sendline('sh ip access-lists permit_snmp | i 192.168.4.55')
    child.expect(device_prompt)
    output = child.before
    child.sendline('exit')

sys.stdout.write(str(output).split('(')[1].split()[0].strip())