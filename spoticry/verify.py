import os
import sys
import time
import json
import random
import requests
from requests.exceptions import HTTPError
import spoticore 

from spoticore import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_email(md5):

    http_response = 400

    url = "https://privatix-temp-mail-v1.p.rapidapi.com/request/mail/id/" + md5 + "/"

    head = {
        'x-rapidapi-host': "privatix-temp-mail-v1.p.rapidapi.com",
        'x-rapidapi-key': "da6d75ca4emsh6141adc1de07170p15d12ajsn08a3f957a221"
    } 

    try:
        r = requests.get(
            url, 
            headers=head
        )

        try:
            r.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP request failed: {http_err}')

        http_response = 200     

    except HTTPError as http_err:
        print(f'HTTP error occured: {http_err}')
    except Exception as err:
        print(f'Other error occured during email fetch: {err}')

    return http_response, r

def sign_up(user):
    # Handles sign-up process using generated user info

    # Selecting and assigning proxy
    #proxy = user['proxy']['ip']

    chrome_options = webdriver.ChromeOptions()                  # Options argument initalization
    # chrome_options.add_argument('--proxy-server=%s' % proxy)  # Assigns proxy
    # chrome_options.add_argument('--headless')                   # Specifies GUI display, set to headless (NOGUI)
    chrome_options.add_argument('--ignore-certificate-errors')  # Minimize console output
    chrome_options.add_argument('--ignore-ssl-errors')          # Minimize console output
    chrome_options.add_argument('log-level=3')                  # Minimize console output
    
    # Use Google Chrome webdriver to handle form filling      
    web = webdriver.Chrome(
        executable_path=('src/webdriver/chromedriver.exe'), 
        options=chrome_options
        ) 

    # Open Spotify sign-up URL via webdriver
    print(">> Loading webpage...")
    web.get(spoticore.SIGN_UP_URL_US) 
    print(">> Webpage loaded")
    time.sleep(random.randint(3, 12))

    # Locate and fill email portion of form
    print(">>\t Filling email input box...")
    email_input = web.find_element(By.XPATH, '//*[@id="email"]')
    email_input.send_keys(user['email'])
    time.sleep(random.randint(1, 9))

    # Locate and fill email confirmation portion of form
    print(">>\t Filling email confirmation box...")
    email_confirmation_input = web.find_element(By.XPATH, '//*[@id="confirm"]')
    email_confirmation_input.send_keys(user['email'])
    time.sleep(random.randint(1, 9))

    # Locate and fill password portion of form
    print(">>\t Filling password input box...")
    password_input = web.find_element(By.XPATH, '//*[@id="password"]')
    password_input.send_keys(user['pass'])
    time.sleep(random.randint(1, 9))

    # Locate and fill profile name portion of form
    print(">>\t Filling username input box...")
    username_input = web.find_element(By.XPATH, '//*[@id="displayname"]')
    username_input.send_keys(user['user'])
    time.sleep(random.randint(1, 9))

    # Locate and fill month portion of form
    print(">>\t Filling date of birthmonth input box...")
    dob_month_input = Select(web.find_element(By.XPATH, '//*[@id="month"]'))
    dob_month_input.select_by_visible_text(user['dob']['month'])
    time.sleep(random.randint(1, 9))

    # Locate and fill day portion of form
    print(">>\t Filling date of birthday input box...")
    dob_day_input = web.find_element(By.XPATH, '//*[@id="day"]')
    dob_day_input.send_keys(user['dob']['day'])
    time.sleep(random.randint(1, 9))

    # Locate and fill year portion of form
    print(">>\t Filling date of birth year box...")
    dob_year_input = web.find_element(By.XPATH, '//*[@id="year"]')
    dob_year_input.send_keys(user['dob']['year'])
    time.sleep(random.randint(1, 9))

    # Locate and fill gender portion of form 
    gender = user['gender']

    print(">>\t Filling gender...")
    if gender == 0:
        male = web.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/form/fieldset/div/div[1]/label/span[1]')
        male.click()
    elif gender == 1:
        female = web.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/form/fieldset/div/div[2]/label/span[1]')
        female.click()
    elif gender == 2:
        nonbinary = web.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/form/fieldset/div/div[3]/label/span[1]')
        nonbinary.click()
    else:
        print(">> ERROR:\n>> Invalid gender input")
        return False

    time.sleep(random.randint(1, 9))    

    # Locate and fill marketing information portion of form
    print(">>\t Answering marketing opt-in/opt-out...")
    if user['opt_in'] == 1:
        marketing_information = web.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/form/div[6]/div/label/span[1]')        
        marketing_information.click()

    time.sleep(random.randint(1, 9))   

    # Solve Captcha
    print(">>\t Solving reCaptcha...")
    WebDriverWait(web, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//*[@id=\"checkbox-container\"]/div/div/iframe")))
    web.execute_script("arguments[0].click();", WebDriverWait(web, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='recaptcha-checkbox goog-inline-block recaptcha-checkbox-unchecked rc-anchor-checkbox']/div[@class='recaptcha-checkbox-checkmark']"))))
    
    # Initialize temp-mail inbox
    response, data = get_email(user['md5_hash'])

    print('[' + response + ']:\n[DATA]: \n' + data)
    sys.exit()



def main():
    newUser = {
        "email": "GlazenerMahlon@invecra.com",
        "user": "cabinJohannesen",
        "pass": "m_|2^r&Sf0t2",
        "dob": {
            "day": 7,
            "month": "March",
            "year": 2003
        },
        "gender": 2,
        "opt_in": 1,
        "md5_hash": "cf953d3ec639b6caf09ab50a7a52d0e2",
        "proxy": {
            "ip": "188.132.241.162:56109",
            "country": "TR",
            "protocol": "socks5"
        },
        "verified": {
            "status": "",
            "date": ""
        }
    }

    sign_up(newUser)

if __name__ == "__main__":
    main()    
