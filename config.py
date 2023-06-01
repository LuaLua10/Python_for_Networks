user_remote_dhcp_server = 'root'
ip_remote_dhcp_server = '192.168.5.10'
leases_remote_path = '/var/lib/dhcp/dhcpd.leases'
leases_local_path = '/var/lib/dhcpd/dhcpd.leases'
leases_download_path = './tmp/dhcpd.leases'
leases_backup_path = '/var/lib/dhcpd/dhcpd.leases.backup'
ssh_key_path = "~/.ssh/id_rsa"
dhcp_service_name = 'dhcpd.service' #'isc-dhcp-server'