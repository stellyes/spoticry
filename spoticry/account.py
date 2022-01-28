import sys
import json
import time
import utils
import string
import random
import requests
import spoticore

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException

def request(user):
    headers= {
        "Accept-Encoding": "gzip",
        "Accept-Language": "en-US",
        "App-Platform": "Android",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "spclient.wg.spotify.com",
        "User-Agent": "Spotify/8.6.72 Android/29 (SM-N976N)",
        "Spotify-App-Version": "8.6.72",
        "X-Client-Id": utils.generate_random_string(32)
    }
    
    payload = {
    "creation_point": "client_mobile",
    "gender": "male" if random.randint(0, 1) else "female",
    "birth_year": random.randint(1990, 2000),
    "displayname": user['user'],
    "iagree": "true",
    "birth_month": random.randint(1, 11),
    "password_repeat": user['pass'],
    "password": user['pass'],
    "key": "142b583129b2df829de3656f9eb484e6",
    "platform": "Android-ARM",
    "email": user['email'],
    "birth_day": random.randint(1, 20)
    }

    r = requests.post('https://spclient.wg.spotify.com/signup/public/v1/account/', headers=headers, data=payload, proxies={"http": user['proxy']['ip']})
    time.sleep(random.randint(3, 5))

    if r.status_code==200:
        if r.json()['status']==1:
            return True, time.time()
        else:
            False, time.time()
    else:
        print(">> Spotify account failed initialization - 400")
        False, time.time()


def main():
    valid = False

    while not valid:
        try:
            amount = input(">>\n>> Spoticry Account Tool v0.0.2\n>> How many accounts do you wish to create? : ")
            amount = int(amount)
            valid = True
        except ValueError as VE:
            print(">> " + utils.bcolors.WARNING + "WARNING: Error converting input. Please provide a valid input" + utils.bcolors.ENDC)    

    for i in range(amount):
        print(">>\n>> Generating new user...")

        # Random elements initialized
        password_length = random.randint(8, 16)
        domain_index = random.randint(0, 9)
        dob_month = random.randint(1, 11)
        dob_day = random.randint(1, 28)
        dob_year = random.randint(1982, 2006)

        # Generate spotifyUser data
        # Generate temp email address and email MD5 hash token
        email = utils.generate_email(domain_index)

        # Generate random username
        username = utils.generate_username()
        # Generate random password
        password = utils.generate_password(password_length)
        # Generate random birthday
        birthday = utils.generate_birthday(dob_month, dob_day, dob_year)
        # Generate random gender selection
        gender = random.randint(0, 2)
        # Generate random response to marketing infomation
        marketing_info = random.randint(0, 1)
        # Generate random proxy from list of scraped proxies
        proxy_info = utils.get_proxy()

        print(">> Credentials for " + username + " generated")

        # Create email user in AWS
        print(">> Initializing email in AWS WorkMail...")
        resp = utils.create_email(username, password, email)

        # Create spotifyUser dictionary
        newUser = {
            "email": email,
            "user": username,
            "pass": password,
            "dob": {
                "day": birthday.day,
                "month": birthday.month,
                "year": birthday.year
            },
           "gender": gender,
            "opt_in": marketing_info,
            "proxy": proxy_info,
            "created": {
                "status": '',
                "date": ''
            },
            "verified": {
                "status": '',
                "date": ''
            }
        }

            
        # Send credentials to sign-up page using webdriver
        print(">> Verifying user...")
        site = utils.get_sitemap()
        status, date = request(newUser)
        newUser["created"]["status"] = status
        newUser["created"]["date"] = date

        # Print generated user to JSON file
        time.sleep(30)
        utils.create_user(newUser)

        print(">> " + utils.bcolors.BOLD + "User " + newUser["user"] + " successfully generated" + utils.bcolors.ENDC)
    
    print(">>\n>> " + utils.bcolors.OKGREEN + utils.bcolors.BOLD + str(amount) + " users successfully generated. Closing..." + utils.bcolors.ENDC + "\n")


if __name__ == "__main__":
    main()
