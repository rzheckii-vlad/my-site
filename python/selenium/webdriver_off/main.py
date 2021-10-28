from tempfile import tempdir
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from fake_useragent import UserAgent
import pickle
# from auth_date import email, passwarod




useragent = UserAgent()

options = webdriver.ChromeOptions()
# options.add_argument('user-agent=Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-G925F Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.2 Chrome/38.0.2125.102 Mobile Safari/537.36')
# options.add_argument(f'user-agent={random.choice(user_agent_list)}')
options.add_argument(f'user-agent={useragent.random}')
options.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome(executable_path='E:\ПРОГА\python\selenium\chromedriver.exe', options=options)


try:
    driver.get('https://www.instagram.com/')
    time.sleep(5)


except Exception as ex:
    print(ex)
finally:
    driver.close
    driver.quit