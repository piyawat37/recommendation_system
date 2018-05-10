'''
Created on May 5, 2018

@author: Piyawat Pemwattana
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import os
import urllib
import argparse
import requests
import cv2
import absPath, re
from connectMongoDB import _connect_mongo
from selenium.webdriver.chrome.options import Options

db = _connect_mongo(host='localhost', port=27017, username=None, password=None, db='recommendation_system')
# MAX_RANGES = 250
def include_image(keyword):
    keyword = keyword
    fileName = ''
    googleSearch = "https://www.google.co.in/search?q="+keyword+"&source=lnms&tbm=isch"
    browser = webdriver.Chrome(absPath.chrome_driver_path())
    browser.get(googleSearch)
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    
    # Start search
    print("[INFO] searching images '{}' from Google with Chrome.. ".format(keyword))
    
    
    directory = absPath.movies_image_path()
    keyword = re.sub('\W+', '', keyword)
    for x in browser.find_elements_by_xpath('//div[contains(@class,"rg_meta")]'):
        try:
            url = json.loads(x.get_attribute('innerHTML'))["ou"]
            print("[INFO] fetching: {}".format(url))
            requestFile = requests.get(url, timeout=30)
            fileName = keyword + url[url.rfind("."):]
            saveDirectory = os.path.join(directory, fileName)
            f = open(saveDirectory, "wb")
            f.write(requestFile.content)
            f.close()
            image = cv2.imread(saveDirectory)
            break
            # if the image is `None` then we could not properly load the
            # image from disk (so it should be ignored)
            if image is None:
                print("[INFO] deleting: {}...".format(fileName))
                os.remove(saveDirectory)
                continue
        except Exception as e:
            print("[ERR] Skipping >> URL {} doesn't load...".format(url))
            print("[ERR] {}... ".format(e))
            continue
        

def generate_image_all():
    options = Options()
    options.add_argument("--headless") # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox') # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized') # 
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    
    movies_list = db.movies.find()
    keyword = ''
    keyword_list = []
    for cursor in movies_list:
        print(cursor['title'])
        keyword_list.append(cursor['title'])
    fileName = ''
    
    directory = absPath.movies_image_path()
    for keyword in keyword_list:
        googleSearch = "https://www.google.co.in/search?as_st=y&tbm=isch&hl=th&as_q="+keyword+"&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=ift:jpg"
#         googleSearch = "https://www.google.co.in/search?q="+keyword+"&as_st=y&hl=th&tbs=ift:png&tbm=isch&source=lnt&sa=X&ved=0ahUKEwjazIHD7PjaAhXHo48KHX3WBI0QpwUIHA&biw=1920&bih=987&dpr=1"
#         googleSearch = "https://www.google.co.in/search?q="+keyword+"&source=lnms&tbm=isch"
        browser = webdriver.Chrome(executable_path=absPath.chrome_driver_path(), chrome_options=options)
        browser.get(googleSearch)
        header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        
        # Start search
        print("[INFO] searching images '{}' from Google with Chrome.. ".format(keyword))
        keyword_regex = re.sub('\W+', '', keyword)
        for x in browser.find_elements_by_xpath('//div[contains(@class,"rg_meta")]'):
            try:
                url = json.loads(x.get_attribute('innerHTML'))["ou"]
                print("[INFO] fetching: {}".format(url))
                requestFile = requests.get(url, timeout=30)
                fileName = keyword_regex + url[url.rfind("."):]
                saveDirectory = os.path.join(directory, fileName)
                f = open(saveDirectory, "wb")
                f.write(requestFile.content)
                f.close()
                image = cv2.imread(saveDirectory)
                db['movies'].find_one_and_update({'title':keyword}, {'$set': {'fileImage': fileName}})
                break
                # if the image is `None` then we could not properly load the
                # image from disk (so it should be ignored)
                if image is None:
                    print("[INFO] deleting: {}...".format(fileName))
                    os.remove(saveDirectory)
                    continue
            except Exception as e:
                print("[ERR] Skipping >> URL {} doesn't load...".format(url))
                print("[ERR] {}... ".format(e))
                continue

generate_image_all()