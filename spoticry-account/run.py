import os
import time
import json
import string
import requests
import pyautogui

from pyautogui import FailSafeException

from nordvpn_connect import initialize_vpn
from nordvpn_connect import rotate_VPN as connect
from nordvpn_connect import close_vpn_connection as disconnect

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
        sleep(ri(8, 15))
    else:
        sleep(interval)

def country_convert(string):
    '''
    Returns corresponding index value from CODE and VPN lists
    '''        
    if string in CODE:
        index = CODE.index(string)
        return VPN[index]
    elif string in VPN:
        index = VPN.index(string)
        return CODE[index]
    else:
        print("Unable to determine index location for country " + string)    


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


def doublecheck(path):
    '''
    The application safe 'locate' function
    '''

    i = 1
    confidence_meter=0.8
    print("\n\t\t\tSearching for '" + path + "'\n")

    while confidence_meter > 0.35:
        try:
            ffx, ffy = pyautogui.locateCenterOnScreen(path, confidence=confidence_meter)
            wait(1)
            print("\t\t==> Attempt " + str(i) + " successful!")
            return ffx, ffy 
        except TypeError as E:
            print("\t\t==> Attempt " + str(i) + " unsuccessful...\tConfidence: %.2f" % confidence_meter)
            i += 1
            confidence_meter -= 0.05

    return 0, 0        


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
    settings = initialize_vpn(country)
    connect(settings)
    return settings

def generate_username():
    '''
    Random username generator
    '''

    markers = [0, 0, 0, 0]          # Markers used to prevent duplicate entries
    op0 = ri(0, 99)                 # appended numbers to username
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

    cc = file[:-4]
    i = CODE.index(cc)
    parsed_country = VPN[i]

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
        "dob-day": birthday.day,
        "dob-month": birthday.month,
        "dob-year": birthday.year,
        "gender": gender,
        "useragent": useragent,
        "country": vpn['country'],
        "coordinates": vpn['coordinates'],
        "status": 0
    }    

    return user

def changeLocation(coordinates):
    print(">> Changing geo provider")
    print(">>\tNavigating to settings")
    pyautogui.typewrite("about:config")
    pyautogui.typewrite(['enter'])
    wait(1)

    #print(">>\tClearing risk barrier")
    #ffx, ffy = doublecheck("img/firefox-caution-config.PNG")
    #pyautogui.moveTo(ffx, ffy)
    #pyautogui.click()
    #wait(1)

    print(">>\tLocating provider")
    pyautogui.typewrite("geo.provider.network.url")
    wait(1)

    print(">>\tEditing...")
    ffx, ffy = doublecheck("img/firefox-edit-wifi-geo-config.PNG")
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
    ffx, ffy = doublecheck("img/firefox-change-location-searchbar.png")
    pyautogui.moveTo(ffx, ffy)
    pyautogui.click()
    pyautogui.press('backspace', presses=24)
    wait(1)

def changeUserAgent(useragent):
    print(">> Changing user agent")
    print(">>\tLocating user agent definition")
    pyautogui.typewrite("general.useragent.override")
    wait(1)

    print(">>\tEditing...")
    ffx, ffy = doublecheck("img/firefox-edit-wifi-geo-config.PNG")
    pyautogui.moveTo(ffx, ffy)
    pyautogui.click()
    wait(1)

    print(">>\tEntering user agent information")
    pyautogui.typewrite(useragent)
    pyautogui.typewrite(['enter'])
    wait(1)

    print(">>\tSaving user agent settings")
    pyautogui.hotkey('ctrl', 'k')
    pyautogui.press('backspace', presses=5)     # Presses quantifier unnecessary, just cautionary measures
    wait(1)

def clearPrivacyCheck():
    '''
    Legacy Function:
    Clears privacy barriers
    '''    

    print(">> Clearing cookies/privacy window")
    try:
        ffx, ffy = doublecheck("img/spotify-accept-cookies.png")
        pyautogui.moveTo(ffx, ffy, duration=2)
        pyautogui.click()
        wait()
    except:
        try:
            ffx, ffy = doublecheck("img/spotify-privacy-accept.png")
            pyautogui.moveTo(ffx, ffy, duration=2)
            pyautogui.click()
            wait()
        except:
            print(">> Unable to clear cookies/privacy warning")

def maximize():
    # Attempt to maximize window
    print(">> Maximizing window")
    ffx, ffy = doublecheck("img/firefox-maximize.PNG", )
    pyautogui.moveTo(ffx, ffy, duration=2)
    pyautogui.click()
    wait()               

def main():

    print(">> Generating user data")
    user = getUser()

    # Locate and open Firefox
    print(">> Locating Firefox logo")
    ffx, ffy = doublecheck("img/firefoxHomeScreen.png")
    pyautogui.moveTo(ffx, ffy, duration=1)
    pyautogui.doubleClick()
    wait()

    # Hide browser/device from websites
    print(">>\n>>\t\t CONNECTING TO VPN\n>>")
    vpn = vpn_connect(user['country'])
    changeLocation(user['coordinates'])
    changeUserAgent(user['useragent'])

    # Go to Spotify signup page
    print(">> Opening sign-up url")
    country = country_convert(user['country'])
    pyautogui.typewrite('spotify.com/' + country.lower() + '/signup')
    pyautogui.typewrite(['enter'])
    wait()

    # Fill email
    print(">> Filling email entry")
    ffx, ffy = doublecheck("img/spotify_com-email_entry.PNG")
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(1)
    pyautogui.typewrite(user['email'], interval=round(rf(0.15, 0.4), 2))
    wait()

    # Fill email confirmation
    print(">> Filling email confirmation entry")
    ffx, ffy = doublecheck("img/spotify_com-email_confirm.PNG")
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(1)
    pyautogui.typewrite(user['email'], interval=round(rf(0.15, 0.4), 2))
    wait()

    # Navigate down
    scroll()

    # Fill password
    print(">> Filling password entry")
    ffx, ffy = doublecheck("img/spotify_com-password_entry.PNG")
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(1)
    pyautogui.typewrite(user['pass'], interval=round(rf(0.15, 0.4), 2))

    # Fill username
    print(">> Filling username entry")
    ffx, ffy = doublecheck("img/spotify_com-username_entry.PNG")
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(1)
    pyautogui.typewrite(user['user'], interval=round(rf(0.15, 0.4), 2))
    wait()

    # Navigate down
    scroll()

    # Fill month
    print(">> Filling month entry")
    ffx, ffy = doublecheck("img/spotify_com-month_dropdown.PNG")
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(1)

    mo_dir = "img/months/" + str(user['dob-month']) + ".PNG"
    ffx, ffy = doublecheck(mo_dir, )
    pyautogui.moveTo(ffx, ffy, duration=2)
    pyautogui.click()
    wait()

    # Fill day
    print(">> Filling day entry")
    ffx, ffy = doublecheck("img/spotify_com-birthday_day_entry.PNG")
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(1)
    pyautogui.typewrite(str(user['dob-day']), interval=round(rf(0.15, 0.4), 2))
    wait()

    # Fill year
    print(">> Filling year entry")
    ffx, ffy = doublecheck("img/spotify_com-birthday_year_entry.PNG")
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(1)
    pyautogui.typewrite(str(user['dob-year']), interval=round(rf(0.15, 0.4), 2))
    wait()

    # Navigate down
    scroll()

    # Click gender
    print(">> Filling gender entry")

    if user['gender'] == 0:
        gendir = "img/spotify_com-gender_entry-male.PNG"
    else:
        gendir = "img/spotify_com-gender_entry-female.PNG"     

    ffx, ffy = doublecheck(gendir, )
    pyautogui.moveTo(ffx, ffy, duration=2)
    pyautogui.click()
    wait()

    # Click registration data
    print(">> Filling registration data")
    try:
        ffx, ffy = doublecheck("img/spotify_com-marketing_info.PNG")
        pyautogui.moveTo(ffx, ffy, duration=2)
        pyautogui.click()
        wait()
    except:
        ffx, ffy = doublecheck("img/spotify_com-eea.PNG", )
        pyautogui.moveTo(ffx, ffy, duration=2)
        pyautogui.click()
        wait()    

    # Navigate down
    scroll()

    # Click captcha
    print(">> Filling captcha")
    ffx, ffy = doublecheck("img/spotify_com-captcha_box.PNG")
    pyautogui.moveTo(ffx, ffy, duration=2)
    pyautogui.click()
    wait()

    print(">> Signing up")
    ffx, ffy = doublecheck("img/spotify_com-sign_up_button.PNG")
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(30)

    # Return firefox to windowed view
    ffx, ffy = doublecheck("img/firefox-windowed.PNG")
    pyautogui.moveTo(ffx, ffy, duration=1)
    pyautogui.click()
    wait()

    # Close window
    print(">> Closing Firefox")
    ffx, ffy = doublecheck("img/firefox-close.PNG")
    pyautogui.moveTo(ffx, ffy, duration=2)
    pyautogui.click()

    disconnect(vpn)

    print(">> Registering Mailsac email")
    emailInit(user['email'])

    print(user)

def setup():
    print(">>\n>> PLEASE ENSURE THE FOLLOWING SETTINGS ARE ADJUSTED:")
    print(">>\tEnsure 'about:config' warning barrier is cleared")
    print(">>\tEnsure NordVPN is open and disconnected")
    print(">>\t'about:config' ==> 'general.useragent.override' is initialized")
    print(">>\t'about:config' ==> 'geo.provider.ms-windows-location' ==> 'false'")
    print(">>\t'about:config' ==> 'geo.enabled' ==> 'false'")
    os.system("pause")

    #print(">> Starting script, Session #" + str(start))
    #logfile = "logs/session" + str(start) + ".txt"
    #sys.stdout = open(logfile, 'w')

    try:
        ffx, ffy = doublecheck("img/python-minimize.PNG")
        pyautogui.moveTo(ffx, ffy)
        pyautogui.click()
        main()   
    except TypeError as E:
        print(">> ERROR: Unable to find element on screen")
        print(E)

if __name__ == "__main__":
    
    # Element blocker
    # https://addons.mozilla.org/en-US/firefox/addon/element-blocker/

    flag = 1
    start = time.time()

    if flag == 0:
        setup()
    else:
        try:
            main()
        except FailSafeException:
            print(">>\n>> Failsafe triggered. Exiting...\n>>")
    print(">> UPTIME: %s" % (time.time() - start))
    os.system("pause")   