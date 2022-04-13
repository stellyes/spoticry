import os
import time
import json
import string
import platform
import requests
import pyautogui

from time import sleep
from random import choice as rc
from random import randint as ri
from random import uniform as rf
from requests import HTTPError 

pyautogui.FAILSAFE = True
CODE = ['AU', 'CA', 'DE', 'ES', 'FI', 'FR', 'IT', 'NL', 'NO', 'SE', 'UA', 'UK', 'US']
VPN = ['Australia', 'Canada', 'Germany', 'Spain', 'Finland',
       'France', 'Italy', 'Netherlands', 'Norway', 'Sweden',
       'Ukraine', 'United Kingdom', 'United States']

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
        words = list(map(str, text.split('\n')))
    doc.close()
    return rc(words)

def generate_password(length):
    '''
    Random password generator of length provided
    '''
    charset = string.ascii_letters + string.digits + '!#@&^*()<>?'
    password = ''.join(rc(charset) for i in range(length))
    return password    

def vpn_connect(country):
    '''
    Connects to server with corresponding country location
    '''
    command = "nordvpn -c -g '" + country
    os.system(command)
    wait(15)

def vpn_disconnect():
    '''
    Disconnects from NordVPN server
    '''
    command = "nordvpn -d"
    os.system(command)
    wait(15)

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
    
def get_location():
    '''
    Pick random location in directorty
    '''  
    root = 'resources/coordinates/'  
    file = rc(os.listdir(root))                   
    country = root + file
    coordinates = select_entry(country)
    parsed_country = VPN[CODE.index[file[:-4]]]

    return { "country": parsed_country, "coordinates": coordinates }    

def getUser():

    print(">> Generating user credentials")
    
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
    useragent = select_entry("resources/data/useragents.txt")       # Fetch random user agent from list
    vpn = get_location()                                            # Fetch location information


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
        "useragent": useragent,
        "location": vpn,
        "status": 0
    }    

    print(user)
    return user

def changeLocation(coordinates):
    print(">> Changing geo provider")
    print(">>\tNavigating to settings")
    pyautogui.typewrite("about:config")
    pyautogui.typewrite(['enter'])
    wait(1)

    print(">>\tClearing risk barrier")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-caution-config.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy)
    pyautogui.click()
    wait(1)

    print(">>\tLocating provider")
    pyautogui.typewrite("geo.provider.network.url")
    wait(1)

    print(">>\tEditing...")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-edit-wifi-geo-config.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy)
    pyautogui.click()
    wait(1)

    print(">>\tParsing and entering coordinates")
    lat, lon = coordinates.split(', ')
    locationinfo = 'data:application/json,{"location": {"lat": ' + lat + ', "lng": ' + lon + '}, "accuracy": 27000.0}'
    pyautogui.typewrite(locationinfo)
    pyautogui.typewrite(['enter'])
    wait(1)

    print(">>\tSaving geo provider settings")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-location-settings-url-bar.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy)
    pyautogui.click()
    wait(1)

def changeUserAgent(useragent):
    print(">> Changing user agent")
    print(">>\tNavigating to settings")
    pyautogui.typewrite("about:config")
    pyautogui.typewrite(['enter'])
    wait()

    print(">>\tClearing risk barrier")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-caution-config.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy)
    pyautogui.click()
    wait(1)

    print(">>\tLocating user agent definition")
    pyautogui.typewrite("general.useragent.override")
    wait(1)

    print(">>\tEditing...")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-edit-wifi-geo-config.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy)
    pyautogui.click()
    wait(1)

    print(">>\tEntering user agent information")
    pyautogui.typewrite(useragent)
    pyautogui.typewrite(['enter'])
    wait(1)

    print(">>\tSaving user agent settings")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-useragent-settings-url-bar.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy)
    pyautogui.click()
    wait(1)

def main():

    print(">> Generating user data")
    user = getUser()

    # Locate and open Firefox
    print(">> Locating Firefox logo")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefoxHomeScreen.png", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=1)
    pyautogui.doubleClick()
    wait()

    # Hide browser/device from websites
    vpn_connect(user['proxy']['country'])
    changeLocation(user['proxy']['coordinates'])
    changeUserAgent(user['useragent'])

    # Go to Spotify signup page
    print(">> Opening sign-up url")
    pyautogui.typewrite('spotify.com/' + user['proxy']['country'].lower() + '/signup')
    pyautogui.typewrite(['enter'])
    wait()

    # Attempt to maximize window
    #print(">> Maximizing window")
    #ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-maximize.PNG", confidence=0.8)
    #pyautogui.moveTo(ffx, ffy, duration=2)
    #pyautogui.click()
    #wait()        

    # Fill email
    print(">> Filling email entry")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/spotify_com-email_entry.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(1)
    pyautogui.typewrite(user['email'], interval=round(rf(0.15, 0.4), 2))
    wait()

    # Fill email confirmation
    print(">> Filling email confirmation entry")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/spotify_com-email_confirm.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(1)
    pyautogui.typewrite(user['email'], interval=round(rf(0.15, 0.4), 2))
    wait()

    # Navigate down
    scroll()

    # Fill password
    print(">> Filling password entry")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/spotify_com-password_entry.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(1)
    pyautogui.typewrite(user['pass'], interval=round(rf(0.15, 0.4), 2))

    # Fill username
    print(">> Filling username entry")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/spotify_com-username_entry.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(1)
    pyautogui.typewrite(user['user'], interval=round(rf(0.15, 0.4), 2))
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
    pyautogui.typewrite(str(user['dob']['day']), interval=round(rf(0.15, 0.4), 2))
    wait()

    # Fill year
    print(">> Filling year entry")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/spotify_com-birthday_year_entry.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(1)
    pyautogui.typewrite(str(user['dob']['year']), interval=round(rf(0.15, 0.4), 2))
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
    try:
        ffx, ffy = pyautogui.locateCenterOnScreen("img/spotify_com-marketing_info.PNG", confidence=0.8)
        pyautogui.moveTo(ffx, ffy, duration=2)
        pyautogui.click()
        wait()
    except:
        ffx, ffy = pyautogui.locateCenterOnScreen("img/spotify_com-eea.PNG", confidence=0.8)
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

    vpn_disconnect()

    print(">> Registering Mailsac email")
    emailInit(user['email'])

    print(user)

if __name__ == "__main__":
    print(">>\n>> PLEASE ENSURE THE FOLLOWING SETTINGS ARE ADJUSTED:")
    print(">>\t'about:config' ==> 'general.useragent.override' is initialized")
    print(">>\t'about:config' ==> 'geo.provider.ms-windows-location' ==> 'false'")
    print(">>\t'about:config' ==> 'geo.enabled' ==> 'false'")
    os.system("pause")
    
    start = time.time()
    #print(">> Starting script, Session #" + str(start))
    #logfile = "logs/session" + str(start) + ".txt"
    #sys.stdout = open(logfile, 'w')

    try:
        #ffx, ffy = pyautogui.locateCenterOnScreen("img/python-minimize.PNG", confidence=0.8)
        #pyautogui.moveTo(ffx, ffy)
        #pyautogui.click()
        main()
    except TypeError as E:
        print(">> ERROR: Unable to find element on screen")
        print(E)
        print("UPTIME: %s" % (time.time() - start))
        os.system("pause") 

    print("UPTIME: %s" % (time.time() - start))
    os.system("pause")   