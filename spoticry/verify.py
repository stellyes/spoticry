import os
import sys
import time
import json
import random
import spoticore
from requests import HTTPError
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas

import twocaptcha


# Solve and Verify captcha using 2Captcha API
    #
    # Refer to https://github.com/2captcha/2captcha-python documentation
    # for explanation of this. Frankly, idfk what this does but the 
    # code doesn't work without it. 

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


API_KEY = 'cfdd1e0dafb83224e79a5ade1e9191a9'
API_URL = 'https://2captcha.com/in.php?'
REQ_URL_US = 'https://www.spotify.com/us/signup'
REQ_URL_UK = 'https://www.spotify.com/uk/signup'
REQ_URL_TR = 'https://www.spotify.com/tr/signup'

WEBDRIVER = 'src/webdriver/chromedriver.exe'


def sign_up(user):
    # Handles sign-up process using generated user info

    # Selecting and assigning proxy
    #proxy = user['proxy']['ip']

    chrome_options = webdriver.ChromeOptions()                  # Options argument initalization
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    #chrome_options.add_argument('--proxy-server=%s' % proxy)   # Assigns proxy
    chrome_options.add_argument('--headless')  
    chrome_options.add_argument('log-level=3')                 # Specifies GUI display, set to headless (NOGUI)

    # Uncomment when debugging is complete

    # Use Google Chrome webdriver to handle form filling      
    web = webdriver.Chrome(
        service=Service('src/webdriver/chromedriver.exe'), 
        options=chrome_options
        ) 

    # Open Spotify sign-up URL via webdriver
    web.get(REQ_URL_US)
    print(">>\t Loading webpage")
    time.sleep(2)

    # Grab relevant recaptchaCheckboxKey from spotify signup page
    proplist = []
    props = web.find_elements(By.XPATH, '//*[@id="__NEXT_DATA__"]')
    for prop in props:
        proplist.append(prop.text)
        
    print(proplist)    
    web.close()
    sys.exit()

    # Locate and fill email portion of form
    email_input = web.find_element('//*[@id="email"]')
    email_input.send_keys()
    time.sleep(random.randint(1, 9))

    # Locate and fill email confirmation portion of form
    email_confirmation_input = web.find_element('//*[@id="confirm"]')
    email_confirmation_input.send_keys()
    time.sleep(random.randint(1, 9))

    # Locate and fill password portion of form
    password_input = web.find_element('//*[@id="password"]')
    password_input.send_keys()
    time.sleep(random.randint(1, 9))

    # Locate and fill profile name portion of form
    username_input = web.find_element('//*[@id="displayname"]')
    username_input.send_keys()
    time.sleep(random.randint(1, 9))

    # Locate and fill month portion of form
    dob_month_input = web.find_element('//*[@id="month"]')
    dob_month_input.send_keys()
    time.sleep(random.randint(1, 9))

    # Locate and fill day portion of form
    dob_day_input = web.find_element('//*[@id="day"]')
    dob_day_input.send_keys()
    time.sleep(random.randint(1, 9))

    # Locate and fill year portion of form
    dob_year_input = web.find_element('//*[@id="year"]')
    dob_year_input.send_keys()
    time.sleep(random.randint(1, 9))

    # Locate and fill gender portion of form 
    gender = user['gender']

    if gender == 0:
        male = web.find_element('//*[@id="__next"]/main/div[2]/div/form/fieldset/div/div[1]/label/span[1]')
        male.send_keys()
    elif gender == 1:
        female = web.find_element('//*[@id="__next"]/main/div[2]/div/form/fieldset/div/div[2]/label/span[1]')
        female.send_keys()
    elif gender == 2:
        nonbinary = web.find_element('//*[@id="__next"]/main/div[2]/div/form/fieldset/div/div[3]/label/span[1]')
        nonbinary.send_keys()
    else:
        print(">> ERROR:\n>> Invalid gender input")

    time.sleep(random.randint(1, 9))    

    # Locate and fill marketing information portion of form
    if user['opt_in'] == 1:
        marketing_information = web.find_element('//*[@id="__next"]/main/div[2]/div/form/div[6]/div/label/span[1]')        
        marketing_information.send_keys()

    time.sleep(random.randint(1, 9))   

    # Solve and Verify captcha using 2Captcha API
    #
    # Refer to https://github.com/2captcha/2captcha-python documentation
    # for explanation of this. Frankly, idfk what this does but the 
    # code doesn't work without it. 
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    # Grab relevant recaptchaCheckboxKey from spotify signup page
    props = web.find_element('//*[@id="__NEXT_DATA__"]/text()')
    props = json.loads(props)
    print(json.dumps(props, indent=4)) 
    sys.exit()


def main():
    newUser = {
            "email": 'testemail@email.com',
            "user": 'testuser',
            "pass": 'testpass',
            "dob": {
                "day": 1,
                "month": 1,
                "year": 1900
            },
            "gender": 1,
            "opt_in": 1,
            "md5_hash": '16d86f132910b8368636bf625f232f37',
            "proxy": spoticore.get_proxy(),
            "verified": ''
     }

    sign_up(newUser)

if __name__ == "__main__":
    main()    
