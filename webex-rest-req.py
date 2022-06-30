import requests
import json

base_url = 'https://webexapis.com/v1/'
access_token = 'MjA0YWIwMWQtZGJiZC00MzQ4LTkyYTEtY2RhNGM3YmJmMTQzZTg1OGQzYzYtZGRk_P0A1_af949325-f1e2-44dc-a297-78a9bdf6f617'

def check_access_token():
    url = base_url + 'people/me'

    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    res = requests.get(url, headers=headers)
    print(json.dumps(res.json(), indent=4))

if __name__ == "__main__":
    while True:
        print('Menu')
        print('1. Check Access Token')
        print('2. List Peoples - by e-mail')
        print('3. List Rooms')
        print('4. Create Rooms')
        print('5. Add Member in Room')
        print('0. Exit')

        pilihan = int(input('Pilih Menu [0-5]: '))

        match pilihan:
            case 1:
                check_access_token()
            # case 2:
            #     mail = input('email: ')
            #     list_people(mail)
            # case 3:
            #     max = input('batas max: ')
            #     list_rooms(max)
            # case 4:
            #     title = input('Nama Room: ')
            #     create_rooms(title)
            # case 5:
            #     room_id = input('ID Room: ')
            #     person_mail = input('Email Person: ')
            #     add_membership(room_id, person_mail)
            case 0:
                break
        print('\n')