import os
import time
import json
import string
import random

class dob:
    def __init__(self, month, day, year):
        self.month = month
        self.day = day
        self.year = year

def select_entry(filename):
    '''
    Selects random string from random line in text document
    '''
    with open(filename, "r") as doc:
        text = doc.read()
        words = list(map(str, text.split()))
    doc.close()
    return random.choice(words)

def generate_password(length):
    '''
    Random password generator of length provided
    '''
    charset = string.ascii_letters + string.digits + '!#@&^*()<>?'
    password = ''.join(random.choice(charset) for i in range(length))
    return password

def generate_username():
    '''
    Random username generator
    '''

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
                username_order = username_order + 1  # If polled int is < 3, increment

        if username_order == 0:
            markers[0] = 1
            username = username + str(op0)
        elif username_order == 1:
            markers[1] = 1
            op1 = select_entry("resources/data/fname.txt")
            username = username + op1
        elif username_order == 2:
            markers[2] = 1
            op2 = select_entry("resources/data/lname.txt")
            username = username + op2
        elif username_order == 3:
            markers[3] = 1
            op3 = select_entry("resources/data/words.txt")

            # If length of string is unreasonably long, reselect
            while len(op3) > 8:
                op3 = select_entry("resources/data/words.txt")
            username = username + op3

    return username    

def generate_email():
    '''
    Generates email address
    '''
    # Generate random string for email
    base_string = generate_username()

    email = base_string + '@mailsac.com'

    return email, base_string


def get_proxy():
    '''
    Pick random proxy server in directorty
    '''  

    root = 'resources/proxies/'  
    file = random.choice(os.listdir(root))                   
    country = root + file
    proxy = select_entry(country)
    parsed_country = file[:-4]

    return { "ip": proxy, "country": parsed_country } # file.removesuffix('.txt')    
    

def lambda_handler(event, context):
    print(">>\n>> Generating new user...")

    # Random elements initialized
    password_length = random.randint(8, 16)
    dob_month = random.randint(1, 11)
    dob_day = random.randint(1, 28)
    dob_year = random.randint(1982, 2006)
    
    # Generate temp email address
    print(">> Generating email and username")
    email, username = generate_email()
    # Generate random password
    print(">> Generating password")
    charset = string.ascii_letters + string.digits + '!#@&^*()<>?'
    password = ''.join(random.choice(charset) for i in range(password_length))
    # Generate random birthday
    print(">> Generating birthday")
    birthday = dob(dob_month, dob_day, dob_year)
    # Generate random gender selection
    print(">> Generating gender")
    gender = random.randint(0, 2)
    # Generate random proxy from list of scraped proxies
    print(">> Generating proxy")
    proxy_info = get_proxy()

    print(">> Credentials for " + username + " generated")

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
        "proxy": proxy_info,
        "created": {
            "status": '',
            "date": ''
        }
    }

    return ({ "response": 200, "body": newUser })   