from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from imgstonote import ImgToNote

path = "/chromedriver_win32/chromedriver.exe"
service = Service(path)

def get_driver(url: str) -> webdriver.Chrome:
    # Options to make browsing easier
    options = webdriver.ChromeOptions()
    options.add_argument("disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument("disable-dev-shm-usage")
    options.add_argument("no-sandbox")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    return driver

url = "https://teams.live.com/meet/9393881799688"

driver = get_driver(url)

import time

time.sleep(40)

text = ""
xpath = '/html/body/div[1]/div[2]/div/div[1]/div/calling-screen/div/div[2]/div[2]/div[3]/calling-stage/div/calling-participant-stream/div/div[3]'
content = driver.find_element(by='xpath', value=xpath)
png = content.screenshot_as_png

