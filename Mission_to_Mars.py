from bs4 import BeautifulSoup as soup
import requests
import pymongo
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import pandas as pd
from pprint import pprint

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

url = 'https://marshemispheres.com/'
browser.visit(url)

html=browser.html
soup=soup(html, 'html.parser')

img_title_list = []

high_reso_image = soup.find_all('div', class_ = 'description')

for image in high_reso_image: 
    image_title = image.find('h3').get_text()
    img_url = image.find('a', class_ = 'itemLink product-item')['href']
    hemis_url = url + img_url
    
    
    browser.visit(hemis_url)
    html = browser.html
    soup = soup(html,'html.parser')

    img_src = soup.find('img', class_='wide-image')['src']

    highresol_imgurl = url + img_src
    

    hemisphere_image_url = [{
        'title': image_title,
        'image_url': highresol_imgurl
    }]      

    img_title_list += hemisphere_image_url


for high_res_image in img_title_list:
    
    print(high_res_image['image_url'], high_res_image['title']   
    )
    

browser.quit()





