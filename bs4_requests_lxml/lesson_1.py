import requests
from bs4 import BeautifulSoup
from requests.sessions import session
import json
import csv
import time
import random


# url = 'https://health-diet.ru/table_calorie/'

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 YaBrowser/21.9.2.169 Yowser/2.5 Safari/537.36'
}


# req = requests.get(url, headers=headers)
# src = req.text

# with open('caloric_content.html', 'w', encoding='utf-8') as file:
#     file.write(src)


# with open('bs4_requests_lxml\caloric_content.html', encoding='utf-8') as file:
#     src = file.read()

# soup = BeautifulSoup(src, 'lxml')
# all_products_hrefs = soup.find_all(class_= 'mzr-tc-group-item-href')

# all_category_dict = {}
# for item in all_products_hrefs:
#     item_text = item.text
#     item_href = 'https://health-diet.ru' + item.get('href')
#     print(f'{item_text} : {item_href}')

#     all_category_dict[item_text] = item_href

# with open('all_category_dict.json', 'w', encoding='utf-8') as file:
#     json.dump(all_category_dict, file, indent=4, ensure_ascii=False)


with open('bs4_requests_lxml\\all_category_dict.json', encoding='utf-8') as file:
    all_categories = json.load(file)

iteration_count = int(len(all_categories)) - 1
count = 0
print(f'Всего итераций: {iteration_count}')
for category_name, category_href in all_categories.items():



    rep = [',', ' ', '-']
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, '_')

    req = requests.get(url=category_href, headers=headers)
    src = req.text

    with open(f'bs4_requests_lxml\data\{count}_{category_name}.html', 'w', encoding='utf-8') as file:
        file.write(src)

    with open(f'bs4_requests_lxml\data\{count}_{category_name}.html', encoding='utf-8') as file:
        file.read()
    
    soup = BeautifulSoup(src, 'lxml')

    # Проверка страницы на наличие таблицы с продуктами
    alert_block = soup.find(class_='uk-alert-danger')
    if alert_block is not None:
        continue

    # Собираем заголовки таблицы
    table_head = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
    product = table_head[0].text
    calorise = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text

    with open(f'bs4_requests_lxml\data\{count}_{category_name}.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                product,
                calorise,
                proteins,
                fats, 
                carbohydrates
            )
        )
    # Собираем данные продуктов
    product_date = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')

    product_info = []

    for item in product_date:
        product_tds = item.find_all('td')

        title = product_tds[0].find('a').text
        calorise = product_tds[1].text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        carbohydrates = product_tds[4].text
    
        product_info.append(
            {
                'title': title,
                'calories': calorise,
                'proteins': proteins,
                'fats': fats,
                'carbohydrates': carbohydrates
            }
        )

        with open(f'bs4_requests_lxml\data\{count}_{category_name}.csv', 'a', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        (
                            title,
                            calorise,
                            proteins,
                            fats, 
                            carbohydrates
                        )
                    )

    with open(f'bs4_requests_lxml\data\{count}_{category_name}.json', 'a', encoding='utf-8') as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)
        
    count += 1
    print(f' # Итерация {count}. {category_name} записаны...')
    iteration_count = iteration_count - 1

    if iteration_count == 0:
        print('Работа закончена')
        break

    print(f'Осталось итераций: {iteration_count}')
    time.sleep(random.randrange(2, 4))
    
    

