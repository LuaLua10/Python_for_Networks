# HTTP Service Python
* ex_flask_1.py - шаблон для проектирования
* ex_flask_2.py - маршрутизация URL
* ex_flask_3.py - URL-переменные
* ex_flask_4.py - генерация URL
* ex_flask_5.py - возвращение результата с помощью jsonfy
* ex_flask_db_1.py - создаем сетевую базу данных
* ex_flask_6.py - API для работы с устройствами
    * Создание узла: 
      >curl -X POST http://127.0.0.1:5000/devices/ -H 'Content-Type: application/json' -d '{"hostname":"SW_AG_5","loopback":"192.168.0.5","mgmt_ip":"172.16.0.5","role":"aggregate","vendor":"Dlink","os":"4.0"}'
    * Получение списка узлов:
      >curl -X GET http://127.0.0.1:5000/devices/
    * Получение данных об узле:
      >curl -X GET http://127.0.0.1:5000/devices/5
    * Изменение узла (OS):
      >curl -X PUT http://127.0.0.1:5000/devices/5 -H 'Content-Type: application/json' -d '{"hostname":"SW_AG_5","loopback":"192.168.0.5","mgmt_ip":"172.16.0.5","role":"aggregate","vendor":"Dlink","os":"5.0"}'
    * Запрос версии узла (pexpect):
      >curl -X GET http://127.0.0.1:5000/devices/5/version
* ex_flask_7.py - API, асинхронные операции
    * Запрос URL для доступа к версии (URL в заголовке Location):
      > curl -I -X GET http://127.0.0.1:5000/devices/5/version

      > HTTP/1.1 202 ACCEPTED\
        Server: Werkzeug/2.2.2 Python/3.11.0\
        Date: Tue, 20 Dec 2022 12:35:10 GMT\
        Content-Type: application/json\
        Content-Length: 3\
        Location: /status/0cadafb7ba1a44b4b81058f3376e34d7\
        Connection: close
    * Запрос версии коммутатора, посредством сгенерированного URL:
      > curl -X GET http://127.0.0.1:5000/status/0cadafb7ba1a44b4b81058f3376e34d7
* ex_flask_7.py - API, авторизация
    * Создание пользователя (в cli):
      > from ex_flask_7 import db, User\
      db.create_all()\
      u = User(usernamee='alex')\
      u.set_password('pass')\
      db.session.add(u)\
      db.session.commit()\
      exit()
    * Получение списка узлов с авторизацией:
      > curl --user alex:pass -I -X GET http://127.0.0.1:5000/devices/5/version
* test-app - запуск API в контейнере.