"""
Данный код служит примером работы с контроллерами Cisco ACI и APIC-EM.
Основное отличие данных контроллеров в сфере приминения:
ACI используется в дата-центрах, тогда как APIC-EM является вариантом для корпоративных сетей.
"""

import requests
import json

controller = 'URL'
username = 'cisco'
password = 'cisco'


def getTicket():
    """Получаем тикет (право доступа) от контроллера на ограниченое время"""
    url = "https://" + controller + "/api/v1/ticket"
    playload = {"username": username, "password": password}
    header = {"content-type": "application/json"}
    response = requests.post(url, data=json.dumps(playload), headers=header, verify=False)
    r_json = response.json() # Конвертируем response в json формат
    ticket = r_json["response"]["serviceTicket"] # Забираем тикет
    return ticket

def get_NetworkDevices(ticket):
    """Получаем список сетевых устройств известных контроллеру. Требуется ticket для авторизации."""
    url = "https://" + controller + "/api/v1/network-device"
    header = {"content-type": "application/json", "X-Auth-Token":ticket}
    response = requests.get(url, headers=header, verify=False)
    print("Network Devices = ")
    print(json.dumps(response.json(), indent=4, separators=(',', ': ')))
    r_json = response.json()
    for i in r_json["response"]:
        print(i["id"] + " " + i["series"])

def main():
    theTicket = getTicket() # Получаем тикет
    get_NetworkDevices(theTicket) # Получаем и выводим данные

if (__name__ == "__main__"):
    main()