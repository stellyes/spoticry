import os
import sys
import time
import json
import utils
import random
import shutil
import pickle
import hashlib
import requests

from utils import bcolors
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# First page has been parsed, reference this:
# https://developers.whatismybrowser.com/useragents/explore/software_name/spotify/2

USER_AGENT_PC = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Spotify/1.1.31.703 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Spotify/1.1.32.618 Safari/537.36",
    "Spotify/117400631 Win32/0 (PC desktop)",
    "Spotify/117300517 Win32/0 (PC laptop)",
    "Spotify/117400631 Win32/0 (PC laptop)",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Spotify/1.1.33.569 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Spotify/1.1.30.658 Safari/537.36",

]

USER_AGENT_iOS = [
    "Spotify/1.0",
    "Spotify/8.6.84 iOS/15.1 (iPhone12,1)",
    "Spotify/8.6.84 iOS/15.1.1 (iPhone13,2)",
    "Spotify/8.6.84 iOS/15.1 (iPhone11,8)",
    "Spotify/8.6.84 iOS/15.1 (iPhone12,8)",
    "Spotify/8.6.84 iOS/15.1 (iPhone10,4)",
    "Spotify/8.6.82 iOS/14.8.1 (iPhone12,1)",
    "Spotify/8.6.94 iOS/15.1.1 (iPhone13,2)",
    "Spotify/8.6.82 iOS/14.8.1 (iPhone13,2)",
    "Spotify/8.6.84 iOS/15.1 (iPhone11,2)",
    "Mozilla/5.0 (iPhone; CPU OS 12_2_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25 Spotify/856800921 (36; 2; 3)",
    "Spotify/8.6.84 iOS/15.1.1 (iPhone13,1)",
    "Spotify/8.6.96 iOS/15.1 (iPhone12,1)",
    "Spotify/8.6.82 iOS/15.1 (iPhone12,1)",
    "Spotify/8.6.84 iOS/14.8.1 (iPhone10,4)",
    "Spotify/8.6.84 iOS/14.8.1 (iPhone13,3)",
    "Spotify/8.6.84 iOS/14.8.1 (iPhone13,3)",
    "Spotify/8.6.96 iOS/15.1 (iPhone12,8)",
    "Spotify/8.6.84 iOS/14.8.1 (iPhone9,3)",
    "Spotify/8.6.84 iOS/15.1 (iPhone9,3)",
    "Spotify/8.6.30 iOS/14.6 (iPhone10,4)",
    "Spotify/8.6.84 iOS/15.1 (iPhone12,5)",
    "Spotify/8.6.96 iOS/15.1.1 (iPhone13,2)",
    "Spotify/8.6.84 iOS/15.1.1 (iPhone13,3)",
    "Spotify/8.6.84 iOS/15.1.1 (iPhone14,5)",
    "Spotify/8.6.84 iOS/14.8.1 (iPhone12,1)",
    "Spotify/8.6.82 iOS/15.1 (iPhone13,2)",
    "Spotify/8.6.30 iOS/14.6 (iPhone12,8)",
    "Spotify/8.6.84 iOS/14.7.1 (iPhone12,3)",
    "Spotify/8.6.52 iOS/14.6 (iPhone12,8)",
    "Spotify/8.6.84 iOS/15.1 (iPhone12,3)"
]

USER_AGENT_ANDROID = [
    "Spotify/1.0",
    "Spotify/8.6.88.1104 Android/30 (SM-A415F)",
    "Spotify/8.6.88.1104 Android/30 (SM-G973F)",
    "Spotify/8.6.94.306 Android/30 (M2102J20SG)",
    "Spotify/8.6.94.306 Android/30 (SM-G975F)",
    "Spotify/8.6.88.1104 Android/30 (SM-A525F)",
    "Spotify/8.4.49 Android/28 (LG)",
    "Spotify/8.6.88.1104 Android/30 (SM-A505FN)",
    "Spotify/8.6.98.900 Android/31 (SM-G986B)",
    "Spotify/8.4.88 Android/28 (SM-A105FN)",
    "Spotify/8.6.88.1104 Android/30 (SM-G981B)",
    "Spotify/8.6.74.1176 Android/30 (SM-G991B)",
    "Spotify/8.6.84.1240 Android/30 (SM-A705FN)",

]

START = "start"
RESUME = "resume"

BL_AUTHORS = ['Spotify']
BL_ARTISTS = ['Drake']

ACC_ACTIVE = 'src/resources/users/active'
ACC_INACTIVE = 'src/resources/users/inactive'
ACC_QUARANTINE = 'src/resources/users/quarantine'

AUTHORS = ['ryan', 'olivbeea']
ARTISTS = ['deo autem nihil', '18pm', '18PM', 'Exploitsound', 'exploitsound', 'BADTIME!', 'Ｏｃｅａｎ Ｓｈｏｒｅｓ']

PLAYLIST = "playlist"
ALBUM = "album"
ARTIST = "artist"
SONG = "song"


class Error(Exception):
    """Base class for other exceptions"""

class SpoticryRuntimeError(Error):
    """General debugging, 'pass' functionality"""
    pass

# Data organization to be logged
class session():
    def __init__(self, user):  
        self.user = user
        self.id = hashlib.md5(user['email']) 
        self.country = user['proxy']['country']
        self.ostreams = 0
        self.xstreams = 0
        self.ctime = time.ctime()
        self.runtimeExceptions = []

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

    # Record error and append to runtimeException attribute
    def error(self, error):
        try:
            self.runtimeExceptions.append(error)
        except:
            print(">> " + bcolors.FAIL + "ERROR: Unable to add runtime error to session logs. Aborting process..." + bcolors.ENDC)            

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
            "lowEstProfit": str(round(loprof, 2)),
            "runtimeExceptions": self.runtimeExceptions
        }

        # Create relative file path
        utils.makedir('src/resources/sessionlogs')
        filename = 'src/resources/sessionlogs/' + self.id + '.json'

        # Export
        try:
            with open(filename, 'x') as x:
                json.dump(data, x, indent=4)
        except:
            print("\n>>> " + bcolors.FAIL + "ERROR\n>>> Could not create JSON file\n" + bcolors.ENDC)  

# Webdriver controller
class userinstance():
    def __init__(self, user, site):
        # Options argument initalization
        chrome_options = webdriver.ChromeOptions()          

        # chrome_options.add_argument('--proxy-server=%s' % user['proxy']['ip'])                  # Assigns proxy
        # chrome_options.add_argument('--headless')                                             # Specifies GUI display, set to headless (NOGUI)
        chrome_options.add_argument("--mute-audio")                                             # Mute audio output
        #chrome_options.add_argument(f'user-agent={random.choice(USER_AGENT_PC)}')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])   # Disable pop-ups? maybe?
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])           # Disable all logging        


        print(">> " + bcolors.OKCYAN + "Initializing Webplayer instance..." + bcolors.ENDC)

        # Webdriver service object
        # webdriverChromeService = Service('src/webdriver/chromedriver.exe')

        # Assign user data and evaluate webdriver command via sitemap
        self.user = user
        self.site = site     
        self.web = eval(self.site['login']['webdriver'])

        if os.path.exists("src/resources/cookies/spoticry.pk1"):
            self.web.get("https://open.spotify.com/")
            cookies = pickle.load(open("src/resources/cookies/spoticry.pk1", "rb"))
            for cookie in cookies:
                self.web.add_cookie(cookie)
            time.sleep(3)
            self.web.refresh()
            print(">> " + bcolors.OKCYAN + "Webplayer succesfully initialized" + bcolors.ENDC)
            time.sleep(1)
            print(">> ")
        else:
            # Builds corresponding URL to proxy host location
            url = "https://accounts.spotify.com/" + user['proxy']['country'].lower() + "/login"

            # Open Spotify login URL
            self.web.get(url)   
            self.web.maximize_window()
            self.dSleep()
            
            # Input login credentials
            self.dSend(site['login']['loginEmail'], user['email'])
            self.dSend(site['login']['loginPassword'], user['pass'])
            self.dClick(site['login']['loginButton'])

            self.dSleep()

            # Handles login errors
            if self.exists("//div[@data-testid='login-container']/div[@role='alert']"):
                errormessage = self.web.find_element(By.XPATH, "//div[@data-testid='login-container']/div[@role='alert']/span/p").text
                try:
                    quarantineUser("src/resources/users/active/" + user['user'] + ".json")
                except:
                    print(">>\t" + bcolors.FAIL + "ERROR: Unable to quarantine user '" + user['user'] + "'" + bcolors.ENDC)   
                print(">>\t" + bcolors.FAIL + "ERROR: Login failed \"" + errormessage.removesuffix('.') + "\". Shutting down." + bcolors.ENDC)
                raise Exception("\n>>\n>> END SESSION")

            # Click Webplayer option
            self.dClick(site['login']['webplayerButton']) 

            print(">> " + bcolors.OKCYAN + "Webplayer succesfully initialized" + bcolors.ENDC)
            time.sleep(1)
            print(">> ")
            

    # Handles closing of webdriver instance
    def shutdown(self):
        # Attempt to gather cookies
        try:
            print(">> " + bcolors.OKCYAN + "Attempting to gather cookies from browser session..." + bcolors.ENDC)
            utils.makedir("src/resources/cookies/")
            cookie_dir = "src/resources/cookies/" + self.user['user'] + ".pk1"
            pickle.dump(self.web.get_cookies(), open(cookie_dir, "wb"))
            print(">> " + bcolors.OKCYAN + "Cookies successfully stored." + bcolors.ENDC)
        except:
            print(">> " + bcolors.WARNING + "Failed to gather cookies..." + bcolors.ENDC)

        self.web.quit()

    # Dynamic scroll -> wait function
    def dScroll(self):
        self.web.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
        self.dSleep()

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

    # Returns collection of sub elements from referenced XPATH
    def dSearch(self, xpath):
        a = self.web.find_elements(By.XPATH, xpath)
        time.sleep(random.randint(random.randint(3, 4), random.randint(6, 10))) 
        return a       

    # Bool function to check if element exists on webpage
    def exists(self, xpath):
        try:
            self.web.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            self.dSleep()
            return False
        self.dSleep()    
        return True    

    def recursiveScrape(self, iurl="https://open.spotify.com/artist/36r4ltZmLqtiDBdAs9XSqn", **opcode):
        print(">> " + bcolors.OKGREEN + "Starting recursive scrape function..." + bcolors.ENDC)

        imported = []
        scraped = []

        # Collects all imported album file names
        utils.makedir("src/resources/artists/")
        for root, dirs, files in os.walk("src/resources/artists/"):
            for file in files:
                if(file.endswith(".json")):
                    imported.append(file.removesuffix(".json"))

        if iurl not in scraped:
            try:
                while(1):
                    url = scraped.pop()
                    self.web.get(url)
                    self.dSleep()
        
                    name = self.web.find_element(By.XPATH, "//section[@data-testid='artist-page']/div/div[1]/div[2]/span[2]/h1").text

                    print(">> " + bcolors.OKGREEN + "Parsing items from " + name + "..." + bcolors.ENDC)
                    # Parse discography and add to txt files
                    try:
                        discography_albums_url = url + "/discography/album"
                        discography_songs_url = url + "/discography/single"
                        discography_appearson = url + "/appears-on"
                        related_artists = url + "/related"
                        
                        scraped.append(self.web.current_url)

                        print(">>\t\t" + bcolors.OKGREEN + "Parsing albums..." + bcolors.ENDC)
                        self.web.get(discography_albums_url)

                        gridview = "//section[@data-testid='artist-page']/div/div[1]/button[@aria-label='grid']"
                        enabled_grid = self.web.find_element(By.XPATH, gridview).get_attribute('aria-checked')

                        if enabled_grid == 'false':
                            self.dClick(gridview)

                        self.dSleep()
                        with open("src/resources/txt/albums.txt", "a") as file:
                            i = 1
                            try:
                                while(True):
                                    albumxpath = "//section[@data-testid='artist-page']/div/div[@data-testid='grid-container']/div[" + str(i) + "]/div/div[2]/a"
                                    albumlink = self.web.find_element(By.XPATH, albumxpath).get_attribute('href')
                                    file.write(albumlink + "\n")
                                    i += 1
                                    time.sleep(1)
                            except NoSuchElementException:
                                print(">>\t\t\t" + bcolors.OKGREEN + "Finished parsing albums!" + bcolors.ENDC)
                        

                        print(">>\t\t" + bcolors.OKGREEN + "Parsing singles and EPs..." + bcolors.ENDC)
                        self.web.get(discography_songs_url)

                        self.dSleep()
                        with open("src/resources/txt/albums.txt", "a") as file:
                            i = 1
                            try:
                                while(True):
                                    albumxpath = "//section[@data-testid='artist-page']/div/div[@data-testid='grid-container']/div[" + str(i) + "]/div/div[2]/a"
                                    albumlink = self.web.find_element(By.XPATH, albumxpath).get_attribute('href')
                                    file.write(albumlink + "\n")
                                    i += 1
                                    time.sleep(1)
                            except NoSuchElementException:
                                print(">>\t\t\t" + bcolors.OKGREEN + "Finished parsing singles and EPs!" + bcolors.ENDC)


                        print(">>\t\t" + bcolors.OKGREEN + "Parsing featured releases..." + bcolors.ENDC)
                        self.web.get(discography_appearson)   
                        self.dSleep()       
                        with open("src/resources/txt/albums.txt", "a") as file:
                            i = 1
                            try:
                                while(True):
                                    albumxpath = "//section[@data-testid='artist-page']/div/div[@data-testid='grid-container']/div[" + str(i) + "]/div/div[2]/a"
                                    albumlink = self.web.find_element(By.XPATH, albumxpath).get_attribute('href')
                                    file.write(albumlink + "\n")
                                    i += 1
                                    time.sleep(1)
                            except NoSuchElementException:
                                print(">>\t\t\t" + bcolors.OKGREEN + "Finished parsing featured releases!" + bcolors.ENDC)    


                        print(">>\t\t" + bcolors.OKGREEN + "Parsing related artists..." + bcolors.ENDC)
                        self.web.get(related_artists)      
                        self.dSleep()      
                        with open("src/resources/txt/artists.txt", "a") as file:
                            i = 1
                            try:
                                while(True):
                                    artistxpath = "//section[@aria-label='Fans also like']/div[@data-testid='grid-container']/div[" + str(i) + "]/div/div[2]/a"
                                    artistlink = self.web.find_element(By.XPATH, artistxpath).get_attribute('href')
                                    file.write(artistlink + "\n")
                                    if artistlink not in imported:
                                        imported.append(artistlink)
                                    i += 1
                                    time.sleep(1)
                            except NoSuchElementException:
                                print(">>\t" + bcolors.OKGREEN + "Finished parsing related artists..." + bcolors.ENDC)   

                    except NoSuchElementException:
                        print(">>\t" + bcolors.OKGREEN + "Finished parsing " + name + "!" + bcolors.ENDC)
                    except Exception as E:
                        print(E)
                        print(">>\t" + bcolors.FAIL + " FATAL ERROR: Error parsing " + name + ". Shutting down..." + bcolors.ENDC)
                        self.shutdown()    

            except KeyboardInterrupt:
                print(">>\t" + bcolors.OKGREEN + "Terminating recursive scrape function, returning to home..." + bcolors.ENDC)
                self.home()     
            except NoSuchElementException:
                print(">>\t" + bcolors.WARNING + "Unable to find element on page... ending recursive scrape" + bcolors.ENDC)      
            except Exception as E:
                print(E)
                print(">>\t" + bcolors.FAIL + " FATAL ERROR - Shutting down..." + bcolors.ENDC)
                self.shutdown()      


    # Scrapes song from passed in spotify object 'name'
    def songScrape(self, opcode, name):
        '''
        OP-CODE:
            0 - Scrape songs from playlist
            1 - Scrape songs from album
        '''    
        if opcode == 0:
            print(">>\t" + bcolors.BOLD + bcolors.OKGREEN + "Scraping songs from playlist '" + name + "' ..." + bcolors.ENDC)
            baseXPATH = "//div[@data-testid='playlist-tracklist']/div[2]/div[2]/"
            i = 2
            
            while (i >= 2):
                try:
                    if i % 25 == 0:
                        try:
                            self.dScroll()
                        except: 
                            pass    

                    itemXPATH0 = baseXPATH  + "div[@aria-rowindex='" + str(i) + "']/div/div[2]/div"
                    
                    titleXPATH = itemXPATH0 + "/div"
                    title = self.web.find_element(By.XPATH, titleXPATH).text
                    title = utils.cleanInput(title)

                    j = 1
                    artists = []
                    try:
                        artistXPATH = itemXPATH0 + "/span/a[" + str(j) + "]"
                        artist = self.web.find_element(By.XPATH, artistXPATH).text
                        artists.append[artist]
                    except:
                        artist_string = ""
                        for artist in artists:
                            artist_string = artist_string + artist + ", "
                        artist_string.removesuffix(", ")   
                    artist = artist_string        

                    albumXPATH = baseXPATH  + "div[@aria-rowindex='" + str(i) + "']/div/div[3]/a"
                    album = self.web.find_element(By.XPATH, albumXPATH).text

                    url = self.web.find_element(By.XPATH, albumXPATH).get_attribute('href')

                    pr = random.randint(1, 2) 

                    if artist in ARTISTS:
                        pr = 5                             

                    song_obj = {
                        "title": title,
                        "artist": artist,
                        "album": album,
                        "album-url": url,
                        "priority": pr
                    }   

                    song_object_directory = "src/resources/songs/" + str(pr) + "/"
                    obj_name = title + " - " + artist + ".json"
                    utils.makedir(song_object_directory)

                    if obj_name not in os.listdir(song_object_directory):
                        jsonfile = os.path.join(song_object_directory + obj_name)
                        with open(jsonfile, 'x')as obj:
                            json.dump(song_obj, obj, indent=4)
                        print(">>\t\t" + bcolors.OKGREEN + "Song \'" + title + "\' imported" + bcolors.ENDC)
                    else:
                        print(">>\t\t" + bcolors.WARNING + "Song \'" + title + "\' by " + artist + " entry already exists. Skipping..." + bcolors.ENDC)  
                    
                    time.sleep(random.randint(1, 4))
                    i += 1
                except Exception as E:
                    print(">> " + bcolors.WARNING + "WARNING: Song import interrupted. Aborting process..." + bcolors.ENDC)
                    # self.session
                    i = 1 
            
            print(">>\t" + bcolors.OKGREEN + "Complete" + bcolors.ENDC)

        elif opcode == 1:
            print(">>\t" + bcolors.BOLD + bcolors.OKGREEN + "Scraping songs from album '" + name + "'..." + bcolors.ENDC)
            baseXPATH = "//div[@data-testid='track-list']/div[2]/div[2]"
            i = 2
            
            while (i >= 2):
                try:
                    itemXPATH0 = baseXPATH  + "/div[@aria-rowindex='" + str(i) + "']/div/div[2]/div"
                    
                    titleXPATH = itemXPATH0 + "/div"
                    title = self.web.find_element(By.XPATH, titleXPATH).text
                    title = utils.cleanInput(title)

                    j = 1
                    artists = []
                    try:
                        try:
                            artistXPATH = itemXPATH0 + "/span/a[" + str(j) + "]"
                            artist = self.web.find_element(By.XPATH, artistXPATH).text
                            artists.append[artist]
                        except:
                            artist_string = ""
                            for artist in artists:
                                artist_string = artist_string + artist + ", "
                            artist_string.removesuffix(", ")       
                    except:
                        artistXPATH = itemXPATH0 + "/span/a"
                        artist = self.web.find_element(By.XPATH, artistXPATH).text

                    url = self.web.current_url

                    pr = random.randint(1, 2) 

                    if artist in ARTISTS:
                        pr = 5                             

                    song_obj = {
                        "title": title,
                        "artist": artist,
                        "album": name,
                        "album-url": url,
                        "priority": pr
                    }   

                    song_object_directory = "src/resources/songs/" + str(pr) + "/"
                    obj_name = title + " - " + artist + ".json"
                    utils.makedir(song_object_directory)

                    if obj_name not in os.listdir(song_object_directory):
                        jsonfile = os.path.join(song_object_directory + obj_name)
                        with open(jsonfile, 'x')as obj:
                            json.dump(song_obj, obj, indent=4)
                        print(">>\t\t" + bcolors.OKGREEN + "Song \'" + title + "\' imported" + bcolors.ENDC)
                    else:
                        print(">>\t\t" + bcolors.WARNING + "Song \'" + title + "\' by " + artist + " entry already exists. Skipping..." + bcolors.ENDC)  
                    
                    time.sleep(random.randint(1, 4))
                    i += 1
                except NoSuchElementException as E:
                    print(E)
                    i = 1 
                except:    
                    print(">> " + bcolors.WARNING + "WARNING: Song import interrupted. Aborting process..." + bcolors.ENDC)
                    # self.session
                    i = 1 

            print(">>\t" + bcolors.OKGREEN + "Complete" + bcolors.ENDC)            

    # Imports list of albums in storage file
    def importAlbums(self):
        print(">> " + bcolors.BOLD + bcolors.OKGREEN + "Importing albums..." + bcolors.ENDC)
        imported = []

        # Collects all imported album file names
        for root, dirs, files in os.walk("src/resources/albums/"):
            for file in files:
                if(file.endswith(".json")):
                    imported.append(file.removesuffix(".json"))

        with open("src/resources/txt/albums.txt", "r+") as file:
            # Get lines containing album URLs
            lines = file.readlines()

            for line in lines:
                try:
                    # Get album URL
                    self.web.get(line)
                    self.dSleep()

                    title = self.web.find_element(By.XPATH, "//section[@data-testid='album-page']/div[1]/div[5]/span/h1").text
                    title = utils.cleanInput(title)
                    self.dSleep()    

                    # Get artist of album, except multiple artists
                    try:
                        i = 1
                        artist = ""
                        while i != 0:
                            try:
                                xpath = "//section[@data-testid='album-page']/div[1]/div[5]/div/div[1]/a[" + str(i) + "]"
                                artists = self.web.find_element(By.XPATH, xpath).text
                                artist = artist + artists + ", "
                                i += 1
                            except:
                                i = 0
                        artist.removesuffix(", ")        
                        artist = utils.cleanInput(artist)        
                        self.dSleep()
                    except:
                        artist = self.web.find_element(By.XPATH, "//section[@data-testid='album-page']/div[1]/div[5]/div/div[1]/a").text
                        artist = utils.cleanInput(artist) 
                        self.dSleep()   
                            
                    # Default priority scale
                    pr = random.randint(1, 3)

                    # 5% random chance, gets assigned a 4 priority rating
                    if (utils.chance(5)):
                        pr = 4

                    if artist in ARTISTS:
                        pr = 5

                    url = self.web.current_url

                    self.songScrape(1, title)

                    album_object = {
                        "title": title,
                        "url": url,
                        "artist": artist,
                        "priority": pr
                    }

                    album_object_directory = "src/resources/albums/" + str(pr) + "/"
                    obj_name = title + ".json"
                    utils.makedir(album_object_directory)

                    # Checks current album against existing entries
                    if obj_name not in imported:
                        jsonfile = os.path.join(album_object_directory + obj_name)
                        with open(jsonfile, 'x')as obj:
                            json.dump(album_object, obj, indent=4)
                        imported.append(file)    

                        print(">>\t" + bcolors.OKGREEN + "Album \'" + title + "\' by " + album_object[artist] + "imported" + bcolors.ENDC)
                    else:
                        print(">>\t" + bcolors.WARNING + "Album \'" + title + "\' entry already exists. Skipping..." + bcolors.ENDC)    
                except SpoticryRuntimeError:
                    print(">> ")
                except:
                    print(">> " + bcolors.WARNING + "WARNING: Error parsing album.txt list, clearing text file and resuming..." + bcolors.ENDC)
    
            file.truncate(0)

        print(">> " + bcolors.BOLD + bcolors.OKGREEN + "Albums imported" + bcolors.ENDC)

    # Imports list of playlists in storage file
    def importPlaylists(self):
        print(">> " + bcolors.BOLD + bcolors.OKGREEN + "Importing playlists..." + bcolors.ENDC)
        imported = []

        # Collects all imported album file names
        for root, dirs, files in os.walk("src/resources/playlists/"):
            for file in files:
                if(file.endswith(".json")):
                    imported.append(file.removesuffix(".json"))

        with open("src/resources/txt/playlists.txt", "r+") as file:
            # Get lines containing playlist URLs
            lines = file.readlines()

            for line in lines:
                try:
                    # Get playlist URL
                    self.web.get(line)
                    self.dSleep()

                    try: # If playlist not authored by profile
                        title = self.web.find_element(By.XPATH, "//section[@data-testid='playlist-page']/div[1]/div[5]/span/h1").text   
                    except: # If playlist is authored by profile
                        title = self.web.find_element(By.XPATH, "//section[@data-testid='playlist-page']/div[1]/div[5]/span/button/span/h1").text
                    self.dSleep()    
                    title = utils.cleanInput(title)

                    # Get author of playlist
                    author = self.web.find_element(By.XPATH, "//section[@data-testid='playlist-page']/div[1]/div[5]/div/div[1]/a").text
                    self.dSleep()
                    
                    # Default priority scale
                    pr = random.randint(1, 3)

                    # 5% random chance, gets assigned a 4 priority rating
                    if (utils.chance(5)):
                        pr = 4

                    if author in AUTHORS:
                        pr = 5

                    url = self.web.current_url

                    self.songScrape(0, title)

                    playlist_obj = {
                        "title": title,
                        "url": url,
                        "author": author,
                        "priority": pr
                    }
                    
                    playlist_object_directory = "src/resources/playlists/" + str(pr) + "/"
                    obj_name = title + ".json"
                    utils.makedir(playlist_object_directory)

                    # Checks current album against existing entries
                    if obj_name not in imported:
                        jsonfile = os.path.join(playlist_object_directory + obj_name)
                        with open(jsonfile, 'x')as obj:
                            json.dump(playlist_obj, obj, indent=4)
                        imported.append(file)

                        print(">>\t" + bcolors.OKGREEN + "Playlist \'" + title + "\' imported" + bcolors.ENDC)
                    else:
                        print(">>\t" + bcolors.WARNING + "Playlist \'" + title + "\' entry already exists. Skipping..." + bcolors.ENDC)    
                except SpoticryRuntimeError:
                    print(">> ")
                except:
                    print(">> " + bcolors.WARNING + "WARNING: Error parsing playlists.txt list, clearing text file and resuming..." + bcolors.ENDC)
    
            file.truncate(0)

        print(">> " + bcolors.BOLD + bcolors.OKGREEN + "Playlists imported" + bcolors.ENDC)
   
    # Imports list of artists in storage file
    def importArtists(self):
        print(">> " + bcolors.BOLD + bcolors.OKGREEN + "Importing artists..." + bcolors.ENDC)
        imported = []

        # Collects all imported album file names
        for root, dirs, files in os.walk("src/resources/artists/"):
            for file in files:
                if(file.endswith(".json")):
                    imported.append(file.removesuffix(".json"))

        with open("src/resources/txt/artists.txt", "r+") as file:   
            # Get lines containing playlist URLs
            lines = file.readlines()
            for line in lines:
                try:     
                    # Get playlist URL
                    self.web.get(line)
                    self.dSleep()

                    name = self.web.find_element(By.XPATH, "//section[@data-testid='artist-page']/div/div[1]/div[2]/span[2]/h1").text
                    name = utils.cleanInput(name)
                    self.dSleep()

                    url = self.web.current_url
                    self.dSleep()

                    # Default priority scale
                    pr = random.randint(1, 3)

                    # 5% random chance, gets assigned a 4 priority rating
                    if (utils.chance(5)):
                        pr = 4

                    if name in ARTISTS:
                        pr = 5

                    artist_obj = {
                        "artist": name,
                        "artist-url": url,
                        "priority": pr
                    }

                    artist_object_directory = "src/resources/artists/" + str(pr) + "/"
                    obj_name = name + ".json"
                    utils.makedir(artist_object_directory)

                    # Checks current album against existing entries
                    if name not in imported:
                        jsonfile = os.path.join(artist_object_directory + obj_name)
                        with open(jsonfile, 'x')as obj:
                            json.dump(artist_obj, obj, indent=4)
                        imported.append(file)

                        print(">>\t" + bcolors.OKGREEN + "Artist \'" + name + "\' imported" + bcolors.ENDC)
                    else:
                        print(">>\t" + bcolors.WARNING + "Artist \'" + name + "\' entry already exists. Skipping..." + bcolors.ENDC)                    

                except SpoticryRuntimeError:
                    print(">> ")
                except:
                    print(">> " + bcolors.WARNING + "WARNING: Error parsing artists.txt list, clearing text file and resuming..." + bcolors.ENDC)
    
            file.truncate(0) 

        print(">> " + bcolors.BOLD + bcolors.OKGREEN + "Artists imported" + bcolors.ENDC)         

    # Return to open.spotify.com
    def home(self):
        self.dClick(self.site['sidebarNav']['homeButton']) 

    # Returns to the previous page
    def navBack(self):
        self.dClick(self.site['homeNav']['navBack'])    

    # Toggle shuffle feature on/off
    def toggleShuffle(self):
        self.dClick(self.site['songControls']['shuffleButton'])  

    # Toggle repeat between off/queue/song repeat
    def toggleRepeat(self):
        self.dClick(self.site['songControls']['repeatButton'])      

    # Toggle mute button
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

    # Opens queue view
    def openQueue(self):
        self.dClick(self.site['songControls']['queueButton'])

    # Opens Spotify object specified through url
    def openObject(self, url):
        self.web.get(url)
        self.dSleep()

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

        with open("src/spoticry__playlists.json", "r+") as jsonfile:
            filedata = json.load(jsonfile)
            url = self.web.current_url

            playlist_object = {
                "title": title,
                "url": url,
                "author": self.user['user'],
                "priority": 3
            }

            filedata["playlists"].append(playlist_object)
            jsonfile.seek(0)

        self.home()

    # Toggles play/pause for playlists
    def playPausePlaylist(self):
        self.dClick(self.site['playlistNav']['playlistPlayPause'])

    def playPauseAlbum(self):
        self.dClick(self.site['albumNav']['albumPlayPause'])    

    # Likes playlist
    def likePlaylist(self):
        if (self.exists(self.site['playlistNav']['playlistLike_F'])):
            self.dClick(self.site['playlistNav']['playlistLike_F'])
        else:
            print(">> \t" + bcolors.WARNING + "Playlist already liked. Continuing..." + bcolors.ENDC)      

    # Toggles like on playlist
    def toggleLikePlaylist(self):
        if (self.exists(self.site['playlistNav']['playlistLike_F'])):
            self.dClick(self.site['playlistNav']['playlistLike_F'])
        elif (self.exists(self.site['playlistNav']['playlistLike_T'])):
            self.dClick(self.site['playlistNav']['playlistLike_T'])    
        else:
            print(">> \t" + bcolors.WARNING + "Unable to perform operation under toggleLikePlaylist()" + bcolors.ENDC)    

    # Selects random playlist
    def selectPlaylist(self):
        print(">> UNDER CONSTRUCTION - selectPlaylist()")
        raise SpoticryRuntimeError

    # Searches for playlist based on one of the input parameters
    def searchPlaylist(self, title, author, priority):
        if title is not None:
            with open('src/spoticry__playlists.json', 'r') as file:
                data = json.load(file)
                playlists = data['playlists']

                for playlist in playlists:
                    if title == playlist['title']:
                        return playlist
        elif author is not None:
            with open('src/spoticry__playlists.json', 'r') as file:
                data = json.load(file)
                playlists = data['playlists']

                for playlist in playlists:
                    if author == playlist['author']:
                        return playlist  
        elif priority is not None:
            with open('src/spoticry__playlists.json', 'r') as file:
                data = json.load(file)
                playlists = data['playlists']

                results = []

                for playlist in playlists:
                    if priority == playlist['priority']:
                        results.append(playlist)
                    return results             


def openUser():
    try:
        file_ = random.choice(os.listdir('src/resources/users/inactive'))
        filename = utils.select_file('src/resources/users/inactive/' + file_)
        movedir = filename.replace("inactive", "active")    
        shutil.move(filename, movedir)        

        with open(movedir, "r+") as file:
            user = json.load(file)

        return user    
    except Exception as E:
        print(E)
        sys.exit()

def quarantineUser(userpath):       
    try:
        filename = utils.select_file(userpath)
        movedir = filename.replace("active", "quarantine")    
        shutil.move(filename, movedir)        

        with open(movedir, "r+") as file:
            user = json.load(file)

        return user    
    except Exception as E:
        print(E)
        sys.exit()       

def selectSpotifyObject(objectname):
    priority = utils.selectPriority(1)
    if "playlist" in objectname:
        parentdir = 'src/resources/playlists/' + priority + '/'
        filename = random.choice(os.listdir(parentdir))    
        obj_dir = parentdir + filename

        with open(obj_dir, "r+") as file:
            playlist = json.load(file)

        return playlist

    elif "song" in objectname:
        print(">> " + bcolors.WARNING + "ATTENTION: Selecting a song loads the album associated with the song" + bcolors.ENDC)
        parentdir = 'src/resources/songs/' + priority + '/'
        filename = random.choice(os.listdir(parentdir))    
        obj_dir = parentdir + filename

        with open(obj_dir, "r+") as file:
            song = json.load(file)

        return song

    elif "album" in objectname:
        parentdir = 'src/resources/albums/' + priority + '/'
        filename = random.choice(os.listdir(parentdir))    
        obj_dir = parentdir + filename

        with open(obj_dir, "r+") as file:
            album = json.load(file)

        return album 

    elif "user" in objectname:
        parentdir = 'src/resources/spotify-users/' + priority + '/'
        filename = random.choice(os.listdir(parentdir))    
        obj_dir = parentdir + filename

        with open(obj_dir, "r+") as file:
            user = json.load(file)

        return user 

    elif "artist" in objectname:
        parentdir = 'src/resources/artists/' + priority + '/'
        filename = random.choice(os.listdir(parentdir))    
        obj_dir = parentdir + filename

        with open(obj_dir, "r+") as file:
            user = json.load(file)

        return user  
        
    print(">> " + bcolors.FAIL + "ERROR: Unable to parse input" + bcolors.ENDC)
    raise SpoticryRuntimeError()        

def newinstance(user):

    record = utils.startProcess()

    user = {
        "email": "me@rengland.org",
        "user": "spoticry",
        "pass": "!8192Rde",
        "proxy": {
            "ip": "45.72.40.194:9288",
            "country": "US"
        }
    }

    # Debug grab random user
    # user = openUser()

    # Create sitemap and trigger objects for webdriver
    site = utils.get_sitemap()

    # Initialization 
    test = userinstance(user, site)

    try:
        # Song Controller (bottom panel) 
        #
        # test.playPause()  
        # test.skipBack()
        # test.skipForward()
        # test.toggleShuffle()
        # test.toggleRepeat()
        # test.toggleMute()
        # test.openQueue()

        # Sidebar Controller
        #
        # test.createPlaylist("hi from selenium!","a test playlist generated with selenium", utils.absolutePath(utils.fetch_image(1)))     Functional
        # test.home()
        # test.search()
        # test.library()
        # test.likedSongs()
        # test.getPlaylists()
        # test.importPlaylists()
        # test.importAlbums()
        # test.importArtists()

        test.recursiveScrape()

        raise SpoticryRuntimeError()

        test.home()

        # Test loop
        loginTime = utils.randomTimeDelta(180, 300)

        while time.time() < loginTime:
            taskTime = utils.randomTimeDelta(3, 5)
            playlist = test.selectPlaylist()
            while time.time() < taskTime:
                test.openPlaylist(playlist['url'])
                test.playPausePlaylist()
                time.sleep(taskTime - time.time() + 1)

        test.web.quit()

    except NoSuchElementException as E:
        print(E)
    except AttributeError as E:
        print(E)    
    except json.JSONDecodeError as E:
        print(E)    
    except SpoticryRuntimeError:
        print(">> ")
    except Exception as E:
        print(E)     
           
    test.shutdown()
    utils.peakMemory(record)


if __name__ == "__main__":
    newinstance(None)   