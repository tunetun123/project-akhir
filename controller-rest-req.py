import requests
import json

api_url = 'http://localhost:58000/api/v1/'
user = 'central'
pswrd = 'netcom'


def req_service_ticket(usr, pwd):

    url = api_url + 'ticket'

    headers = {
        "content-type": "application/json"
    }

    body_json = {
        "username": str(usr),
        "password": str(pwd)
    }

    resp = requests.post(url, json.dumps(body_json),
                         headers=headers, verify=False)

    print("Ticket request status : ", resp.status_code)
    response_json = resp.json()

    serviceTicket = response_json["response"]["serviceTicket"]
    print("service ticket number is : ", serviceTicket)

    return serviceTicket


def get_network_devices(ticket):
    url = api_url + 'network-device'

    headers = {
        "X-Auth-Token": str(ticket)
    }

    resp = requests.get(url, headers=headers, verify=False)

    print("Request status : ", resp.status_code)
    response_json = resp.json()

    networkDevices = response_json["response"]

    devices = len(response_json['response'])
    output = "Terdapat " + str(devices) + " network device yang terdaftar:\n"
    output += "-"*60 + "\n"
    output += "NO. | HOSTNAME | PLATFORM ID | IP ADDRESS\n"
    output += "-"*60 + "\n"

    n = 1
    for networkDevice in response_json["response"]:
        output += "" + str(n) + ". | " + networkDevice['hostname'] + " | " + \
            networkDevice['platformId'] + " | " + \
            networkDevice['managementIpAddress'] + "\n"
        n += 1

    return output


def get_hosts(ticket):
    url = api_url + 'host'

    headers = {
        'X-Auth-Token': str(ticket)
    }

    resp = requests.get(url, headers=headers, verify=False)

    print("Request status : ", resp.status_code)
    response_json = resp.json()

    print("service ticket number is : ", ticket)

    hostDevices = response_json["response"]

    devices = len(response_json['response'])
    output = "Terdapat " + str(devices) + " Host yang terdaftar:\n"
    output += "-"*60 + "\n"
    output += "NO. | HOSTNAME | HOST IP | HOST MAC | INTERFACE\n"
    output += "-"*60 + "\n"

    n = 1
    for hostDevice in hostDevices:
        output += "" + str(n) + ". | " + hostDevice['hostName'] + " | " + \
            hostDevice['hostIp'] + " | " + \
            hostDevice['hostMac'] + " | " + \
            hostDevice['connectedInterfaceName'] + "\n"
        n += 1

    return output


def send_to_webex(message):

    webex_url = "https://webexapis.com/v1/messages"
    access_token = "MjA0YWIwMWQtZGJiZC00MzQ4LTkyYTEtY2RhNGM3YmJmMTQzZTg1OGQzYzYtZGRk_P0A1_af949325-f1e2-44dc-a297-78a9bdf6f617"
    roomId = "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vMGFmMDYwMDAtZjg0NS0xMWVjLWI5MWEtMjFhYmQ1YTNmYmE0"

    headers = {
        "Authorization": "Bearer {}".format(access_token),
        "Content-Type": "application/json"
    }

    params = {
        "roomId": roomId,
        "markdown": '**Pesan diterima dari Controller :**'+'\n' + '>' + message
    }

    res = requests.post(webex_url, headers=headers, json=params)

    print("Request status : ", res.status_code)

    if res.status_code == 200:
        print("Pengiriman Pesan Berhasil")
    else:
        print("Terjadi Error, Gagal mengirim pesan.")


if __name__ == "__main__":
    username = input('Username : ')
    password = input('Password : ')
    print('\n')

    if (username == user) & (password == pswrd):
        access_ticket = req_service_ticket(username, password)
        while True:
            print('Menu')
            print('1. Get Network Devices')
            print('2. Get Hosts')
            print('0. Exit')

            pilihan = int(input('Pilih Menu [0-3]: '))

            match pilihan:
                case 1:
                    result = get_network_devices(access_ticket)
                    print(result)
                    send = input("Kirim hasil ke Webex room [y/n]: ")
                    if (send == 'y') | (send == 'Y'):
                        send_to_webex(result)
                    elif (send == 'n') | (send == 'N'):
                        pass
                    else:
                        pass
                case 2:
                    result = get_hosts(access_ticket)
                    print(result)
                    send = input("Kirim hasil ke Webex room [y/n]: ")
                    if (send == 'y') | (send == 'Y'):
                        send_to_webex(result)
                    elif (send == 'n') | (send == 'N'):
                        pass
                    else:
                        print("Wrong Input")
                        pass
                # case 3:
                case 0:
                    break

            print('\n')
    else:
        print('Wrong credentials')