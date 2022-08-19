from pexpect import pxssh
import getpass

devices = {'IOS_R1': {'prompt': 'IOS_R1#', 'ip': '192.168.4.51'},
           'IOS_R2': {'prompt': 'IOS_R2#', 'ip': '192.168.4.52'}}

commands = ['term length 0', 'show version', 'show run']

username = input('Username: ')
password = getpass.getpass('Password: ')

for device in devices.keys():
    outputFileName = f'{device}_output.txt'
    device_prompt = devices[device]['prompt']
    child = pxssh.pxssh()
    child.login(devices[device]['ip'], username.strip(), password.strip(), auto_prompt_reset=False)
    with open(outputFileName, 'wb') as f:
        for command in commands:
            child.sendline(command)
            child.expect(device_prompt)
            f.write(child.before)

    child.logout()