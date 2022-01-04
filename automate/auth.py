from selenium import webdriver
from selenium.webdriver.chrome.options import Options



chromdriver_path = "/Users/parth/Desktop/~~/bustabit/automate/chromedriver"





# username = "thekillingmac"
# password = "xN85GniM3f"




chrome_options = Options()
chrome_options.add_argument("--user-data-dir=chrome-data")
driver = webdriver.Chrome(chromdriver_path,options=chrome_options)


chrome_options.add_argument("user-data-dir=chrome-data") 
driver.get('https://www.bustabit.com/play')


input("Enter when finished login")

driver.quit()

exit(1)