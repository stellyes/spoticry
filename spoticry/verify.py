import os
import sys
import time
import json
import random
import requests
import spoticore

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
    time.sleep(random.randint(3, 12))

    # Locate and fill email portion of form
    email_input = web.find_element(By.XPATH, '//*[@id="email"]')
    email_input.send_keys(user['email'])
    time.sleep(random.randint(1, 9))

    # Locate and fill email confirmation portion of form
    email_confirmation_input = web.find_element(By.XPATH, '//*[@id="confirm"]')
    email_confirmation_input.send_keys(user['email'])
    time.sleep(random.randint(1, 9))

    # Locate and fill password portion of form
    password_input = web.find_element(By.XPATH, '//*[@id="password"]')
    password_input.send_keys(user['pass'])
    time.sleep(random.randint(1, 9))

    # Locate and fill profile name portion of form
    username_input = web.find_element(By.XPATH, '//*[@id="displayname"]')
    username_input.send_keys(user['user'])
    time.sleep(random.randint(1, 9))

    # Locate and fill month portion of form
    dob_month_input = Select(web.find_element(By.XPATH, '//*[@id="month"]'))
    dob_month_input.select_by_visible_text(user['dob']['month'])
    time.sleep(random.randint(1, 9))

    # Locate and fill day portion of form
    dob_day_input = web.find_element(By.XPATH, '//*[@id="day"]')
    dob_day_input.send_keys(user['dob']['day'])
    time.sleep(random.randint(1, 9))

    # Locate and fill year portion of form
    dob_year_input = web.find_element(By.XPATH, '//*[@id="year"]')
    dob_year_input.send_keys(user['dob']['year'])
    time.sleep(random.randint(1, 9))

    # Locate and fill gender portion of form 
    gender = user['gender']

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

    time.sleep(random.randint(1, 9))    

    # Locate and fill marketing information portion of form
    if user['opt_in'] == 1:
        marketing_information = web.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/form/div[6]/div/label/span[1]')        
        marketing_information.click()

    time.sleep(random.randint(1, 9))   

    # Solve Captcha
    WebDriverWait(web, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//*[@id=\"checkbox-container\"]/div/div/iframe")))
    web.execute_script("arguments[0].click();", WebDriverWait(web, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='recaptcha-checkbox goog-inline-block recaptcha-checkbox-unchecked rc-anchor-checkbox']/div[@class='recaptcha-checkbox-checkmark']"))))
    time.sleep(60)


def main():
    newUser = {
            "email": 'testemail@email.com',
            "user": 'testuser',
            "pass": 'testpass',
            "dob": {
                "day": 1,
                "month": 'January',
                "year": 1998
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
