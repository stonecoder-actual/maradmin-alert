from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

url = 'https://www.marines.mil/News/Messages/Messages-Display/Article/3917376/officer-promotions-for-october-2024-and-projected-officer-promotions-for-novemb/'
driver.get(url)

pageBody = driver.find_elements(By.CLASS_NAME, 'body-text')

print(type(pageBody))


for elem in pageBody:
    if elem[0] == 'R':
        print(elem.text)




driver.quit()