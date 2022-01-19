import site
import time
import json
import utils
import random
import hashlib
import requests

from utils import bcolors
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service




class userinstance:
    def __init__(self, web, user, site):

        print(">> " + bcolors.OKCYAN + "Initializing Webplayer instance..." + bcolors.ENDC)

        # Options argument initalization
        chrome_options = webdriver.ChromeOptions()                  

        chrome_options.add_argument('--proxy-server=%s' % user['proxy']['ip'])  # Assigns proxy
        # chrome_options.add_argument('--headless')                             # Specifies GUI display, set to headless (NOGUI)
        #chrome_options.add_argument('--ignore-certificate-errors')              # Minimize console output
        #chrome_options.add_argument('--ignore-ssl-errors')                      # Minimize console output
        #chrome_options.add_argument('log-level=3')                              # Minimize console output

        self.user = user
        self.site = site     
        self.web = eval(web)

        self.web.get('https://accounts.spotify.com/no/login')   
        time.sleep(5)

        email = self.web.find_element(By.XPATH, site['login']['loginEmail'])
        email.send_keys(user['email'])
        time.sleep(random.randint(2, 8))

        password = self.web.find_element(By.XPATH, site['login']['loginPassword'])
        password.send_keys(user['pass'])
        time.sleep(random.randint(2, 8))

        login = self.web.find_element(By.XPATH, site['login']['loginButton'])
        login.click()
        time.sleep(random.randint(5, 10))

        webplayer = self.web.find_element(By.XPATH, site['login']['webplayerButton'])
        webplayer.click()    
    
        print(">> \t" + bcolors.OKCYAN + "Complete" + bcolors.ENDC)
        time.sleep(random.randint(3, 8))

    def newPlaylist(self):
        create = self.web.find_element(By.XPATH, self.site['createPlaylist'])
        create.click()
        time.sleep(random.randint(2, 5))

        rename = self.web.find_element(By.CLASS_NAME, self.site['playlistImage'])
        result = utils.fetch_image(1)
        rename.send_keys(result)
        time.sleep(random.randint(3, 7))

        save = self.web.find_element(By.CLASS_NAME, self.site['playlistEditSave'])
        save.click()
        time.sleep(random.randint(15))


def generate_user(user):

    gender = user['gender']

    if gender == 0:
        parsed_gender = "male"
    elif gender == 1:
        parsed_gender = "female"
    elif gender == 2:
        parsed_gender = "non-binary"
        
    headers={"Accept-Encoding": "gzip",
             "Accept-Language": "en-US",
             "App-Platform": "Android",
             "Connection": "Keep-Alive",
             "Content-Type": "application/x-www-form-urlencoded",
             "Host": "spclient.wg.spotify.com",
             "User-Agent": "Spotify/8.6.72 Android/29 (SM-N976N)",
             "Spotify-App-Version": "8.6.72",
             "X-Client-Id": utils.generate_random_string(32)}
    
    payload = {"creation_point": "client_mobile",
            "gender": parsed_gender,
            "birth_year": user['dob']['year'],
            "displayname": user['user'],
            "iagree": "true",
            "birth_month": user['dob']['month'],
            "password_repeat": user['pass'],
            "password": user['pass'],
            "key": "142b583129b2df829de3656f9eb484e6",
            "platform": "Android-ARM",
            "email": user['email'],
            "birth_day": user['dob']['day']}
    
    r = requests.post('https://spclient.wg.spotify.com/signup/public/v1/account/', headers=headers, data=payload)

    if r.status_code==200:
        if r.json()['status']==1:
            return (True, time.time())
        else:
            #Details available in r.json()["errors"]
            print(r.json()["errors"])
            return (False, "Could not create the account, some errors occurred")
    else:
        return (False, "Could not load the page. Response code: "+ str(r.status_code))             


def newinstance(user):

    # Create sitemap and trigger objects for webdriver
    site = utils.get_sitemap()
    trigger = site['login']['webdriver']

    # Grab proxy from passed user
    proxy = user['proxy']['ip']

    # Initialization 
    test = userinstance(trigger, user, site)
    
    # Test new playlist
    test.newPlaylist()


if __name__ == "__main__":
    newinstance({'email': 'spoticrier@gmail.com', 'pass': '!8192spoticry', 'proxy': {'ip': '45.192.138.248:6890', 'country': 'NO'}})   