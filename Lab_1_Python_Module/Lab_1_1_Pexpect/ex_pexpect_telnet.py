import pexpect

devices = {'IOS_R1': {'prompt': 'IOS_R1>', 'ip': '192.168.4.51'},
           'IOS_R2': {'prompt': 'IOS_R2>', 'ip': '192.168.4.52'}}

username = 'cisco'
password = 'cisco'

for device in devices.keys():
    device_prompt = devices[device]['prompt']
    child = pexpect.spawn('telnet ' + devices[device]['ip'])
    child.logfile = open(f'debug_{device}.log', 'wb') # Режим логирования
    try:
        child.expect('[Uu]sername:', timeout=5)
    except pexpect.exceptions.TIMEOUT as error:
        pass
    else:
        child.sendline(username)
    child.expect('[Pp]assword:')
    child.sendline(password)
    child.expect(device_prompt)
    child.sendline('show version | i V')
    child.expect(device_prompt)
    print(child.before)
    #print(child) - подробный режим сессии
    #child.interact() - дает возможность перейти в интеракутивный режим управления
    child.sendline('exit')
