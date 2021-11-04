from selenium import webdriver
import time
import random
from fake_useragent import UserAgent


#  url = 'https://www.instagram.com/'
# option

# user_agent_list = [
#     'hellow_world',
#     'python_today'
#     'idi_lesom'
]

useragent = UserAgent()

options = webdriver.ChromeOptions()
# options.add_argument('user-agent=Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-G925F Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.2 Chrome/38.0.2125.102 Mobile Safari/537.36')
# options.add_argument(f'user-agent={random.choice(user_agent_list)}')
options.add_argument(f'user-agent={useragent.random}')
driver = webdriver.Chrome(executable_path='E:\ПРОГА\python\selenium\chromedriver.exe', options=options)


try:
    driver.get(url='http://whatsmyuseragent.org/') 
    time.sleep(5)

    # driver.get_screenshot_as_file('1.png')
    # driver.save_screenshot('2.png')
    # time.sleep(2)

except Exception as ex:
    print(ex)
finally:
    driver.close
    driver.quit

