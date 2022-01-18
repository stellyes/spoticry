import time
import utils
import random
import requests

from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


def generate_user(user):

    gender = user['gender']

    if gender == 0:
        parsed_gender = "male"
    elif gender == 1:
        parsed_gender = "female"
    elif gender == 2:
        parsed_gender = "non-binary"
        
    headers={"Accept-Encoding": "gzip",
             "Accept-Language": "en-US",
             "App-Platform": "Android",
             "Connection": "Keep-Alive",
             "Content-Type": "application/x-www-form-urlencoded",
             "Host": "spclient.wg.spotify.com",
             "User-Agent": "Spotify/8.6.72 Android/29 (SM-N976N)",
             "Spotify-App-Version": "8.6.72",
             "X-Client-Id": utils.generate_random_string(32)}
    
    payload = {"creation_point": "client_mobile",
            "gender": parsed_gender,
            "birth_year": user['dob']['year'],
            "displayname": user['user'],
            "iagree": "true",
            "birth_month": user['dob']['month'],
            "password_repeat": user['pass'],
            "password": user['pass'],
            "key": "142b583129b2df829de3656f9eb484e6",
            "platform": "Android-ARM",
            "email": user['email'],
            "birth_day": user['dob']['day']}
    
    r = requests.post('https://spclient.wg.spotify.com/signup/public/v1/account/', headers=headers, data=payload)

    if r.status_code==200:
        if r.json()['status']==1:
            return (True, time.time())
        else:
            #Details available in r.json()["errors"]
            print(r.json()["errors"])
            return (False, "Could not create the account, some errors occurred")
    else:
        return (False, "Could not load the page. Response code: "+ str(r.status_code))             


def newinstance(user):
    
    proxy = user['proxy']['ip']

    chrome_options = webdriver.ChromeOptions()                  # Options argument initalization
    chrome_options.add_argument('--proxy-server=%s' % proxy)  # Assigns proxy
    # chrome_options.add_argument('--headless')                   # Specifies GUI display, set to headless (NOGUI)
    chrome_options.add_argument('--ignore-certificate-errors')  # Minimize console output
    chrome_options.add_argument('--ignore-ssl-errors')          # Minimize console output
    chrome_options.add_argument('log-level=3')                  # Minimize console output
    
    # Use Google Chrome webdriver to handle form filling      
    web = webdriver.Chrome(executable_path=r"src/webdriver/chromedriver.exe", options=chrome_options)  

    web.get('https://accounts.spotify.com/ua/login')
    
    time.sleep(5)

    email = web.find_element(By.XPATH, '//*[@id="login-username"]')
    email.send_keys(user['email'])
    time.sleep(random.randint(2, 8))

    password = web.find_element(By.XPATH, '//*[@id="login-password"]')
    password.send_keys(user['pass'])
    time.sleep(random.randint(2, 8))

    login = web.find_element(By.XPATH, '//*[@id="login-button"]')
    login.click()
    time.sleep(random.randint(5, 10))

    webplayer = web.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/button[2]')
    webplayer.click()

    html_object = web.page_source
    track_length = html_object.xpath("//*[@id=\"main\"]/div/div[2]/div[2]/footer/div/div[2]/div/div[2]/div[3]")

    playButton = '//*[@id="main"]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/button'
    forwaredButton = '//*[@id="main"]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/div[2]/button[1]'
    backButton = '//*[@id="main"]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/div[1]/button[2]'
    shuffleButton = '//*[@id="main"]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/div[1]/button[1]'
    repeatButton = '//*[@id="main"]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/div[2]/button[2]'

    muteButton = '//*[@id="main"]/div/div[2]/div[2]/footer/div/div[3]/div/div[3]/button'
    
    time.sleep(15)

    


if __name__ == "__main__":
    newinstance({'email': 'me@rengland.org', 'pass': '!8192Rde', 'proxy': {'ip': '154.21.39.177:6015', 'country': 'US'}})   