#!/usr/bin/python
import bisect
import datetime
import paramiko
from getpass import getpass
import os
import pytz

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

def download_dhcpd_lesases(d_ip_add,d_pass,d_user='root'):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(d_ip_add, username=d_user, password=d_pass)
        sftp = ssh.open_sftp()
        remotepath = '/var/lib/dhcp/dhcpd.leases'
        localpath = './tmp/dhcpd.leases'
        sftp.get(remotepath, localpath)
        sftp.close()
        ssh.close()
        return True
    except paramiko.ssh_exception.AuthenticationException as error:
        print(f'Не удается подключится к DHCP серверу ({error}).')
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

##############################################################################

d_user = 'root'
d_pass = getpass("Domain password: ")
d_ip_add = '192.168.5.10'

# Загружаем dhcpd.leases
if creating_dir():
    if download_dhcpd_lesases(d_ip_add,d_pass,d_user):
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

# Читаем dhcpd.leases
now = timestamp_now()
report_dataset = select_active_leases(leases, now)

print('+---------------------------------------------------------------------------------------------------------------------------')
print('| DHCPD ACTIVE LEASES REPORT')
print('+-----------------+-------------------+----------------------+-----------------+-------+--------------------+---------------')
print('| IP Address      | MAC Address       | Started (days,H:M:S) | Expires (H:M:S) | Ports | Switch MAC Address | Hostname ')
print('+-----------------+-------------------+----------------------+-----------------+-------+--------------------+---------------')

for lease in report_dataset:
    print('| ' + format(lease['ip_address'], '<15') + ' | ' + \
          format(lease['hardware'], '<17') + ' |' + \
          format(str(lease['starts']), '>21') + ' | ' + \
          format(str((lease['ends'] - now) if lease['ends'] != 'never' else 'never'), '>15') + ' | ' + \
          format(str(lease['option agent.circuit-id']), '<5') + ' | ' + \
          format(str(lease['option agent.remote-id']), '<18') + ' | ' + \
          lease['client-hostname'])
print('+-----------------+-------------------+----------------------+-----------------+-------+--------------------+---------------')
print('| Total Active Leases: ' + str(len(report_dataset)))
print('| Report generated: ' + str(now))
print('+---------------------------------------------------------------------------------------------------------------------------')