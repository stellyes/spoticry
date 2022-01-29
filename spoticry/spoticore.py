import os
import sys
import time
import json
import utils
import string
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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException


START = "start"
RESUME = "resume"

BL_AUTHORS = ['Spotify']
BL_ARTISTS = ['Drake']

ACC_ACTIVE = 'src/resources/users/active'
ACC_INACTIVE = 'src/resources/users/inactive'
ACC_QUARANTINE = 'src/resources/users/quarantine'

AUTHORS = ['ryan', 'olivbeea']
ARTISTS = ['deo autem nihil', '18pm', '18PM', 'Exploitsound', 'exploitsound', 'BADTIME!', 'Ｏｃｅａｎ Ｓｈｏｒｅｓ']


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
    def __init__(self, user, site, state):
        # Options argument initalization
        chrome_options = webdriver.ChromeOptions()                

        # chrome_options.add_argument('--proxy-server=%s' % user['proxy']['ip'])                  # Assigns proxy
        # chrome_options.add_argument('--headless')                                             # Specifies GUI display, set to headless (NOGUI)
        chrome_options.add_argument("--mute-audio")                                             # Mute audio output
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])   # Disable pop-ups? maybe?
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])           # Disable all logging        


        if (state=="start"):
            print(">> " + bcolors.OKCYAN + "Initializing Webplayer instance..." + bcolors.ENDC)

            # Webdriver service object
            # webdriverChromeService = Service('src/webdriver/chromedriver.exe')

            # Assign user data and evaluate webdriver command via sitemap
            self.user = user
            self.site = site     
            self.web = eval(self.site['login']['webdriver'])

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

            # Attempt to gather cookies
            try:
                print(">> " + bcolors.OKCYAN + "Attempting to gather cookies from browser session..." + bcolors.ENDC)
                utils.makedir("src/resources/cookies/")
                cookie_dir = "src/resources/cookies/" + user['user'] + ".pk1"
                pickle.dump(self.web.get_cookies(), open(cookie_dir, "wb"))
                print(">> " + bcolors.OKCYAN + "Cookies successfully stored." + bcolors.ENDC)
            except:
                print(">> " + bcolors.WARNING + "Failed to gather cookies..." + bcolors.ENDC)    

    # Handles closing of webdriver instance
    def shutdown(self):
        print(">>\n>> Session ID: " + self.session_id + " | >> Execute URL: " + self.executor_url)

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
                    obj_name = title + ".json"
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
            return 0

    def importAlbums(self):
        print(">> " + bcolors.BOLD + bcolors.OKGREEN + "Importing albums..." + bcolors.ENDC)
        
        # Removes outdated version 
        if os.path.exists("src/spoticry__albums.json"):
            with open("src/spoticry__albums.json", "r+") as jsonfile:
                # Create object from file contents
                filedata = json.load(jsonfile)
                jsonfile.close()

        with open("src/resources/txt/albums.txt", "r+") as file:
            # Get lines containing album URLs
            lines = file.readlines()

            for line in lines:
                # Get album URL
                self.web.get(line)
                self.dSleep()

                title = self.web.find_element(By.XPATH, "//section[@data-testid='album-page']/div[1]/div[5]/span/h1").text
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
                pr = random.randint(1, 2)
                if artist in ARTISTS:
                    pr = 5

                url = self.web.current_url

                album_object = {
                    "title": title,
                    "url": url,
                    "artist": artist,
                    "priority": pr
                }

                print(">>\t" + bcolors.OKGREEN + "Album \'" + title + "\' imported" + bcolors.ENDC)

                if album_object not in filedata['playlists'][str(pr)]:
                    filedata['playlists'][str(pr)].append(album_object)
                else:
                    print(">>\t" + bcolors.WARNING + "Album \'" + title + "\' entry already exists. Skipping..." + bcolors.ENDC)    

                # Prevent temporary IP Ban
                time.sleep(30)    

        file.truncate(0)
        os.remove("src/spoticry__albums.json")
        
        with open("src/spoticry__albums.json", "x") as jsonfile:
            json.dumps(filedata, jsonfile, indent=4)

        print(">> " + bcolors.BOLD + bcolors.OKGREEN + "Albums imported" + bcolors.ENDC)

    # Imports list of playlists in storage file.
    def importPlaylists(self):
        print(">> " + bcolors.BOLD + bcolors.OKGREEN + "Importing playlists..." + bcolors.ENDC)

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
                    pr = random.randint(1, 2)
                    if author in AUTHORS:
                        pr = 5

                    url = self.web.current_url

                    try:
                        self.songScrape(0, title)
                    except:
                        raise SpoticryRuntimeError(">> ")

                    playlist_obj = {
                        "title": title,
                        "url": url,
                        "author": author,
                        "priority": pr
                    }
                    
                    playlist_object_directory = "src/resources/playlists/" + str(pr) + "/"
                    obj_name = title + ".json"
                    utils.makedir(playlist_object_directory)

                    if obj_name not in os.listdir(playlist_object_directory):
                        jsonfile = os.path.join(playlist_object_directory + obj_name)
                        with open(jsonfile, 'x')as obj:
                            json.dump(playlist_obj, obj, indent=4)

                        print(">>\t" + bcolors.OKGREEN + "Playlist \'" + title + "\' imported" + bcolors.ENDC)
                    else:
                        print(">>\t" + bcolors.WARNING + "Playlist \'" + title + "\' entry already exists. Skipping..." + bcolors.ENDC)    
                except SpoticryRuntimeError:
                    print(">> ")
                except:
                    print(">> " + bcolors.WARNING + "WARNING: Error parsing playlists.txt list, clearing text file and resuming..." + bcolors.ENDC)
    
            file.truncate(0)

        print(">> " + bcolors.BOLD + bcolors.OKGREEN + "Playlists imported" + bcolors.ENDC)
   
    # Return to open.spotify.com
    def home(self):
        self.dClick(self.site['sidebarNav']['homeButton']) 

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

    # Opens playlist specified through url
    def openPlaylist(self, url):
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

    # Option 0 - Unlike Playlist
    # Option 1 - Like Playlist
    def toggleLikePlaylist(self, option):
        if (self.exists(self.site['playlistNav']['playlistLike_F']) and option == 1):
            self.dClick(self.site['playlistNav']['playlistLike_F'])
        elif (self.exists(self.site['playlistNav']['playlistLike_T']) and option == 0):
            self.dClick(self.site['playlistNav']['playlistLike_T'])    
        else:
            print(">> \t" + bcolors.WARNING + "Unable to perform operation under toggleLikePlaylist()" + bcolors.ENDC)    

    # Selects random playlist
    def selectPlaylist(self):
        with open('src/spoticry__playlists.json', 'r') as file:
            data = json.load(file)
            playlists = data['playlists']

            pr = utils.selectPriority()
            if pr < 5:  # Temporary scale adjustor
                pr = 1

            results = []

            for playlist in playlists:
                if pr == playlist['priority']:
                    results.append(playlist)    

            index = random.randint(0, len(results)-1)

            return results[index]

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
        filename = utils.select_file('src/resources/users/inactive')
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

def newinstance(user):

    record = utils.startProcess()

    # Debug grab random user
    # user = openUser()
    user = {
        "email": "me@rengland.org",
        "user": "spoticry",
        "pass": "!8192Rde",
        "proxy": {
            "ip": "45.72.53.148:6184",
            "country": "US"
        }
    }

    # Create sitemap and trigger objects for webdriver
    site = utils.get_sitemap()

    # Initialization 
    test = userinstance(user, site, START)

    try:
        '''
        Quarantining:
            test.selectPlaylist()
        '''

        

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
        test.importPlaylists()
        # test.importAlbums()
    
        

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
        print(">> End of session")
    except Exception as E:
        print(E)     
           
    print(utils.peakMemory(record))
    test.web.quit()
if __name__ == "__main__":
    newinstance(None)   