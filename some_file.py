import requests
import time

API_URL: str = 'https://api.telegram.org/bot'
API_CATS_URL: str = 'https://api.thecatapi.com/v1/images/search'
API_KAP_URL: str = 'https://api.capy.lol/v1/capybara?json=true'
BOT_TOKEN: str = ''
ERROR_TEXT: str = 'Здесь должна была быть картинка с котиком :('
MAX_COUNTER: int = 100

offset: int = -2
counter: int = 0
chat_id: int
cat_response: requests.Response
cat_link: str

while counter<MAX_COUNTER:

    print('attempt =', counter)  #Чтобы видеть в консоли, что код живет
    dog_api = 'https://random.dog/woof.json'
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()
    print(updates)
    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            text = result['message']['text']
            cat_response = requests.get(API_CATS_URL)
            dog_responce = requests.get(dog_api)
            kapi_responce = requests.get(API_KAP_URL)

            if kapi_responce.status_code == 200 and text == 'Капибара':
                kapi_link = kapi_responce.json()['data']['url']
                ktext = kapi_responce.json()['data']['alt']
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ktext}')

                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={kapi_link}')

            elif dog_responce.status_code == 200 and text == 'Пес':
                dog_link = dog_responce.json()['url']
                while dog_link[-1] == '4':
                    dog_responce = requests.get(dog_api)
                    dog_link = dog_responce.json()['url']
                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={dog_link}')

            elif cat_response.status_code == 200:
                cat_link = cat_response.json()[0]['url']
                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_link}')

            else:
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')

    time.sleep(1)
    counter += 1
