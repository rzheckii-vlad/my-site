from typing import Text
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
import pymongo

'''
Картинки сохраняются в папку под Id лота

'''

headers = {

    'accept': '*/*',
    'Cookie': '_ga=GA1.2.1665625589.1636356877; _ym_uid=1636356877208187880; _ym_d=1636356877; tracking_data=source%3DReferral%26keyword%3D%26referrer%3Dhttps%253A%252F%252Fwww.caroutlet.eu%252F; accept_cookies=1; AUTUS=U1ROeVExUkdWMUkwVm1zeGVUQllORFZ2ZFRGbVFtaHVVM2R2TmtOS016WlBaRkI0VlRGWk5sSnNjVkZGVVdSNVNVbFVVRkZpVVVaRmRUSldTalZYWnpvNg%3D%3D; _gid=GA1.2.1072875117.1636972860; _ym_isad=1; _ym_visorc=w; PHPSESSID=95edf2220c05113631ebe3c32bbbd4e8; _lang=en',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.1.932 Yowser/2.5 Safari/537.36'
}

# Делаем запрос чтобы узнать общее колличество страниц
def get_href():
    url = 'https://www.caroutlet.eu/?page=161&sort=promoted_ending_soon&filter%5Bsearch_id%5D='

    # Делаем привязку ко времени
    # cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    
    with open('data/old_links.txt', 'r') as file:
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
        url = f'https://www.caroutlet.eu/?page={page}&sort=promoted_ending_soon&filter%5Bsearch_id%5D='
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        
        cars_list = soup.find('tbody', class_='table__body').find_all('tr', class_='table__row car-row')
        for link in cars_list:
            cars_href = link.find('a').get('href')
            link_to_car.append(cars_href)

    parametrs_list_finish = []
      
    # Собираем информацию с каждой карточки
    for url in set(link_to_car) - set(old_links):
    # for url in link_to_car:

        r = requests.get(url=url, headers=headers)

        soup = BeautifulSoup(r.text, 'lxml')

        parametrs = soup.find_all('div', class_='flex-base flex-space-between flex-align-start carlot__table-info-row-outer')
        try:
            damage_status = parametrs[0].find('span', class_='accent_warning').text.strip()
        except:
            damage_status = None
            
        if damage_status == 'Car damaged':
            first_registration = parametrs[1].find('li',class_='flex-justify-start').find('span').text.strip()
            probeg = parametrs[1].find('li', text=re.compile('Mileage')).find_next_sibling().text.strip()
            motor_type = parametrs[1].find('li', text=re.compile('Fuel type')).find_next_sibling().text.strip()
            
            country = parametrs[1].find('li', text=re.compile('Origin country')).find_next_sibling().text.strip()
            model_auto = parametrs[2].find('li', text=re.compile('Make, model')).find_next_sibling().text.strip()
            modification_auto = parametrs[2].find('li', text=re.compile('Type')).find_next_sibling().text.strip()
            power_auto = parametrs[2].find('li', text=re.compile('Engine power')).find_next_sibling().text.strip()
            cuzov_auto = parametrs[2].find('li', text=re.compile('Body type')).find_next_sibling().text.strip()
            dors_count_auto = parametrs[2].find('li', text=re.compile('Doors')).find_next_sibling().text.strip()

            try:
                color_auto = parametrs[2].find('li', text=re.compile('Colour')).find_next_sibling().text.strip()
            except:
                color_auto = None
            try:
                kpp_type = parametrs[1].find('li', text=re.compile('Transmission')).find_next_sibling().text.strip()
            except:
                kpp_type = None

            complectations = []
            complectation = parametrs[3].find_all('li')
            for i in complectation:
                i = i.text.strip()
                complectations.append(i)
            complectations_str = ','.join(complectations)
            

        else: 
            first_registration = parametrs[0].find('li',class_='flex-justify-start').find('span').text.strip()
            probeg = parametrs[0].find('li', text=re.compile('Mileage')).find_next_sibling().text.strip()
            country = parametrs[0].find('li', text=re.compile('Origin country')).find_next_sibling().text.strip()
            model_auto = parametrs[1].find('li', text=re.compile('Make, model')).find_next_sibling().text.strip()
            modification_auto = parametrs[1].find('li', text=re.compile('Type')).find_next_sibling().text.strip()
            power_auto = parametrs[1].find('li', text=re.compile('Engine power')).find_next_sibling().text.strip()
            cuzov_auto = parametrs[1].find('li', text=re.compile('Body type')).find_next_sibling().text.strip()
            try:
                color_auto = parametrs[1].find('li', text=re.compile('Colour')).find_next_sibling().text.strip()
            except:
                color_auto = None
            try:           
                kpp_type = parametrs[0].find('li', text=re.compile('Transmission')).find_next_sibling().text.strip()
            except:
                kpp_type = None
            try:           
                dors_count_auto = parametrs[1].find('li', text=re.compile('Doors')).find_next_sibling().text.strip()
            except:
                dors_count_auto = None
            try:           
                motor_type = parametrs[0].find('li', text=re.compile('Fuel type')).find_next_sibling().text.strip()
            except:
                motor_type = None

            complectations = []
            complectation = parametrs[2].find_all('li')
            for i in complectation:
                i = i.text.strip()
                complectations.append(i)
            complectations_str = ','.join(complectations)
           

        try:
            price = soup.find('div', class_='item-sidebar__group visible-when-bidding').find('span', class_='input-group__item').find('input').get('value')       
        except:
            price = None
        
       
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
                    if not os.path.exists(f'data/{url[-8:]}'):
                        os.mkdir(f'data/{url[-8:]}')
                    
                    r = requests.get(url=i)

                    count += 1
            
                    with open(f'data/{url[-8:]}/{count}.png', 'wb') as file:
                        file.write(r.content)
            # with open(f'data/{url[-8:]}/{url[-8:]}.json', 'w', encoding='utf-8') as file:
            #     json.dump(parametrs_list_finish, file, indent=4, ensure_ascii=False)
        
            # print(images_list)
        except Exception as ex:
            print(ex)  

        parametrs_list_finish.append(
            {
                'Ссылка на авто': url,
                'Текущая стоимость': price,
                'Состояние автомобиля': damage_status,
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
                'Комплектация': complectations_str,
                'колличество фото': count
    
            }
        )
                
        
        time.sleep(1)
             
        with open('data/old_links.txt', 'a', encoding='utf-8') as file:
            file.write(url)
            file.write('\n')    

        # with open(f'data/{url[-8:]}/{url[-8:]}.json', 'w', encoding='utf-8') as file:
        #     json.dump(parametrs_list_finish, file, indent=4, ensure_ascii=False)
        

    with open('data/car_info.json', 'a', encoding='utf-8') as file:
        json.dump(parametrs_list_finish, file, indent=4, ensure_ascii=False)
    
    print(f'Обработана {page}/{pages_count}')

    

def app_db(parametrs_list_finish):
    print(parametrs_list_finish)
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb')

    # Connect to our database
    db = client.testdata

    # Fetch our series collection
    call = db.users

    result = call.bulk_write(parametrs_list_finish)

    client.close()  



def main():
    start_time = time.time()
    get_href()
    finish_time = time.time() - start_time
    print(f'Worked Time: {finish_time}')

if __name__ == '__main__':
    main()