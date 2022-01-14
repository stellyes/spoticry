import os
import sys
import time
import json
import utils
import random
import requests
import spoticore 
import captcha

from requests.exceptions import HTTPError

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pydub
import ffmpy
import urllib
import speech_recognition as sr


MAIL_API_KEY = '?_mailsacKey=k_Gdc5XksqCSrfjILfwnaUilpCPRrOf70fbA2g99d3'
CAPTCHA_API_KEY = 'cfdd1e0dafb83224e79a5ade1e9191a9'
API_REQ_URL = 'https://2captcha.com/in.php?'
API_RES_URL = 'https://2captcha.com/res.php?'


def init_email(email):

    http_response = 400

    url = "https://mailsac.com/api/addresses/" + email + MAIL_API_KEY

    try:
        r = requests.post(url)

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


def verify_account(email):

    http_response = 400

    url = "https://mailsac.com/api/addresses/" + email + "/messages" + MAIL_API_KEY

    try:
        r = requests.get(url)

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

def captcha_id():
    '''
    returns captcha id for page
    
    '''


    print(">> Gathering reCaptcha information...")

    html = requests.get(utils.SIGN_UP_URL_US)                                                 # Gets HTML source
    parsed = BeautifulSoup(html.text, 'html.parser')                                # Parses HTML response as raw HTML
    json_res = parsed.find('script', id='__NEXT_DATA__', type='application/json')   # Finds <script> tag with captcha info
    json_str = str(json_res)                        # Converts HTML response to string
    json_str = json_str.removesuffix('</script>')   # Removes ending tag from string
    json_str = json_str[92:]                        # Removes header tags with excess data

    json_obj = json.loads(json_str)
    json_obj = json.loads(json_str)                 # Converts string to JSON object

    solved = json_obj['props']['pageProps']['data']['recaptchaCheckboxKey']
    print("recaptchaCheckboxKey: " + solved)

    return solved
    

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
    web = webdriver.Chrome(executable_path='src/webdriver/chromedriver.exe', options=chrome_options)
    print(">> Loading webpage...")
    web.get(utils.SIGN_UP_URL_US) 
    time.sleep(random.randint(5, 12))

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
    print(">>\t Filling month input box...")
    dob_month_input = Select(web.find_element(By.XPATH, '//*[@id="month"]'))
    dob_month_input.select_by_visible_text(user['dob']['month'])
    time.sleep(random.randint(1, 9))

    # Locate and fill day portion of form
    print(">>\t Filling day input box...")
    dob_day_input = web.find_element(By.XPATH, '//*[@id="day"]')
    dob_day_input.send_keys(user['dob']['day'])
    time.sleep(random.randint(1, 9))

    # Locate and fill year portion of form
    print(">>\t Filling year input box...")
    dob_year_input = web.find_element(By.XPATH, '//*[@id="year"]')
    dob_year_input.send_keys(user['dob']['year'])
    time.sleep(random.randint(1, 9))

    # Locate and fill gender portion of form 
    gender = user['gender']

    print(">>\t Filling gender...")
    if gender == 0:
        WebDriverWait(web, 20).until(EC.invisibility_of_element((By.XPATH, "//*[@id=\"__next\"]/main/div[2]/div/form/fieldset/div/div[1]/label")))
        web.execute_script("arguments[0].click();", WebDriverWait(web, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"__next\"]/main/div[2]/div/form/fieldset/div/div[1]/label"))))
    elif gender == 1:
        WebDriverWait(web, 20).until(EC.invisibility_of_element((By.XPATH, "//*[@id=\"__next\"]/main/div[2]/div/form/fieldset/div/div[1]/label")))
        web.execute_script("arguments[0].click();", WebDriverWait(web, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"__next\"]/main/div[2]/div/form/fieldset/div/div[2]/label"))))
    elif gender == 2:
        WebDriverWait(web, 20).until(EC.invisibility_of_element((By.XPATH, "//*[@id=\"__next\"]/main/div[2]/div/form/fieldset/div/div[1]/label")))
        web.execute_script("arguments[0].click();", WebDriverWait(web, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"__next\"]/main/div[2]/div/form/fieldset/div/div[3]/label"))))
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
    time.sleep(random.randomint(5, 10))

    # Sign up button
    WebDriverWait(web, 20).until(EC.invisibility_of_element((By.CLASS_NAME, "Button-qlcn5g-0 dmJlSg")))
    web.execute_script("arguments[0].click();", WebDriverWait(web, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "Button-qlcn5g-0 dmJlSg"))))
    



def main():
    newUser = {
        "email": "idolater1@mailsac.com",
        "user": "flatuousMarissa",
        "pass": "(Q:$Eo|u7",
        "dob": {
            "day": 26,
            "month": "February",
            "year": 1991
        },
        "gender": 0,
        "opt_in": 0,
        "proxy": {
            "ip": "200.30.170.82:8080",
            "country": "GT",
            "protocol": "http"
        },
        "verified": {
            "status": "",
            "date": ""
        }
    }

    sign_up(newUser)

if __name__ == "__main__":
    main()    
