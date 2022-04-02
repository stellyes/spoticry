import os
import sys
import time
import json
import string
import requests
import pyautogui

from time import sleep
from random import choice as rc
from random import randint as ri
from random import uniform as rf
from requests import HTTPError 

pyautogui.FAILSAFE = True
PROXY_USER = 'spoticrier'
PROXY_PASS = 'kdsg3n5k6bbm02hnkc9sy789'

class dob:
    def __init__(self, month, day, year):
        self.month = month
        self.day = day
        self.year = year

def wait(interval=0):
    if interval == 0:
        sleep(ri(2, 6))
    else:
        sleep(interval)

def scroll(interval=-100):
    if interval != -100:
        for s in range(3):
            pyautogui.scroll(interval)
            sleep(0.5)
        wait()
    else:
        for s in range(3):
            pyautogui.scroll(interval)
            sleep(0.5)
        wait()        

def exists(window):
    try:
        pyautogui.locateCenterOnScreen(window)
        return True
    except:
        return False    


def emailInit(email):
    r = requests.post(
        "https://mailsac.com/api/addresses/" + email,
        headers={
            "Mailsac-Key": 'k_kVsKS05Xl5TcgdfjUSLlnU0N4ivDr9wf404',
            "forward": "accounts@rengland.org"
        }
    )

    try:
        r.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP request failed \"dev/email\": {http_err}')

    data = json.loads(r.text)
    return data    

def select_entry(filename):
    '''
    Selects random string from random line in text document
    '''
    with open(filename, "r") as doc:
        text = doc.read()
        words = list(map(str, text.split()))
    doc.close()
    return rc(words)

def generate_password(length):
    '''
    Random password generator of length provided
    '''
    charset = string.ascii_letters + string.digits + '!#@&^*()<>?'
    password = ''.join(rc(charset) for i in range(length))
    return password    

def generate_username():
    '''
    Random username generator
    '''

    markers = [0, 0, 0, 0]          # Markers used to prevent duplicate entries
    op0 = ri(0, 99)         # appended numbers to username
    op1 = ''                        # first name options
    op2 = ''                        # last name options
    op3 = ''                        # random word from words list
    username = ''                   # empty username string

    for i in range(2):
        # Get random marker
        username_order = ri(0, 3)

        # If marker indicates the choice has already been made
        if (markers[username_order] == 1):
            if username_order == 3:                 # If polled int is 3, wrap around to 0
                username_order = 0
            else:
                username_order = username_order + 1  # If polled int is < 3, increment

        if username_order == 0:
            markers[0] = 1
            username = username + str(op0)
        elif username_order == 1:
            markers[1] = 1
            op1 = select_entry("resources/data/fname.txt")
            username = username + op1
        elif username_order == 2:
            markers[2] = 1
            op2 = select_entry("resources/data/lname.txt")
            username = username + op2
        elif username_order == 3:
            markers[3] = 1
            op3 = select_entry("resources/data/words.txt")

            # If length of string is unreasonably long, reselect
            while len(op3) > 8:
                op3 = select_entry("resources/data/words.txt")
            username = username + op3

    return username 
    
def get_proxy():
    '''
    Pick random proxy server in directorty
    '''  
    root = 'resources/proxies/'  
    file = rc(os.listdir(root))                   
    country = root + file
    proxy = select_entry(country)
    parsed_country = file[:-4]

    coordinatefile = 'resources/coordinates/' + file 
    with open(coordinatefile, "r") as cf:
        lines = cf.readlines()
        coordinates = rc(lines).strip('\n')

    return { "ip": proxy, "country": parsed_country, "coordinates": coordinates }    

def getUser():

    print(">> Gathering username and proxy details")
    
    # Random elements initialized
    password_length = ri(8, 16)
    dob_month = ri(1, 11)
    dob_day = ri(1, 28)
    dob_year = ri(1982, 2006)
    
    username = generate_username()                                  # Generate username from text file input
    email = username + '@mailsac.com'                               # Generate temp email address
    charset = string.ascii_letters + string.digits + '!#@&^*()<>?'  # Gather charset for passwords
    password = ''.join(rc(charset) for i in range(password_length)) # Generate random password
    birthday = dob(dob_month, dob_day, dob_year)                    # Generate random birthday
    gender = ri(0, 2)                                               # Generate random gender selection
    proxy = get_proxy()                                             # Fetch proxy from random file


    print(">> Credentials for " + username + " generated")

    # Create spotifyUser dictionary
    user = {
        "email": email,
        "user": username,
        "pass": password,
        "dob": {
            "day": birthday.day,
            "month": birthday.month,
            "year": birthday.year
        },
        "gender": gender,
        "proxy": proxy,
        "status": 0
    }    

    return user

def proxySignIn():
    pyautogui.typewrite(PROXY_USER, interval=round(rf(0.25, 0.6), 2))
    wait()
    pyautogui.press('tab')
    pyautogui.typewrite(PROXY_PASS, interval=round(rf(0.25, 0.6), 2))
    wait()
    pyautogui.press('tab')
    wait()
    pyautogui.press('enter') 
        
def defineProxy(proxy):
    # Parse proxy into [ip address] and [port] segments
    ip, port = proxy.split(':')    
    wait(2)

    # Open firefox settings menu
    print(">> Updating proxy settings")
    print(">>\tOpening settings menu")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-settings.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=4)
    pyautogui.click()
    wait(1)   

    # Click 'settings'
    print(">>\tClicking 'settings'")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-settings-button.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=2)
    pyautogui.click()
    wait(1)
    
    # Search for proxy settings
    print(">>\tSearching for proxy settings")
    pyautogui.typewrite('proxy', interval=round(rf(0.25, 0.6), 2))
    wait(1)
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-proxy-settings.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=2)
    pyautogui.click()
    wait(1)

    # Input proxy and port
    print(">>\tTyping proxy IP")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/manual-proxy-config.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=1)
    pyautogui.click() 
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-http-proxy-config.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=1)
    pyautogui.click()
    pyautogui.press('backspace', presses=7)
    pyautogui.typewrite(ip, interval=round(rf(0.25, 0.6), 2))
    print(">>\tTyping proxy port")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-http-port-config.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=1)
    pyautogui.click()
    pyautogui.press('backspace', presses=1)
    pyautogui.typewrite(port, interval=round(rf(0.25, 0.6), 2))
    wait(1)

    # Save proxy settings
    print(">>\tSaving proxy settings")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-save-proxy-config.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=1)
    pyautogui.click()
    wait(60)

    proxySignIn()

    print(">>\tPriming URL bar for text input")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-proxy-settings-url-bar.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=1)
    pyautogui.click()
    wait(1)

def clearProxy():
    # Open firefox settings menu
    print(">> Clearing proxy settings")
    print(">>\tOpening settings menu")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-settings.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=4)
    pyautogui.click()
    wait(1)   

    # Click 'settings'
    print(">>\tClicking 'settings'")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-settings-button.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=2)
    pyautogui.click()
    wait(1)
    
    # Search for proxy settings
    print(">>\tSearching for proxy settings")
    pyautogui.typewrite('proxy', interval=round(rf(0.25, 0.6), 2))
    wait(1)
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-proxy-settings.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=2)
    pyautogui.click()
    wait(1)

    # Clearing proxy settings
    print(">>\tClearing proxy data")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-http-proxy-config.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=1)
    pyautogui.click()
    pyautogui.press('backspace', presses=15)
    pyautogui.typewrite('0.0.0.0', interval=round(rf(0.25, 0.6), 2))
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-http-port-config.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=1)
    pyautogui.click()
    pyautogui.press('backspace', presses=4)
    pyautogui.press('1')
    wait(1)

    print(">>\tSaving proxy settings")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-save-proxy-config.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=1)
    pyautogui.click()
    wait(2)

def changeLocation(coordinates):
    print(">> Changing WiFi URI Location")
    print(">> Navigating to settings")
    pyautogui.typewrite("about:config")
    pyautogui.typewrite(['enter'])
    wait()

    print(">> Clearing risk barrier")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-caution-config.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=1)
    pyautogui.click()
    wait()

    pyautogui.typewrite("geo.wifi.uri", interval=round(rf(0.25, 0.6), 2))
    wait()

    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-edit-wifi-geo-config.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=1)
    pyautogui.click()
    wait()

    lat, lon = coordinates.split(', ')
    locationinfo = 'data:application/json,{"location": {"lat": ' + lat + ', "lng": ' + lon + '}, "accuracy": 27000.0}'
    pyautogui.typewrite(locationinfo, interval=round(rf(0.25, 0.6), 2))
    pyautogui.typewrite(['enter'])
    wait()

    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-location-settings-url-bar.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=1)
    pyautogui.click()
    wait()


def main():

    print(">> Generating user data")
    user = getUser()

    # Locate and open Firefox
    print(">> Locating Firefox logo")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefoxHomeScreen.png", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.doubleClick()
    wait()

    defineProxy(user['proxy']['ip'])
    changeLocation(user['proxy']['coordinates'])

    # Go to Spotify signup page
    print(">> Opening sign-up url")
    pyautogui.typewrite('spotify.com/' + user['proxy']['country'].lower() + '/signup', interval=round(rf(0.25, 0.6), 2))
    pyautogui.typewrite(['enter'])
    wait()

    # Attempt to maximize window
    print(">> Maximizing window")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-maximize.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=2)
    pyautogui.click()
    wait()        

    # Fill email
    print(">> Filling email entry")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/spotify_com-email_entry.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(1)
    pyautogui.typewrite(user['email'], interval=round(rf(0.25, 0.6), 2))
    wait()

    # Fill email confirmation
    print(">> Filling email confirmation entry")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/spotify_com-email_confirm.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(1)
    pyautogui.typewrite(user['email'], interval=round(rf(0.25, 0.6), 2))
    wait()

    # Navigate down
    scroll()

    # Fill password
    print(">> Filling password entry")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/spotify_com-password_entry.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(1)
    pyautogui.typewrite(user['pass'], interval=round(rf(0.25, 0.6), 2))

    # Fill username
    print(">> Filling username entry")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/spotify_com-username_entry.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(1)
    pyautogui.typewrite(user['user'], interval=round(rf(0.25, 0.6), 2))
    wait()

    # Navigate down
    scroll()

    # Fill month
    print(">> Filling month entry")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/spotify_com-month_dropdown.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(1)

    mo_dir = "img/months/" + str(user['dob']['month']) + ".PNG"
    ffx, ffy = pyautogui.locateCenterOnScreen(mo_dir, confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=2)
    pyautogui.click()
    wait()

    # Fill day
    print(">> Filling day entry")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/spotify_com-birthday_day_entry.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(1)
    pyautogui.typewrite(str(user['dob']['day']), interval=round(rf(0.25, 0.6), 2))
    wait()

    # Fill year
    print(">> Filling year entry")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/spotify_com-birthday_year_entry.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(1)
    pyautogui.typewrite(str(user['dob']['year']), interval=round(rf(0.25, 0.6), 2))
    wait()

    # Navigate down
    scroll()

    # Click gender
    print(">> Filling gender entry")

    if user['gender'] == 0:
        gendir = "img/spotify_com-gender_entry-male.PNG"
    else:
        gendir = "img/spotify_com-gender_entry-female.PNG"     

    ffx, ffy = pyautogui.locateCenterOnScreen(gendir, confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=2)
    pyautogui.click()
    wait()

    # Click registration data
    print(">> Filling registration data")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/spotify_com-marketing_info.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=2)
    pyautogui.click()
    wait()

    # Navigate down
    scroll()

    # Click captcha
    print(">> Filling captcha")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/spotify_com-captcha_box.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=2)
    pyautogui.click()
    wait()

    print(">> Signing up")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/spotify_com-sign_up_button.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(30)

    clearProxy()

    # Return firefox to windowed view
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-windowed.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=1)
    pyautogui.click()
    wait()

    # Close window
    print(">> Closing Firefox")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-close.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=2)
    pyautogui.click()

    print(">> Registering Mailsac email")
    emailInit(user['email'])

    print(user)

if __name__ == "__main__":
    start = time.time()
    print(">> Starting script, Session #" + str(start))
    logfile = "logs/session" + str(start) + ".txt"
    sys.stdout = open(logfile, 'w')

    try:
        ffx, ffy = pyautogui.locateCenterOnScreen("img/python-minimize.PNG", confidence=0.8)
        pyautogui.moveTo(ffx, ffy)
        pyautogui.click()
        main()
    except TypeError as E:
        print(">> ERROR: Unable to find element on screen")
        print(E)
        print("UPTIME: %s" % (time.time() - start))
        os.system("pause") 
    except Exception as E:
        print(E)
        print("UPTIME: %s" % (time.time() - start))
        os.system("pause")   