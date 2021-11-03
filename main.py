import requests
from bs4 import BeautifulSoup
import json
import time
from dotenv import dotenv_values
config = dotenv_values(".env")

#once daily (can serve to wake up java api as well)
#put base URL in dot env
#create list of resorts slugs
#loop over list of resorts
    #insert resort slug into base url
    #get snow, and date reported
    #add slug, snow, date reported and current date (date collected) to object
        #jsonify object, send to java api

f = open('resorts.json')
data = json.load(f)
for key, val in data.items():
    page = requests.get(val)
    soup = BeautifulSoup(page.content, "html.parser")
    yesterday = soup.find_all('div', string=config['STRING'])
    parent = yesterday[0].parent

    #remove " from snow
    #convert date to back end format
    snow = parent.find('div', config['SNOW']).text.strip()
    date = parent.find('div', config['DATE']).text.strip()
    
    print(key, val)
    print(snow, date)
    time.sleep(1) 


f.close()