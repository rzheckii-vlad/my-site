import requests
from bs4 import BeautifulSoup
import csv
import random
import time
import json
import re
import datetime
import os
from requests import exceptions

'''
Картинки сохраняются в папку под Id лота

'''

headers = {

    'accept': '*/*',
    'Cookie': '_lang=ru; _ga=GA1.2.1665625589.1636356877; _gid=GA1.2.990676637.1636356877; _ym_uid=1636356877208187880; _ym_d=1636356877; tracking_data=source%3DReferral%26keyword%3D%26referrer%3Dhttps%253A%252F%252Fwww.caroutlet.eu%252F; accept_cookies=1; _ym_isad=1; PHPSESSID=405b2744d740417372634fe973500863; _ym_visorc=w; AUTUS=U1ROeVExUkdWMUkwVm1zeGVUQllORFZ2ZFRGbVFtaHVVM2R2TmtOS016WlBaRkI0VlRGWk5sSnNjVkZGVVdSNVNVbFVVRkZpVVVaRmRUSldTalZYWnpvNg%3D%3D',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 YaBrowser/21.9.2.169 Yowser/2.5 Safari/537.36'
}

# Делаем запрос чтобы узнать общее колличество страниц
def get_href():
    url = 'https://www.caroutlet.eu/?page=161&sort=promoted_ending_soon&filter%5Bsearch_id%5D='

    # Делаем привязку ко времени
    # cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    # Открываем файл csv на запись (прописываем заголовки)
    with open('car_info.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Ссылка на авто',
                'Текущая стоимость',
                'Регистрация',
                'Пробег',
                'Тип двигателя',
                'Тип КПП',
                'Страна происхождения',
                'Марка автомобиля, модель',
                'Модификация',
                'Мощность',
                'Цвет',
                'Тип кузова',
                'Количество дверей',
                'Комплектация'
            )
        )
    with open('old_links.txt', 'r') as file:
        old_links = file.read().splitlines()

    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    # Получаем общее колличество страниц из пагинации.
    pages_count = int(soup.find('div', class_='layout-column__inner layout-column__inner_gutter-bottom-x').find_all('a')[-1].text)
    # print(pages_count)
    link_to_car = []

    # Запускаем сбор ссылок с каждый страницы и добавляем в список.
    # for page in range(1, pages_count + 1):
    for page in range(1, 2):
        url = f'https://www.caroutlet.eu/?page={page}&sort=promoted_ending_soon'
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        
        cars_list = soup.find('tbody', class_='table__body').find_all('tr', class_='table__row car-row')
        for link in cars_list:
            # cars_data = link.find_all('td')
            try:
                cars_href = link.find('a').get('href')
            except:
                print('нет ссылки')

            link_to_car.append(cars_href)

    parametrs_list_finish = []
    
    # Собираем информацию с каждой карточки
    for url in set(link_to_car) - set(old_links):
    # for url in link_to_car:

        r = requests.get(url=url, headers=headers)

        soup = BeautifulSoup(r.text, 'lxml')

        try:
            parametrs = soup.find_all('div', class_='flex-base flex-space-between flex-align-start carlot__table-info-row-outer')
            
            first_registration = parametrs[0].find('li',class_='flex-base flex-justify-start').find('span').text.strip()
            probeg = parametrs[0].find('li', text=re.compile('Пробег')).find_next_sibling().text.strip()
            motor_type = parametrs[0].find('li', text=re.compile('Тип двигателя')).find_next_sibling().text.strip()
            kpp_type = parametrs[0].find('li', text=re.compile('Тип КПП')).find_next_sibling().text.strip()
            country = parametrs[0].find('li', text=re.compile('Страна происхождения')).find_next_sibling().text.strip()
            model_auto = parametrs[1].find('li', text=re.compile('Марка автомобиля, модель')).find_next_sibling().text.strip()
            modification_auto = parametrs[1].find('li', text=re.compile('Модификация')).find_next_sibling().text.strip()
            power_auto = parametrs[1].find('li', text=re.compile('Мощность')).find_next_sibling().text.strip()
            cuzov_auto = parametrs[1].find('li', text=re.compile('Тип кузова')).find_next_sibling().text.strip()
            dors_count_auto = parametrs[1].find('li', text=re.compile('Количество дверей')).find_next_sibling().text.strip()
        
            complectations = []
            complectation = parametrs[2].find_all('li')
            for i in complectation:
                i = i.text.strip()
                complectations.append(i)
            complectations_str = ','.join(complectations)
        except Exception as ex:
            print(ex)

        try:
            color_auto = parametrs[1].find('li', text=re.compile('Цвет')).find_next_sibling().text.strip()
        except:
            color_auto = None

        try:
            price = soup.find('div', class_='item-sidebar__group visible-when-bidding').find('span', class_='input-group__item').find('input').get('value')       
        except Exception as ex:
            print(ex)

        images_list = []
        # Скачиваем изображения с карточек
        try:
            images = soup.find('div', id='gallery-images').find('div', class_='overlay-main__primary')
            all_image = images.find_all('div', class_='overlay-main__item')
            for items in all_image:
                img = items.find('img').get('src')
                images_list.append(img)

                count = 0
                
                for i in images_list:
                    if not os.path.exists(f'data\\{url[-8:]}'):
                        os.mkdir(f'data\\{url[-8:]}')
                    
                    r = requests.get(url=i)

                    count += 1
            
                    with open(f'data\\{url[-8:]}\\{count}.png', 'wb') as file:
                        file.write(r.content)

            # print(images_list)
        except Exception as ex:
            print(ex)

        
        parametrs_list_finish.append(
            {
                'Ссылка на авто': url,
                'Текущая стоимость': price,
                'Регистрация': first_registration,
                'Пробег': probeg,
                'Тип двигателя': motor_type,
                'Тип КПП': kpp_type,
                'Страна происхождения': country,
                'Марка автомобиля, модель': model_auto,
                'Модификация': modification_auto,
                'Мощность': power_auto,
                'Цвет': color_auto,
                'Тип кузова': cuzov_auto,
                'Количество дверей': dors_count_auto,
                'Комплектация': complectations_str
            }
        )
                
        # Заполняем нашу таблицу
        with open('car_info.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    url,
                    price,
                    first_registration,
                    probeg,
                    motor_type,
                    kpp_type,
                    country,
                    model_auto,
                    modification_auto,
                    power_auto,
                    color_auto,
                    cuzov_auto,
                    dors_count_auto,
                    complectations_str
                )
            )

        print(f'Обработана {page}/{pages_count}')
        time.sleep(random.randrange(1,2))

    with open('old_links.txt', 'w', encoding='utf-8') as file:
        for it in link_to_car:
            file.write(it)
            file.write('\n')

    with open('car_info.json', 'w', encoding='utf-8') as file:
        json.dump(parametrs_list_finish, file, indent=4, ensure_ascii=False)


def main():
    get_href()

if __name__ == '__main__':
    main()