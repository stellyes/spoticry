import sys
import time
import proxy 
import random
import requests
from hashlib import md5
from requests import HTTPError
from selenium import webdriver
import proxy as prox

API_KEY = 'cfdd1e0dafb83224e79a5ade1e9191a9'
API_URL = 'https://2captcha.com/in.php?'
REQ_URL = 'https://www.spotify.com/us/signup'


def sign_up(user):
    # Handles sign-up process using generated user info

    # Selecting and assigning proxy
    proxy = user['proxy']['ip']
    chrome_options = webdriver.ChromeOptions()               # Options argument initalization
    chrome_options.add_argument('--proxy-server=%s' % proxy) # Assigns proxy
    # Uncomment when debugging is complete
    # chrome_options.add_argument('--headless')                # Specifies GUI display, set to headless (NOGUI)

    # Use Google Chrome webdriver to handle form filling      
    web = webdriver.Chrome(options=chrome_options) 

    # Open Spotify sign-up URL via webdriver
    web.get(REQ_URL)
    time.sleep(15)

    # Locate and fill email portion of form
    email_input = web.find_element_by_xpath('//*[@id="email"]')
    email_input.send_keys()
    time.sleep(random.randint(1, 9))

    # Locate and fill email confirmation portion of form
    email_confirmation_input = web.find_element_by_xpath('//*[@id="confirm"]')
    email_confirmation_input.send_keys()
    time.sleep(random.randint(1, 9))

    # Locate and fill password portion of form
    password_input = web.find_element_by_xpath('//*[@id="password"]')
    password_input.send_keys()
    time.sleep(random.randint(1, 9))

    # Locate and fill profile name portion of form
    username_input = web.find_element_by_xpath('//*[@id="displayname"]')
    username_input.send_keys()
    time.sleep(random.randint(1, 9))

    # Locate and fill month portion of form
    dob_month_input = web.find_element_by_xpath('//*[@id="month"]')
    dob_month_input.send_keys()
    time.sleep(random.randint(1, 9))

    # Locate and fill day portion of form
    dob_day_input = web.find_element_by_xpath('//*[@id="day"]')
    dob_day_input.send_keys()
    time.sleep(random.randint(1, 9))

    # Locate and fill year portion of form
    dob_year_input = web.find_element_by_xpath('//*[@id="year"]')
    dob_year_input.send_keys()
    time.sleep(random.randint(1, 9))

    # Locate and fill gender portion of form 
    gender = user['gender']

    if gender == 0:
        male = web.find_element_by_xpath('//*[@id="__next"]/main/div[2]/div/form/fieldset/div/div[1]/label/span[1]')
        male.send_keys()
    elif gender == 1:
        female = web.find_element_by_xpath('//*[@id="__next"]/main/div[2]/div/form/fieldset/div/div[2]/label/span[1]')
        female.send_keys()
    elif gender == 2:
        nonbinary = web.find_element_by_xpath('//*[@id="__next"]/main/div[2]/div/form/fieldset/div/div[3]/label/span[1]')
        nonbinary.send_keys()
    else:
        print(">> ERROR:\n>> Invalid gender input")

    time.sleep(random.randint(1, 9))    

    # Locate and fill marketing information portion of form
    if user['opt_in'] == 1:
        marketing_information = web.find_element_by_xpath('//*[@id="__next"]/main/div[2]/div/form/div[6]/div/label/span[1]')        
        marketing_information.send_keys()
    time.sleep(random.randint(1, 9))   

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
            "proxy": prox.get(),
            "verified": ''
     }

    sign_up(newUser)

if __name__ == "__main__":
    main()    
