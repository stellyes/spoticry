from asyncio import exceptions
import os
import sys
import time
import json
import utils
import string
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

START = "start"
RESUME = "resume"


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
    def __init__(self, user, site, state):

        if (state=="start"):
            print(">> " + bcolors.OKCYAN + "Initializing Webplayer instance..." + bcolors.ENDC)

            # Webdriver service object
            # webdriverChromeService = Service('src/webdriver/chromedriver.exe')

            # Options argument initalization
            chrome_options = webdriver.ChromeOptions()                  

            chrome_options.add_argument('--proxy-server=%s' % user['proxy']['ip'])                  # Assigns proxy
            # chrome_options.add_argument('--headless')                                             # Specifies GUI display, set to headless (NOGUI)
            chrome_options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])   # Disable pop-ups? maybe?
            chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])           # Disable all logging

            self.user = user
            self.site = site     
            self.web = eval(self.site['login']['webdriver'])
            self.session_id = self.web.session_id
            self.executor_url = self.web.command_executor._url

            self.web.get('https://accounts.spotify.com/us/login')   
            time.sleep(5)

            self.dSend(site['login']['loginEmail'], user['email'])
            self.dSend(site['login']['loginPassword'], user['pass'])
            self.dClick(site['login']['loginButton'])
            self.dClick(site['login']['webplayerButton']) 

            print(">> \t" + bcolors.OKCYAN + "Complete" + bcolors.ENDC)
        elif (state=="resume"):
            return 3
    
    def shutdown(self):
        print(">>\n>> Session ID: " + self.session_id + " | >> Execute URL: " + self.executor_url)
        self.web.quit() 

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

    # Only random sleep functionality
    def dSleep(self):
        time.sleep(random.randint(random.randint(3, 4), random.randint(6, 10)))      

    # Bool function to check if element exists on webpage
    def exists(self, xpath):
        try:
            self.web.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            self.dSleep()
            return False
        self.dSleep()    
        return True    

    # Replaces $INDEX marker in XPATH 
    def indexString(self, xpath, index):
        return xpath.replace("$INDEX", index)    

    # Returns number of subelements
    def countPlaylists(self, xpath):       
        count = 0
        cond = True

        try:
            while(cond):
                test = self.indexString(xpath, str(count + 1))
                if (self.exists(test)):
                    count += 1
        except NoSuchElementException:
            return count  
    
    # Return to open.spotify.com
    def home(self):
        self.dClick(self.site['sidebarNav']['homeButton']) 

    # Toggle shuffle feature on/off
    def toggleShuffle(self):
        self.dClick(self.site['songControls']['shuffleButton'])  

    # Toggle repeat between off/queue/song repeat
    def toggleRepeat(self):
        self.dClick(self.site['songControls']['repeatButton'])      

    def toggleMute(self):
        self.dClick(self.site['songControls']['muteButton'])

    # Toggle play/pause master controls
    def playPause(self):
        self.dClick(self.site['songControls']['playPauseButton']) 

    # Skip to next song in queue
    def skipForward(self):
        self.dClick(self.site['songControls']['skipForwardButton']) 

    # Skip back to beginning of track/previous song
    def skipBack(self):
        self.dClick(self.site['songControls']['skipBackButton'])            

    def openQueue(self):
        self.dClick(self.site['songControls']['queueButton'])

    # Creates playlist from passed in credentials
    def createPlaylist(self, title, description, image):
        self.dClick(self.site['sidebarNav']['createPlaylist'])           # "Create Playlist"
        self.dClick(self.site['playlistNav']['playlistTitle'])     # Playlist title select
        self.dClick("(.//*[normalize-space(text()) and normalize-space(.)='Confirm My Choices'])[1]/following::div[4]")                 # Click edit title box
        self.dClear("//input[@data-testid='playlist-edit-details-name-input']")         # Remove default text from playlist title
        self.dSend("//input[@data-testid='playlist-edit-details-name-input']", title)   # Edit playlist title 
        self.dClear("(.//*[normalize-space(text()) and normalize-space(.)='Description'])[1]/following::textarea[1]")               # Remove playlist description
        self.dSend("(.//*[normalize-space(text()) and normalize-space(.)='Description'])[1]/following::textarea[1]", description)   # Edit playlist description
        self.dClick("(.//*[normalize-space(text()) and normalize-space(.)='Edit details'])[1]/following::*[name()='svg'][3]")       # Click edit image
        self.dSend("//input[@type='file']", image)                      # Send image
        self.dClick(self.site['playlistNav']['editDetails']['save'])    # "Save" 
        self.home()

    def selectPlaylist(self):
        self.dClick("//span[@as='span'][text()='Your Library']")

        index = str(random.randint(2 , self.countPlaylists(self.site['sidebarNav']['yourLibrary_options']['playlistSelect'])))
        xpath = self.indexString(self.site['sidebarNav']['yourLibrary_options']['playlistSelect'], index)
        self.dClick(xpath)

    


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

    # Initialization 
    test = userinstance(user, site, START)

    try:
        '''
        Quarantining:
            test.selectPlaylist()
        '''
        # test.newPlaylist("hi from selenium!","a test playlist generated with selenium", utils.absolutePath(utils.fetch_image(1)))     Functional
        # test.playPause()  
        # test.skipBack()
        # test.skipForward()
        # test.toggleShuffle()
        # test.toggleRepeat()
        # test.toggleMute()
    except NoSuchElementException as E:
        print(E)
    except AttributeError as E:
        print(E)    

if __name__ == "__main__":
    newinstance({'email': 'me@rengland.org', 'pass': '!8192Rde', 'proxy': {'ip': '185.245.26.63:6580', 'country': 'US'}})     


    """
        driver.find_element_by_xpath("//div[@id='main']/div/div[2]/nav/div/div[2]/div/div[4]/div[4]/div/div/ul/div/div[2]/li[2]/div/a/span").click()
        driver.find_element_by_link_text("name").click()
        driver.find_element_by_link_text("hgs").click()
        driver.find_element_by_xpath("//div[@id='main']/div/div[2]/nav/div/div[2]/div/div[4]/div[4]/div/div/ul/div/div[2]/li[10]/div/a/span").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Feb 16, 2021'])[1]/following::*[name()='svg'][3]").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Feb 16, 2021'])[2]/following::*[name()='svg'][1]").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Feb 16, 2021'])[2]/following::*[name()='svg'][2]").click()
        driver.find_element_by_xpath("//div[@id='tippy-1607']/ul/li[2]/button/span").click()
    """