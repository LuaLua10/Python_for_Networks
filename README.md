# DHCPD Active Leases Report
This script generates a report of active leases in a DHCP server. It parses the dhcpd.leases file and displays relevant information about each active lease.

## Prerequisites
- Python 3.x
- The following Python packages: netaddr, pytz

## Installation
- Clone the repository or download the script file.

- Install the required Python packages by running the following command:

```
pip install -r requirements.txt
```

## Usage

  ```
  python script.py <mode> [<filter>...]
  ```

- "mode": Specify the mode of operation. It can be either local or remote.
- "filter" (optional): Specify one or more filters to narrow down the report. Filters can be regular expressions that match IP addresses, MAC addresses, or switch MAC addresses.

## Example Usage
- To generate a report of all active leases from a local dhcpd.leases file:
    ```
    python script.py local
    ```
- To generate a report of active leases from a remote DHCP server:
    ```
    python script.py remote
    ```
- To generate a report of active leases and filter the results based on specific IP addresses, MAC addresses, or switch MAC addresses:'
    ```
    python script.py local "^192\.168\.1\..*" "00:11:22:33:44:55" "^sw-[0-9]{4}$"
    ```

## Configuration
Before running the script, make sure to configure the following variables in the config.py file:

- leases_local_path: The local path to the dhcpd.leases file.
- user_remote_dhcp_server: The remote user for ssh connect. 
- ip_remote_dhcp_server: The remote IP address for ssh connect.
- leases_remote_path: The remote path to the dhcpd.leases file.
- leases_download_path: The local path to the download dir (./tmp).

## Output
The script will display a table with the following columns:

- IP Address: The leased IP address.
- MAC Address: The MAC address of the device.
- MAC Vendor: The vendor of the MAC address.
- Started: The start time of the lease in days, hours, minutes, and seconds.
- Expires: The remaining time until the lease expires in hours, minutes, and seconds.
- Port: The port associated with the lease (if available).
- Switch MAC Address: The MAC address of the associated switch (if available).
- Hostname: The hostname of the device (if available).
- The table will also include a summary of the total number of active leases and the report generation timestamp.

## Note
- The script requires the dhcpd.leases file to be present either locally or on a remote server, depending on the specified mode.


# DHCP Lease Removal Script
This script allows you to remove a DHCP lease for a specific IP address from the DHCP server. It automates the process of locating and deleting the lease block in the dhcpd.leases file.

## Prerequisites
- Python 3.6 or above
- DHCP server with the dhcpd.leases file accessible

## Installation
- Clone the repository or download the script file.

- Install the required Python packages by running the following command:

  ```
  pip install -r requirements.txt
  ```

## Usage
1. Open a terminal or command prompt.

2. Navigate to the directory where the script is located.

3. Run the script with the following command, providing the IP address as an argument:

  ```
  python dhcp_lease_removal.py <IP_ADDRESS>
  ```

Replace <IP_ADDRESS> with the IP address for which you want to remove the DHCP lease.

4. Follow the on-screen instructions to confirm the deletion of the DHCP lease.

5. The script will create a backup of the dhcpd.leases file, remove the lease block for the specified IP address, and update the dhcpd.leases file.

6. Once the lease has been successfully removed, the DHCP service will be restarted automatically.

## Configuration
Before running the script, make sure to configure the following variables in the config.py file:

- dhcp_service_name: The name of the DHCP service on your system.
- leases_local_path: The local path to the dhcpd.leases file.
- leases_backup_path: The path to store the backup copy of the dhcpd.leases file.

## Notes
- This script assumes that you have the necessary permissions to stop/start the DHCP service and modify the dhcpd.leases file.
- Use this script with caution, as removing a DHCP lease can affect network connectivity for the associated IP address.

## License
This project is licensed under the MIT License.

## Contact
For any questions or feedback, please feel free to contact me.