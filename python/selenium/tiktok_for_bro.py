from selenium import webdriver
from fake_useragent import UserAgent
from multiprocessing import Pool
import random
import time


useragent = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument(f'user-agent={useragent.random}')


# urls_lise = ['https://www.tiktok.com/ru-RU/', 'https://www.instagram.com/', 'https://github.com/']

def smart_tiktok(url):
    try:
       
        driver = webdriver.Chrome(executable_path='E:\ПРОГА\python\selenium\chromedriver.exe', options=options)

        driver.get(url = url)
        time.sleep(10)
        # driver.find_element_by_class_name('lazyload-wrapper').find_element_by_class_name('item-video-container').click()
        # time.sleep(random.randrange(3, 10))

    except Exception as ex:
        print(ex)

    finally:
        driver.close
        driver.quit

if __name__ == '__main__':
    process_count = int(input('count: '))
    url_list = ['https://www.tiktok.com/ru-RU/', 'https://www.instagram.com/', 'https://github.com/']
    print(url_list)
    p = Pool(processes=process_count)
    p.map(smart_tiktok, url_list)