from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
import csv


driver = webdriver.Chrome("F:\All Downloads\chromedriver_win32\chromedriver")
driver.implicitly_wait(30)


url ="https://supermarket.souq.com/eg-ar/%D8%A3%D8%B3%D8%A7%D8%B3%D9%8A%D8%A7%D8%AA-%D8%A7%D9%84%D8%B7%D8%A8%D8%AE/c/13173"


file_csv = open('SuperMarketData.csv', 'w',encoding='utf-8-sig')
file_json = open('SuperMarketData.json','w',encoding='utf-8-sig')
    

data = {}
csv_columns = ['name','price','img']


writer = csv.DictWriter(file_csv, fieldnames=csv_columns) 
writer.writeheader()

file_json.write('[\n')

try:
    SCROLL_PAUSE_TIME = 5
    driver.get(url)

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, "html.parser")
    ancher=soup.find_all('div', class_= 'column column-block block-grid-large ')

    for c in ancher:
        name=c.find('h6', class_= 'title')
        itemPrice=c.find('span', class_= 'is block sk-clr1')
        img=c.find('img', class_= 'img-size-medium')
       
        writer.writerow({'name': name.text.strip().rstrip('\n') ,'price': itemPrice.text[0:8].rstrip('\n\t') , 'img': img.get('data-src')})
        data['name'] =name.text.strip().rstrip('\n')
        data['price'] =itemPrice.text[0:8].rstrip('\n\t')
        data['img'] =img.get('data-src')
        json_data = json.dumps(data,ensure_ascii=False )
        file_json.write(json_data)
        file_json.write(",\n")     

finally:
    driver.quit()
    file_json.write("\n]")
    file_csv.close()
    file_json.close()

