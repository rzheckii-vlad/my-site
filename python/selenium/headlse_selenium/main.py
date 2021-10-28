from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from fake_useragent import UserAgent
from auth import username, password

useragent = UserAgent()

options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={useragent.random}')


driver = webdriver.Chrome(executable_path='E:\ПРОГА\python\selenium\chromedriver.exe', options=options)


try:

    driver.get(url='vk.com') 
    time.sleep(5)

    email_input = driver.find_element_by_name("email")
    email_input.clear()
    email_input.send_keys(username)
    time.sleep(1)

    password_input = driver.find_element_by_name('pass')
    password_input.clear()
    password_input.send_keys(password)
    time.sleep(1)

    password_input.send_keys(Keys.ENTER)
    time.sleep(10)
    


except Exception as ex:
    print(ex)
finally:
    driver.close
    driver.quit