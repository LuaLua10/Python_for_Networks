import getpass, time
import paramiko

devices = {'IOS_R1': {'ip': '192.168.4.51'},
           'IOS_R2': {'ip': '192.168.4.52'}}

commands = ['show version\n', 'show run\n']

username = input('Username: ')
password = getpass.getpass('Password: ')

max_buffer = 65535

def clear_buffer(connection):
    """Функция для очистки буфера, который не нужно сохронять или выводить"""
    if connection.recv_ready():
        return connection.recv(max_buffer)

# Start the loop for devices
for device in devices.keys():
    outputFileName = f'{device}_output.txt'
    connection = paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connection.connect(devices[device]['ip'], username=username, password=password, look_for_keys=False, allow_agent=False)
    new_connection = connection.invoke_shell()
    output = clear_buffer(new_connection)
    time.sleep(5) # Делаем паузу, чтобы дать время оборудованию для вывода
    new_connection.send("terminal length 0\n")
    output = clear_buffer(new_connection)
    with open(outputFileName, 'wb') as f:
        for command in commands:
            new_connection.send(command)
            time.sleep(5)
            output = new_connection.recv(max_buffer)
            print(output)
            f.write(output)

    new_connection.close()