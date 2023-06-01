#!/usr/bin/python
import bisect
import datetime
import os
import pytz
from netaddr import *
from config import *
import sys
import re
import subprocess


def parse_timestamp(raw_str):
    tokens = raw_str.split()

    if len(tokens) == 1:
        if tokens[0].lower() == 'never':
            return 'never'

        else:
            raise Exception('Parse error in timestamp')

    elif len(tokens) == 3:
        dt_utc_0 = datetime.datetime.strptime(' '.join(tokens[1:]), '%Y/%m/%d %H:%M:%S')
        local_tz = pytz.timezone('Europe/Moscow')
        local_dt = dt_utc_0.replace(tzinfo=pytz.utc).astimezone(local_tz)
        return datetime.datetime(local_dt.year, local_dt.month, local_dt.day, local_dt.hour, local_dt.minute,
                                 local_dt.second + (0 if local_dt.microsecond < 500000 else 1))

    else:
        raise Exception('Parse error in timestamp')


def timestamp_is_ge(t1, t2):
    if t1 == 'never':
        return True

    elif t2 == 'never':
        return False

    else:
        return t1 >= t2


def timestamp_is_lt(t1, t2):
    if t1 == 'never':
        return False

    elif t2 == 'never':
        return t1 != 'never'

    else:
        return t1 < t2


def timestamp_is_between(t, tstart, tend):
    return timestamp_is_ge(t, tstart) and timestamp_is_lt(t, tend)


def parse_hardware(raw_str):
    tokens = raw_str.split()

    if len(tokens) == 2:
        return tokens[1]

    else:
        raise Exception('Parse error in hardware')


def strip_endquotes(raw_str):
    return raw_str.strip('"')


def identity(raw_str):
    return raw_str


def parse_binding_state(raw_str):
    tokens = raw_str.split()

    if len(tokens) == 2:
        return tokens[1]

    else:
        raise Exception('Parse error in binding state')


def parse_next_binding_state(raw_str):
    tokens = raw_str.split()

    if len(tokens) == 3:
        return tokens[2]

    else:
        raise Exception('Parse error in next binding state')


def parse_rewind_binding_state(raw_str):
    tokens = raw_str.split()

    if len(tokens) == 3:
        return tokens[2]

    else:
        raise Exception('Parse error in next binding state')


def parse_option82(raw_str):
    tokens = raw_str.split()

    if len(tokens) == 2:
        if tokens[0] == 'agent.circuit-id':
            spl_token = tokens[1].split(':')
            pars_token = int(spl_token[5], 16)
            return str(pars_token)
        elif tokens[0] == 'agent.remote-id':
            spl_token = tokens[1].split(':')
            del spl_token[0]
            del spl_token[0]
            pars_token = ':'.join(spl_token)
            return pars_token
        else:
            raise Exception('Parse error in option82')
    else:
        raise Exception('Parse error in option82')


def parse_leases_file(leases_file):
    valid_keys = {
        'starts': parse_timestamp,
        'ends': parse_timestamp,
        'tstp': parse_timestamp,
        'tsfp': parse_timestamp,
        'atsfp': parse_timestamp,
        'cltt': parse_timestamp,
        'hardware': parse_hardware,
        'binding': parse_binding_state,
        'next': parse_next_binding_state,
        'rewind': parse_rewind_binding_state,
        'uid': strip_endquotes,
        'client-hostname': strip_endquotes,
        'option agent.circuit-id': parse_option82,
        'option agent.remote-id': parse_option82,
        'option': identity,
        'set': identity,
        'on': identity,
        'abandoned': None,
        'bootp': None,
        'reserved': None,
    }

    leases_db = {}

    lease_rec = {}
    in_lease = False
    in_failover = False

    for line in leases_file:
        if line.lstrip().startswith('#'):
            continue

        tokens = line.split()

        if len(tokens) == 0:
            continue

        key = tokens[0].lower()

        if key == 'lease':
            if not in_lease:
                ip_address = tokens[1]

                lease_rec = {'ip_address': ip_address}
                in_lease = True

            else:
                raise Exception('Parse error in leases file')

        elif key == 'failover':
            in_failover = True
        elif key == '}':
            if in_lease:
                for k in valid_keys:
                    if callable(valid_keys[k]):
                        lease_rec[k] = lease_rec.get(k, '')
                    else:
                        lease_rec[k] = False

                ip_address = lease_rec['ip_address']

                if ip_address in leases_db:
                    leases_db[ip_address].insert(0, lease_rec)

                else:
                    leases_db[ip_address] = [lease_rec]

                lease_rec = {}
                in_lease = False

            elif in_failover:
                in_failover = False
                continue
            else:
                raise Exception('Parse error in leases file')

        elif key in valid_keys:
            if in_lease:
                value = line[(line.index(key) + len(key)):]
                value = value.strip().rstrip(';').rstrip()

                if callable(valid_keys[key]):
                    if value.split()[0] == 'agent.circuit-id':
                        lease_rec[f'{key} agent.circuit-id'] = valid_keys['option agent.circuit-id'](value)
                    elif value.split()[0] == 'agent.remote-id':
                        lease_rec[f'{key} agent.remote-id'] = valid_keys['option agent.remote-id'](value)
                    else:
                        lease_rec[key] = valid_keys[key](value)
                else:
                    lease_rec[key] = True

            else:
                raise Exception('Parse error in leases file')

        else:
            if in_lease:
                raise Exception('Parse error in leases file')

    if in_lease:
        raise Exception('Parse error in leases file')

    return leases_db


def round_timedelta(tdelta):
    return datetime.timedelta(tdelta.days,
                              tdelta.seconds + (0 if tdelta.microseconds < 500000 else 1))


def timestamp_now():
    n = datetime.datetime.now()
    return datetime.datetime(n.year, n.month, n.day, n.hour, n.minute,
                             n.second + (0 if n.microsecond < 500000 else 1))


def lease_is_active(lease_rec, as_of_ts):
    return timestamp_is_between(as_of_ts, lease_rec['starts'],
                                lease_rec['ends'])


def ipv4_to_int(ipv4_addr):
    parts = ipv4_addr.split('.')
    return (int(parts[0]) << 24) + (int(parts[1]) << 16) + \
           (int(parts[2]) << 8) + int(parts[3])


def select_active_leases(leases_db, as_of_ts):
    retarray = []
    sortedarray = []

    for ip_address in leases_db:
        lease_rec = leases_db[ip_address][0]

        if lease_is_active(lease_rec, as_of_ts):
            ip_as_int = ipv4_to_int(ip_address)
            insertpos = bisect.bisect(sortedarray, ip_as_int)
            sortedarray.insert(insertpos, ip_as_int)
            retarray.insert(insertpos, lease_rec)

    return retarray


def mac_vendor(current_mac):
    mac = EUI(current_mac)
    try:
        vendor = mac.oui.registration().org
        return vendor
    except NotRegisteredError:
        return 'unknown vendor'


def download_file(hostname, username, remote_path, local_path,
                  ssh_key_path=os.path.join(os.path.expanduser('~'), ".ssh", "id_rsa")):
    """
    Downloads a file from a remote server via SSH using key authentication.

    Args:
        hostname (str): The hostname or IP address of the remote server.
        username (str): The SSH username.
        remote_path (str): The path of the file on the remote server.
        local_path (str): The path to save the file locally.

    Returns:
        True if the file was downloaded successfully, False otherwise.
    """
    try:
        # Construct the SSH command
        ssh_command = [
            'scp',
            '-i', os.path.expanduser(ssh_key_path),  # SSH key path
            f'{username}@{hostname}:{remote_path}',  # remote path
            local_path  # local path
        ]

        # Run the SCP command using subprocess
        subprocess.run(ssh_command, check=True)

        print(f"File downloaded from {hostname}:{remote_path} to {local_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error downloading file: {e}")
        return False


def creating_dir(tmp_dir="./tmp"):
    if os.path.isdir(tmp_dir):
        return True
    else:
        try:
            os.mkdir(tmp_dir)
        except OSError:
            return False
        return True


def show_in_cli(lease):
    print('| ' + format(lease['ip_address'], '<15') + ' | ' + \
          format(lease['hardware'], '<17') + ' |' + \
          format(mac_vendor(lease['hardware']), '<55') + ' |' + \
          format(str(lease['starts']), '>21') + ' | ' + \
          format(str((lease['ends'] - now) if lease['ends'] != 'never' else 'never'), '>15') + ' | ' + \
          format(str(lease['option agent.circuit-id']), '<5') + ' | ' + \
          format(str(lease['option agent.remote-id']), '<18') + ' | ' + \
          lease['client-hostname'])


def main(mode, filter=None):

    global now

    if mode == 'local':
        # Открываем dhcpd.leases
        try:
            myfile = open(leases_local_path, 'r')
            leases = parse_leases_file(myfile)
            myfile.close()
        except FileNotFoundError:
            print(f'Файл {leases_local_path} не найден!')
            quit()
    elif mode == 'remote':
        # Загружаем dhcpd.leases
        if creating_dir():
            # if download_dhcpd_lesases(d_ip_add,d_pass,d_user):
            if download_file(ip_remote_dhcp_server, user_remote_dhcp_server, leases_remote_path, leases_download_path, ssh_key_path):
                # Открываем dhcpd.leases
                myfile = open('./tmp/dhcpd.leases', 'r')
                leases = parse_leases_file(myfile)
                myfile.close()
            else:
                print("Не удалось открыть dhcp.leases.")
                quit()
        else:
            print(f"Создать директорию 'tmp' не удалось.")
            quit()
    else:
        print('Введите корректный режим работы (local или remote)!')
        quit()

    # Читаем dhcpd.leases
    now = timestamp_now()
    report_dataset = select_active_leases(leases, now)

    print(
        '+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    print('| DHCPD ACTIVE LEASES REPORT')
    print(
        '+-----------------+-------------------+--------------------------------------------------------+----------------------+-----------------+-------+--------------------+---------------')
    print(
        '| IP Address      | MAC Address       | MAC Vendor                                             |Started (days,H:M:S)  | Expires (H:M:S) | Port  | Switch MAC Address | Hostname ')
    print(
        '+-----------------+-------------------+--------------------------------------------------------+----------------------+-----------------+-------+--------------------+---------------')

    cur_number_leases = 0
    for lease in report_dataset:
        if filter is not None:
            for f in filter:
                ip_result = re.match(f, lease['ip_address'])
                hw_result = re.match(f, lease['hardware'])
                sw_hw_result = re.match(f, lease['option agent.remote-id'])
                if ip_result is not None or hw_result is not None or sw_hw_result is not None:
                    cur_number_leases += 1
                    show_in_cli(lease)
        else:
            show_in_cli(lease)

    print(
        '+-----------------+-------------------+--------------------------------------------------------+----------------------+-----------------+-------+--------------------+---------------')
    if filter is not None:
        print('| Total Filtered Active Leases: ' + str(cur_number_leases))
    print('| Total Active Leases: ' + str(len(report_dataset)))
    print('| Report generated: ' + str(now))
    print(
        '+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')


if __name__ == "__main__":
    mode = sys.argv[1]
    filter = sys.argv[2:]
    if len(filter) != 0:
        main(mode, filter)
    else:
        main(mode)