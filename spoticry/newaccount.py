import os
import sys
import json
import time
import random 
import string
import hashlib
import requests
from requests import HTTPError
from selenium import webdriver
from pathlib import Path


apikeycapatcha = 'cfdd1e0dafb83224e79a5ade1e9191a9'
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
domains = ['@mailkept.com', '@promail1.net', '@rcmails.com', '@relxv.com', '@folllo.com', '@fortuna7.com', '@invecra.com', '@linodg.com', '@awiners.com', '@subcaro.com']
sign_up_url = 'https://www.spotify.com/us/signup'


class dob:
    def __init__(self, month, day, year):
        self.month = month
        self.day = day
        self.year = year       


def sign_up():
# Handles sign-up process using generated user info
    
    # Use Google Chrome webdriver to handle form filling
    web = webdriver.Chrome() 

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


def select_entry(filename):
# Selects random string from random line in text document

    with open(filename, "r") as doc:
        text = doc.read()
        words = list(map(str, text.split()))
    doc.close()    
    return random.choice(words)


def generate_password(length):
# Random password generator of length provided
    
    charset = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(charset) for i in range(length))
    return password


def generate_username(exec_code):
# Random username generator 

    markers = [0, 0, 0, 0]          # Markers used to prevent duplicate entries
    op0 = random.randint(0, 99)     # appended numbers to username
    op1 = ''                        # first name options
    op2 = ''                        # last name options
    op3 = ''                        # random word from words list
    username = ''                   # empty username string

    for i in range(2):
        # Get random marker
        username_order = random.randint(0, 3)

        # If marker indicates the choice has already been made 
        if (markers[username_order] == 1):
            if username_order == 3:                 # If polled int is 3, wrap around to 0
                username_order = 0
            else:
                username_order = username_order + 1 # If polled int is < 3, increment   

        if username_order == 0:
            markers[0] = 1
            username = username + str(op0)
        elif username_order == 1:
            markers[1] = 1
            op1 = select_entry("src/txt/fname.txt")  
            username = username + op1  
        elif username_order == 2:
            markers[2] = 1
            op2 = select_entry("src/txt/lname.txt")  
            username = username + op2 
        elif username_order == 3:
            markers[3] = 1
            op3 = select_entry("src/txt/words.txt") 

            # If length of string is unreasonably long, reselect
            while len(op3) > 8:
                op3 = select_entry("src/txt/words.txt") 
            username = username + op3

    # exec_code used for formatted returns during testing stages.
    if exec_code == 1:
        return username
    elif exec_code == 0:
        return username


def generate_email(domain_index):
# Generates email address and corresponding MD5 hash of email    
    # Generate random string for email
    base_string = generate_username(1)
    domain = domains[domain_index]

    email = base_string + domain

    # Email MD5 Hash key calculated for Temp Mail API Usage
    email_hash = hashlib.md5(email.encode('utf-8')).hexdigest()
    return email, email_hash


def generate_birthday(dob_month, dob_day, dob_year):
# Generate complete indexed date-of-birth object

    month = months[dob_month]
    birthday = dob(month, dob_day, dob_year)
    return birthday
  

def update_records(email_hash, data):
# Updates JSON records with aggregated, generated user infomration

    __nof = 'src/ref/__nof'
    __dir = os.path.join('/src/json')       # JSON output directory
    b_dir = os.path.isfile(__dir)           # checks if __dir exists

    if not b_dir:
        try:
            os.makedirs(__dir)
        except:     
            print("\n>>> ERROR\n>>> ID: " + email_hash + '\n>>> Could not create output directory\n')
            sys.exit()

    obj = json.dumps(data, indent=4)    # Create JSON object from dictionary

    try:
        with open(__nof, 'r') as n:     # Read from count file
            num = int(n.readline()) + 1 # Set account number to count++
            n.truncate()                # Erase file data
            n.write(num)                # Write new value to file
        
        zf = num.zfill(5)                           # Account number
        export = 'src/json/' + str(zf) + '.json'    # Path to account JSOn

        try:
            with open(export, 'x') as x:
                json.dump(obj, x)
        except:
            print("\n>>> ERROR\n>>> ID: " + email_hash + '\n>>> Could not create JSON file\n')
    except FileNotFoundError:
        try:
            with open(__nof, 'x') as m:
                m.write(int(0))
        except:
            print("\n>>> ERROR\n>>> ID: " + email_hash + '\n>>> Could not create index file\n')
        
    return obj


def main():

    for i in range(25):
        # Random elements initialized
        password_length = random.randint(8, 16)
        domain_index = random.randint(0, 9)
        dob_month = random.randint(0, 11)
        dob_day = random.randint(1, 28)
        dob_year = random.randint(1982, 2006)

        # Generate spotifyUser data
        email, email_hash = generate_email(domain_index)            # Generate temp email address and email MD5 hash token
        username = generate_username(0)                             # Generate random username
        password = generate_password(password_length)               # Generate random password
        birthday = generate_birthday(dob_month, dob_day, dob_year)  # Generate random birthday
        gender = random.randint(0, 2)                               # Generate random gender selection
        marketing_info = random.randint(0, 1)                       # Generate random response to marketing infomation

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
            "md5_hash": email_hash
        }

        obj = update_records(email_hash, newUser)
        
        print("\n>> User " + newUser.username + " successfully generated")
        print("\n" + obj)

    
if __name__ == "__main__":
    main()    