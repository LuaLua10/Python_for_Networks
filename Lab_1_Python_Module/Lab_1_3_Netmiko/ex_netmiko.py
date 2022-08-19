import netmiko, getpass

username = input("Username: ")
password = getpass.getpass("Password: ")

devices = {"IOS_R1": {"device_type": "cisco_ios", "host": "192.168.4.51", "username": username,
                      "password": password},
           "IOS_R2": {"device_type": "cisco_ios", "host": "192.168.4.52", "username": username,
                      "password": password}
           }

command = "show ip int brief"

for device in devices.keys():
    with netmiko.ConnectHandler(**devices[device]) as net_connect:
        output = net_connect.send_command(command)

    print()
    print(output)
    print()