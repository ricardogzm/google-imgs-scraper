import re
import time
import requests
from os import mkdir
from selenium import webdriver
from urllib.parse import unquote
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.set_headless(True)

driver = webdriver.Chrome('./chromedriver.exe', options=options)
driver.get('https://www.google.com.mx/imghp')

search_box = driver.find_element_by_xpath('//input[@class="gLFyf gsfi"]')
search_box.send_keys('forest fire at day')
search_box.send_keys(Keys.ENTER)

# Scroll to the bottom of the page
last_height = driver.execute_script('return document.body.scrollHeight')
while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(1)
    new_height = driver.execute_script('return document.body.scrollHeight')

    if new_height == last_height:
        break
    last_height = new_height

url_pattern = "imgurl=(.+)&imgrefurl"
extension_pattern = "/(?:.+)\.(jpg|png|jpeg)\?*"

try:
    mkdir('./imgs')
except OSError as error:
    print('Directory already exists')

number_imgs = 300

for i in range(1, number_imgs+1):
    print(f'img_{i:03}:', end=' ')

    try:
        driver.find_element_by_xpath(f'//div[@class="islrc"]/div[{i}]/a[1]').click()
    except Exception as e:
        print('Element by xpath not found')
        continue

    href = driver.find_element_by_xpath(f'//div[@class="islrc"]/div[{i}]/a[1]').get_attribute('href')
    encoded_url = re.search(url_pattern, href, re.IGNORECASE).group(1)
    decoded_url = unquote(encoded_url)

    print(f'from "{decoded_url}"')

    try:
        file_extension = re.search(extension_pattern, decoded_url).group(1)
    except:
        file_extension = 'jpg'


    try:
        res = requests.get(decoded_url, timeout=1).content
    except requests.exceptions.Timeout:
        print('Request timed out')
        continue

    with open(f'./imgs/{i:03}.{file_extension}', 'wb') as handler:
        print('Image saved')
        handler.write(res)

