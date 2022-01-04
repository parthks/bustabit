from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import json
import time

historic_data ={}

# 50, 51, 53, 55, 57, 59, 61, 65, 68, 70, 72, 75, 78, 80, 83, 86, 89
# 0, 1, 3, 5, 7, 9, 11, 15, 18, 20, 22, 25, 28, 30, 33, 36, 39
f = open('historic_game_data','r')
historic_data = json.load(f)
f.close()

driver = webdriver.Chrome('/usr/local/bin/chromedriver')
num = 607523

input()
#zH64g9jbMy, macotshi

while num > 507561:

    driver.get('https://www.bustabit.com/game/'+str(num))
    time.sleep(2)
    try:
        multiplier = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div[2]/div/div[1]/h5[1]/span[2]').text
    except Exception as e:
        time.sleep(3)
        continue
    
    multiplier = (multiplier[:-1])
    print(' ',num, '=>', multiplier, end='\r')

    try:
        multiplier = float(multiplier)
    except Exception as e:
        print('Unable to convert', multiplier)
        time.sleep(3)
        continue


    historic_data[num] = multiplier
    num -= 1
    f = open('historic_game_data','w')
    json.dump(historic_data, f)
    f.close()