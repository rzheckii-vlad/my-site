from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from fake_useragent import UserAgent


#  url = 'https://www.instagram.com/'
# option

# user_agent_list = [
#     'hellow_world',
#     'python_today'
#     'idi_lesom'
#]

useragent = UserAgent()

options = webdriver.ChromeOptions()
# options.add_argument('user-agent=Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-G925F Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.2 Chrome/38.0.2125.102 Mobile Safari/537.36')
# options.add_argument(f'user-agent={random.choice(user_agent_list)}')
options.add_argument(f'user-agent={useragent.random}')
driver = webdriver.Chrome(executable_path='E:\ПРОГА\python\selenium\chromedriver.exe', options=options)


try:
    driver.get(url='https://www.instagram.com/?hl=ru') 
    time.sleep(2)

    email_input = driver.find_element_by_name("username")
    email_input.clear()
    email_input.send_keys('rzheckii')
    time.sleep(1)

    password_input = driver.find_element_by_name('password')
    password_input.clear()
    password_input.send_keys('zlodey8738939qwerty')
    time.sleep(1)

    password_input.send_keys(Keys.ENTER)
    time.sleep(40)

except Exception as ex:
    print(ex)
finally:
    driver.close
    driver.quit