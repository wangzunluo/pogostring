from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import os
import time
import requests

def pullpvp():
    op = Options()
    op.set_preference("browser.download.folderList", 2)
    op.set_preference("browser.download.manager.showWhenStarting", False)
    op.set_preference("browser.download.dir", os.getcwd()+'/raw')
    browser = webdriver.Firefox(options=op)
    browser.get('https://pvpoke.com/rankings/all/1500/overall/')
    a = browser.find_element(By.LINK_TEXT, 'Export to CSV')
    time.sleep(5)
    a.click()
    print('done 1')
    browser.get('https://pvpoke.com/rankings/all/2500/overall/')
    a = browser.find_element(By.LINK_TEXT, 'Export to CSV')
    time.sleep(5)
    a.click()
    print('done 2')


    browser.get('https://pvpoke.com/rankings/all/10000/overall/')
    a = browser.find_element(By.LINK_TEXT, 'Export to CSV')
    time.sleep(5)
    a.click()
    print('done 3')

    browser.close()

    
def pullpve():
    url = 'https://docs.google.com/spreadsheets/d/'\
        '{}/gviz/tq?tqx=out:csv&sheet={}'
    id = '1avftwmBHszB0s1_5-Z_REvvAMXdLk0vMJI3GYsSWGkg'
    name = 'PVE Top'
    sheet = requests.get(url.format(id, name))
    with open('raw/pve.csv', 'w') as f:
        f.write(sheet.text)

pullpve()
pullpvp()