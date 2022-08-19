import netmiko, getpass

ip = input("IP address: ")
username = input("Username: ")
password = getpass.getpass("Password: ")

device = {"device_type": "dlink_ds", "host": ip, "username": username, "password": password}
command = "show ports"


with netmiko.ConnectHandler(**device) as net_connect:
    output = net_connect.send_command(command)

    print()
    print(output)
    print()