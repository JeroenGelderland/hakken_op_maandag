import os
from uuid import uuid4
from flask.scaffold import F
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.common.by import By
import urllib.request
from uuid import uuid4
import base64
import csv
from threading import Thread

THREADS = 4;
PAGE_COUNT = 1200;

options = webdriver.ChromeOptions()
args = ['--headless']


# options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})

for arg in args:
    options.add_argument(arg)


data = []


def save(my_selenium_pointers, imgs):

    if(len(my_selenium_pointers)>0):
        for i, url in enumerate(my_selenium_pointers):
            try:
                obj = {}

                obj['src'] = imgs[i].get_attribute('src')
                obj['page'] = url.get_attribute('href')
                obj['id'] = uuid4()

                data.append(obj)

                fullfilename = os.path.abspath('.')+'\\plaatjes\\'+f"{obj['id']}.jpg"
                urllib.request.urlretrieve(obj['src'], fullfilename)

                with open(fullfilename, "rb") as image_file:
                    obj['img'] = base64.b64encode(image_file.read())

                os.remove(fullfilename)
            except:
                pass

        return True
    else:
        return False
    

def save_to_csv():
    os.system('cls')
    with open("./plaatjes/out.csv", "w") as f:
        wr = csv.DictWriter(f, delimiter=",",fieldnames=list(data[0].keys()))
        wr.writeheader()
        wr.writerows(data)
        os.system('cls')
        print(f"successfully scaped {len(data)} images")


def scrape(min, max):

    driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)
    driver.get("https://www.marktplaats.nl/q/woonaccessoires/")
    try:
        driver.find_element(By.CLASS_NAME, 'gdpr-consent-button').click()
    except:
        pass

    i=min

    while i < max: 
        os.system('cls')

        urls = driver.find_elements(By.CSS_SELECTOR,'.mp-Listing-coverLink[href]')
        imgs = driver.find_elements(By.CSS_SELECTOR, '.mp-Listing-image-item--main img')
        if(save(urls, imgs)):
            i+=1 
            driver.get(f"https://www.marktplaats.nl/q/woonaccessoires/p/{i}/")
        else:
            break

page_count_thread = round(PAGE_COUNT / THREADS)

t1 = Thread(target=scrape, args=(0, page_count_thread))
t2 = Thread(target=scrape, args=(page_count_thread * 1, page_count_thread * 2))
t3 = Thread(target=scrape, args=(page_count_thread * 2+1, page_count_thread * 3))
t4 = Thread(target=scrape, args=(page_count_thread * 3+1, page_count_thread * 4))

t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()

# scrape(0, PAGE_COUNT)

save_to_csv()