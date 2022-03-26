import os
import sys
import time
import json
import requests
import pyautogui

from time import sleep
from random import randint as ri
from requests import HTTPError 


pyautogui.FAILSAFE = True

def wait(interval=0):
    if interval == 0:
        sleep(ri(2, 6))
    else:
        sleep(interval)

def scroll():
    for s in range(3):
        pyautogui.scroll(-100)
        sleep(0.5)
    wait()    

def emailInit(email):
    r = requests.post( 
        "https://9g8yajiqsg.execute-api.us-west-2.amazonaws.com/dev/email",
        headers= {
            "apikey": "k_kVsKS05Xl5TcgdfjUSLlnU0N4ivDr9wf404",
            "email": email
        }
    )

    try:
        r.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP request failed \"dev/email\": {http_err}')

    data = json.loads(r.text)
    return data.get('response')    


def getUser():

    r = requests.post( "https://9g8yajiqsg.execute-api.us-west-2.amazonaws.com/dev/user/data" )
    
    try:
        r.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP request failed \"dev/user/data\": {http_err}') 

    data = json.loads(r.text)
    user = data.get('body')

    r = requests.post( 
        "https://9g8yajiqsg.execute-api.us-west-2.amazonaws.com/dev/user", 
        headers={
            'username': user['username'],
            'proxy': json.dumps(user['proxy'])        
        } 
    )

    try:
        r.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP request failed \"dev/user\": {http_err}')    

    data = json.loads(r.text)
    user = data.get('body')    

    return user

def main():

    print(">> Generating user data")
    user = getUser()

    print(">> Creating Mailsac email")
    response = emailInit(user['email'])
    if response != 200:
        print(">> Failed to initialize email in Mailsac servers...")
        os.system("pause")
        sys.exit()

    # Locate and open Firefox
    print(">> Locating Firefox logo")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefoxHomeScreen.png", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.doubleClick()
    wait()

    # Go to Spotify signup page
    print(">> Opening sign-up url")
    pyautogui.typewrite('spotify.com/' + user['proxy']['country'].lower() + '/signup', interval=1)
    pyautogui.typewrite(['enter'])
    wait()

    # Fill email
    print(">> Filling email entry")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/spotify_com-email_entry.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(1)
    pyautogui.typewrite(user['email'], interval=1)
    wait()

    # Fill email confirmation
    print(">> Filling email confirmation entry")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/spotify_com-email_confirm.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(1)
    pyautogui.typewrite(user['email'], interval=1)
    wait()

    # Navigate down
    scroll()

    # Fill password
    print(">> Filling password entry")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/spotify_com-password_entry.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(1)
    pyautogui.typewrite(user['password'], interval=1)

    # Fill username
    print(">> Filling username entry")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/spotify_com-username_entry.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(1)
    pyautogui.typewrite(user['username'], interval=1)
    wait()

    # Navigate down
    scroll()

    # Fill month
    print(">> Filling month entry")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/spotify_com-month_dropdown.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(1)

    mo_dir = "img/months" + str(user['dob']['month']) + ".PNG"
    try:
        ffx, ffy = pyautogui.locateCenterOnScreen(mo_dir, confidence=0.8)
    except:
        scroll()    
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
    pyautogui.typewrite(str(user['dob']['day']), interval=1)
    wait()

    # Fill year
    print(">> Filling year entry")
    ffx, ffy = pyautogui.locateCenterOnScreen("img/spotify_com-birthday_year_entry.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=3)
    pyautogui.click()
    wait(1)
    pyautogui.typewrite(str(user['dob']['year']), interval=1)
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
    #ffx, ffy = pyautogui.locateCenterOnScreen("img/spotify_com-sign_up_button.PNG", confidence=0.8)

    # Close window
    ffx, ffy = pyautogui.locateCenterOnScreen("img/firefox-close.PNG", confidence=0.8)
    pyautogui.moveTo(ffx, ffy, duration=2)
    pyautogui.click()

if __name__ == "__main__":
    start = time.time()

    logfile = "logs/session" + str(start) + ".txt"
    sys.stdout = open(logfile, 'w')

    try:
        print(">> Starting script, Session #" + str(start))
        ffx, ffy = pyautogui.locateCenterOnScreen("img/python-minimize.PNG", confidence=0.8)
        pyautogui.moveTo(ffx, ffy)
        pyautogui.click()
        
        main()

    except Exception as E:
        print(E)
        print("UPTIME: %s" % (time.time() - start))
        os.system("pause")