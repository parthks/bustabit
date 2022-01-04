from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys



from pyvirtualdisplay import Display

import time
import threading


# COMMENT THESE 2 LINES IF RUNNING LOCALLY!
display = Display(visible=0, size=(1440, 800))
display.start()


# chromdriver_path = "./chromedriver"


simulation_mode = True
simulated_balance = 1000




chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--user-data-dir=chrome-data")
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.bustabit.com/play')  # Already authenticated


time.sleep(5)










# check if logged in
try:
    right_nav_menu = driver.find_element_by_class_name("navbar-right")
    logout_button = right_nav_menu.find_elements_by_css_selector("*")[-2]
    assert(logout_button.get_attribute("href") == "https://www.bustabit.com/logout")
except Exception as e:
    print("NOT LOGGED IN")
    raise e



# Click AUTO Betting Tab
driver.find_element_by_class_name("bet-control-tabs").find_elements_by_css_selector("*")[2].click()


# Find Bet File named TEST
assert(driver.find_element_by_class_name("list-group").find_elements_by_class_name("list-group-item")[-1].text == "TEST")


# Start betting algorithm
driver.find_element_by_class_name("list-group").find_elements_by_class_name("list-group-item")[-1].find_element_by_class_name("fa-play").click()


if (simulation_mode):
    driver.find_element_by_class_name("simCheckbox").click()
    simulatedBalanceInput = driver.find_element_by_class_name("simulatedBalance").find_element_by_tag_name("input")
    value = simulatedBalanceInput.get_attribute('value')
    while (value != '0'):
        simulatedBalanceInput.send_keys(Keys.BACK_SPACE)
        value = simulatedBalanceInput.get_attribute('value')

    simulatedBalanceInput.send_keys(Keys.BACK_SPACE)
    simulatedBalanceInput.send_keys(str(simulated_balance))



# Start script
driver.find_element_by_class_name("btn-success").click()

time.sleep(10)

driver.save_screenshot("screenshots/starting.png")

print("READY")

while True:
        command = input("Enter a command: ")
        
        if (command == "screenshot"):
            driver.save_screenshot("screenshots/"+str(time.time())+".png")
            print("Took a screenshot!")
        else:
            print("Unrecognized command. Commands available - screenshot")



# driver.quit()






