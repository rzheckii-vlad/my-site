import requests
import json
from requests.exceptions import URLRequired

from requests.models import Response

headers = {
    'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 YaBrowser/21.9.2.169 Yowser/2.5 Safari/537.36'
}

# def get_page(url):
#     s = requests.Session()
#     respons = s.get(url = url, headers = headers)

#     with open('wb.html', 'w', encoding="utf-8") as file:
#         file.write(respons.text)


def get_json(url):
    s = requests.Session()
    respons = s.get(url = url, headers = headers)

    with open('wb.json', 'w', encoding="utf-8") as file:
        json.dump(respons.json(), file, indent=4,ensure_ascii=False)

def collect_date():   #respons = ответ
    s = requests.Session()
    respons = s.get(url='https://wbxcatalog-sng.wildberries.ru/brands/a/catalog?spp=0&regions=4,30,70,68,22,66,40,82,1,80,69,48&stores=119261,122252,122256,121631,122466,122467,122495,122496,122498,122590,122591,122592,123816,123817,123818,123820,123821,123822,124096,124097,124098,121700,117393,117501,507,3158,120762,2737,1699,130744,117986&pricemarginCoeff=1&reg=0&appType=1&offlineBonus=0&onlineBonus=0&emp=0&locale=by&lang=ru&curr=rub&couponsGeo=12,7,3,21&kind=1&sort=newly&brand=61&sort=popular&page=2&xsubject=105&fsize=56158', headers=headers)
    data = respons.json()
    page = data.get('products')

    # results_data = []

    for sale in page:
            products_sale = page.get('sale')
            print(products_sale)

    # for page in range(1, page+1):
    #     url = f'https://wbxcatalog-sng.wildberries.ru/brands/a/catalog?spp=0&regions=4,30,70,68,22,66,40,82,1,80,69,48&stores=119261,122252,122256,121631,122466,122467,122495,122496,122498,122590,122591,122592,123816,123817,123818,123820,123821,123822,124096,124097,124098,121700,117393,117501,507,3158,120762,2737,1699,130744,117986&pricemarginCoeff=1&reg=0&appType=1&offlineBonus=0&onlineBonus=0&emp=0&locale=by&lang=ru&curr=rub&couponsGeo=12,7,3,21&kind=1&sort=newly&brand=61&sort=popular&page={page}&xsubject=105&fsize=56158'
    #     r = s.get(url=url, headers=headers)
    #     data = r.json()


        



def main():
    # get_page(url = 'https://by.wildberries.ru/brands/asics/mujchiny?sort=popular&page=1&bid=ddb54e39-ae65-4093-b5b3-8f62a531041f')
    # get_json(url = 'https://wbxcatalog-sng.wildberries.ru/brands/a/catalog?spp=0&regions=4,30,70,68,22,66,40,82,1,80,69,48&stores=119261,122252,122256,121631,122466,122467,122495,122496,122498,122590,122591,122592,123816,123817,123818,123820,123821,123822,124096,124097,124098,121700,117393,117501,507,3158,120762,2737,1699,130744,117986&pricemarginCoeff=1&reg=0&appType=1&offlineBonus=0&onlineBonus=0&emp=0&locale=by&lang=ru&curr=rub&couponsGeo=12,7,3,21&kind=1&sort=newly&brand=61&sort=popular&page=2&xsubject=105&fsize=56158')
    collect_date()


if __name__ == '__main__':
    main()