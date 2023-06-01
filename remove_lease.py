import sys
import ipaddress
import os
import subprocess
import time
import select
from config import *


# Function to manage the DHCP service start/stop
def managment_service(status):
    cur_service_name = dhcp_service_name

    if status == 'start':
        try:
            # Start the DHCP service using the 'service' command
            subprocess.check_output(['service', cur_service_name, 'start'], stderr=subprocess.STDOUT)
            print(f"Service {cur_service_name} started successfully.")
            return True
        except subprocess.CalledProcessError as error:
            print(f"Error starting service {cur_service_name}: {error.output.decode()}")
            return False
    elif status == 'stop':
        try:
            # Stop the DHCP service using the 'service' command
            subprocess.check_output(['service', cur_service_name, 'stop'], stderr=subprocess.STDOUT)
            print(f"{cur_service_name} stopped successfully.")
            return True
        except subprocess.CalledProcessError as error:
            print(f"Error stopping service {cur_service_name}: {error.output.decode()}")
            return False
    else:
        print("Invalid status.")
        return False


def user_input(pr_text):
    # Set the time limit in seconds
    time_limit = 10

    # Prompt the user for input
    print(f'{pr_text} (y/n) ({time_limit} seconds for choose)')

    # Start the timer
    start_time = time.time()

    # Initialize the status variable with a default value
    cur_status = None

    # Wait for user input within the time limit
    while time.time() - start_time < time_limit:
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            cur_status = sys.stdin.readline().strip().lower()
            break
        time.sleep(0.1)

    # If no input received within the time limit, assume 'n' (no deletion)
    if cur_status is None:
        cur_status = 'n'

    # Process the user's input
    if cur_status == 'y':
        # Delete the binding
        return True
    elif cur_status == 'n':
        # Do not delete the binding
        return False
    else:
        # Invalid input
        return False


def search_addr(ip_addr):
    # Find the index of the lease block corresponding to the provided IP address
    cr_start_index = -1
    cr_end_index = -1
    for i in range(len(lines)):
        if lines[i].startswith('lease ' + ip_addr + ' {'):
            cr_start_index = i
        elif cr_start_index != -1 and lines[i].startswith('}'):
            cr_end_index = i
            break
    return cr_start_index, cr_end_index


# Get the IP address from the command line argument
try:
    ip_address = sys.argv[1]
    ipaddress.ip_address(ip_address)
except (IndexError, ValueError):
    print("Please input a valid IP address!")
    exit()

# Read the contents of the file into a list of lines
try:
    with open(leases_local_path, 'r') as f1:
        lines = f1.readlines()
except FileNotFoundError:
    print(f"File {leases_local_path} not Found!")
    exit()

# Find the index of the lease block corresponding to the provided IP address for print
start_index, end_index = search_addr(ip_address)

# Remove the lease block from the list of lines
if start_index != -1 and end_index != -1:
    for i in lines[start_index:end_index+1]:
        print(i)
    status = user_input('Delete this binding?')
    if status:

        # Stop dhcpd.service
        if managment_service('stop'):

            # Find the index of the lease block corresponding to the provided IP address for del
            start_index, end_index = search_addr(ip_address)

            # Del lines
            del lines[start_index:end_index+1]

            # Move 'dhcpd.leases' file to 'dhcpd.leases.backup'
            try:
                file_oldname = os.path.join(f'{leases_local_path}')
                file_newname_newfile = os.path.join(f'{leases_local_path}.backup')
                os.rename(file_oldname, file_newname_newfile)
                print(f'The backup file ({leases_local_path}.backup) was created successfully.')
            except PermissionError:
                print(f'Error backup create! No permission for {leases_local_path}. Use root.')
                print(f"DHCP lease for {ip_address} has NOT been removed.")
                managment_service('start')
                exit()

            # Write the updated contents to the file
            with open(f'{leases_local_path}', 'w') as f2:
                f2.writelines(lines)
                print(f"DHCP lease for {ip_address} has been removed.")

            # Start dhcpd.service and check
            managment_service('start')

        else:
            # If service didn't start
            pass
    else:
        print(f"DHCP lease for {ip_address} has NOT been removed.")
else:
    print(f"No DHCP lease found for {ip_address}.")
