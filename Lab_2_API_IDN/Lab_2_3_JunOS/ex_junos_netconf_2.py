from ncclient import manager
from ncclient.xml_ import new_ele, sub_ele

conn = manager.connect(
                        host='192.168.4.46',
                        port='830',
                        username='netconf',
                        password='AdminAdmin1!',
                        timeout=10,
                        device_params={'name': 'junos'},
                        hostkey_verify=False
                        )

# Блокируем конфигурацию и вносим в нее изменения
conn.lock()

# Формируем конфигурацию
config = new_ele('system')
sub_ele(config, 'host-name').text = 'NewR1_JunOS'
sub_ele(config, 'domain-name').text = 'JunOS_DOMAIN'
sub_ele(config, 'time-zone').text = 'Europe/Moscow'

# Отправляем, проверяем и фиксируем конфигурацию
conn.load_configuration(config=config)
conn.validate()
commit_config = conn.commit()
print(commit_config.tostring)

# Разблокируем конфигурацию
conn.unlock()

# Закрываем сессию
conn.close_session()
