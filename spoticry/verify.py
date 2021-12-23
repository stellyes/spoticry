import sys
import time
import proxy 
import random
import requests
from hashlib import md5
from requests import HTTPError
from selenium import webdriver


apikeycapatcha = 'cfdd1e0dafb83224e79a5ade1e9191a9'
sign_up_url = 'https://www.spotify.com/us/signup'


def select_proxy():
    # Selects random proxy from proxy list

    with open("src/txt/proxy.txt", "r") as doc:
        text = doc.read()
        proxylist = list(map(str, text.split()))
    doc.close()
    return random.choice(proxylist)


def sign_up(user):
    # Handles sign-up process using generated user info

    # Selecting and assigning proxy
    PROXY = select_proxy()
    chrome_options = webdriver.ChromeOptions()               # Options argument initalization
    chrome_options.add_argument('--proxy-server=%s' % PROXY) # Assigns proxy

    # Uncomment when debugging is complete
    # chrome_options.add_argument('--headless')                # Specifies GUI display, set to headless (NOGUI)

    # Use Google Chrome webdriver to handle form filling      
    web = webdriver.Chrome(options=chrome_options) 

    # Open Spotify sign-up URL via webdriver
    web.get(sign_up_url)
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

def main():
    user = {
            "email": 'test@test.com',
            "user": 'test',
            "pass": 'account',
            "dob": {
                "day": 1,
                "month": 'January',
                "year": 1999
            },
            "gender": 1,
            "opt_in": 1,
            "md5_hash": md5('test@test.com'),
            "proxy": proxy.get(),
            "verified": {
                "status": '',
                "date": ''
            }
        }

    sign_up(user)

    sys.exit()

if __name__ == "__main__":
    main()