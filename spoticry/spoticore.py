import sys
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
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException


# Data organization to be logged
class session():
    def __init__(self, user):  
        self.user = user
        self.id = hashlib.md5(user['email']) 
        self.country = user['proxy']['country']
        self.ostreams = 0
        self.xstreams = 0
        self.ctime = time.ctime()

    # Increment counter for number of 'critical' streams, and total streams
    def newXStream(self):
        self.xstreams += 1
        self.ostreams += 1

    # Increment counter for total number of streams
    def newOStream(self):
        self.ostreams += 1   

    # Returnes estimated profit 
    def getEstimatedProfit(self):
        return self.xstreams*0.00437, self.xstreams*0.00331     

    def exit(self):
        hiprof, loprof = self.getEstimatedProfit()

        # Returned JSON object
        data = {
            "sessionId": self.id,
            "region": self.country,
            "start": self.ctime,
            "end": time.ctime(),
            "totalStreams": self.ostreams,
            "profitableStreams": self.xstreams,
            "highEstProfit": str(round(hiprof, 2)),
            "lowEstProfit": str(round(loprof, 2))
        }

        # Create relative file path
        utils.makedir('src/sessionlogs')
        filename = 'src/sessionlogs/' + self.id + '.json'

        # Export
        try:
            with open(filename, 'x') as x:
                json.dump(data, x, indent=4)
        except:
            print("\n>>> " + bcolors.FAIL + "ERROR\n>>> Could not create JSON file\n" + bcolors.ENDC)  

# Webdriver controller
class userinstance():
    def __init__(self, web, user, site, wait=None):

        print(">> " + bcolors.OKCYAN + "Initializing Webplayer instance..." + bcolors.ENDC)

        # Options argument initalization
        chrome_options = webdriver.ChromeOptions()                  

        chrome_options.add_argument('--proxy-server=%s' % user['proxy']['ip'])  # Assigns proxy
        # chrome_options.add_argument('--headless')                             # Specifies GUI display, set to headless (NOGUI)
        chrome_options.add_argument('--ignore-certificate-errors')              # Minimize console output
        chrome_options.add_argument('--ignore-ssl-errors')                      # Minimize console output
        chrome_options.add_argument('log-level=3')                              # Minimize console output

        chrome_options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])   # Disable pop-ups? maybe?

        self.user = user
        self.site = site     
        self.web = eval(web)
        self.web.implicitly_wait(30)

        self.web.get('https://accounts.spotify.com/us/login')   
        time.sleep(5)

        self.dSend(site['login']['loginEmail'], user['email'])
        self.dSend(site['login']['loginPassword'], user['pass'])
        self.dClick(site['login']['loginButton'])
        self.dClick(site['login']['webplayerButton']) 
    
        print(">> \t" + bcolors.OKCYAN + "Complete" + bcolors.ENDC)
    
    def tearDown(self):
        self.web.quit()
        self.assertEqual([], self.verificationErrors) 

    # Dynamic click -> wait function
    def dClick(self, xpath):
        a = self.web.find_element(By.XPATH, xpath)
        a.click()
        time.sleep(random.randint(random.randint(3, 4), random.randint(6, 10)))

    # Dynamic send keys -> wait function
    def dSend(self, xpath, data):   
        a = self.web.find_element(By.XPATH, xpath)
        a.send_keys(data)
        time.sleep(random.randint(random.randint(3, 4), random.randint(6, 10))) 

    # Dynamic clear -> wait function
    def dClear(self, xpath):
        a = self.web.find_element(By.XPATH, xpath)
        a.clear()
        time.sleep(random.randint(random.randint(3, 4), random.randint(6, 10)))   

    def newPlaylist(self, title, description, image):

        self.dClick("//button[@data-testid='create-playlist-button']")           # "Create Playlist"
        self.dClick("//div[@id='main']/div/div[2]/div[3]/main/div[2]/div[2]/div/div/div[2]/section/div/div[5]/span/button/span/h1")     # Playlist title select
        self.dClick("(.//*[normalize-space(text()) and normalize-space(.)='Confirm My Choices'])[1]/following::div[4]")                 # Click edit title box
        
        self.dClear("//input[@data-testid='playlist-edit-details-name-input']")         # Remove default text from playlist title
        self.dSend("//input[@data-testid='playlist-edit-details-name-input']", title)   # Edit playlist title 

        self.dClear("(.//*[normalize-space(text()) and normalize-space(.)='Description'])[1]/following::textarea[1]")               # Remove playlist description
        self.dSend("(.//*[normalize-space(text()) and normalize-space(.)='Description'])[1]/following::textarea[1]", description)   # Edit playlist description

        a008 = self.web.find_element(By.XPATH, "(.//*[normalize-space(text()) and normalize-space(.)='Edit details'])[1]/following::*[name()='svg'][3]")
        a008.click()
        time.sleep(random.randint(4, 7))

        a010 = self.web.find_element(By.XPATH, "//input[@type='file']")
        a010.send_keys(image)
        time.sleep(random.randint(4, 7))

        # Close file-picker dialogue 
        webdriver.ActionChains(self.web).send_keys(Keys.ESCAPE).perform()

        # "Save" 
        save = self.web.find_element(By.XPATH, "//button[@data-testid='playlist-edit-details-save-button']")
        save.click()
        time.sleep(random.randint(4, 7))

        # Return to open.spotify.com
        home = self.web.find_element(By.XPATH, "//div[@id='main']/div/div[2]/nav/div/ul/li/a/span"),
        home.click()
        time.sleep(21)

        self.web.close()

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

    # Initialization 
    test = userinstance(trigger, user, site)
    
    # Test new playlist
    test.newPlaylist("hi from selenium!","a test playlist generated with selenium", "D:\Personal Files\Autostream\spoticry\src\img\image14122021031438.jpg")


if __name__ == "__main__":
    newinstance({'email': 'me@rengland.org', 'pass': '!8192Rde', 'proxy': {'ip': '209.127.170.150:8243', 'country': 'US'}})     