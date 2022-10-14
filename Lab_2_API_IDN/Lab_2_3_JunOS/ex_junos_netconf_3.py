"""Здесь подключаемся к JunOS, загружаем его версию и устанавливаем hostname и domain name."""

from ncclient import manager
from ncclient.xml_ import new_ele, sub_ele

# Создаем обьект подключения
def connect(host, port, user, password):
    connection = manager.connect(host=host, port=port, username=user, password=password,
                                 timeout=10, device_params={'name': 'junos'},
                                 hostkey_verify=False)
    return connection

# Выполняем команду show
def show_cmds(conn, cmd):
    result = conn.command(cmd, format='text')
    return result

# Отправляем конфигурацию
def config_cmds(conn, config):
    conn.lock()
    conn.load_configuration(config=config)
    commit_config = conn.commit()
    return commit_config

if __name__ == '__main__':
    conn = connect('192.168.4.46', '830', 'netconf', 'AdminAdmin1!')
    result = show_cmds(conn, 'show version')
    print('show version: ' + str(result))
    new_config = new_ele('system')
    sub_ele(new_config, 'host-name').text = 'New_R1_JunOS'
    sub_ele(new_config, 'domain-name').text = 'New_JunOS_DOMAIN'
    result = config_cmds(conn, new_config)
    print('change id: ' + str(result))
    conn.close_session()